from contextlib import closing, contextmanager

import click
import psycopg2
from dodoo import odoo

from .format import process


@contextmanager
def OdooTestExecution(self):
    connection = {"dbname": self.database}
    if odoo.tools.config["db_host"]:
        connection.update({"host": odoo.tools.config["db_host"]})
    if odoo.tools.config["db_port"]:
        connection.update({"port": odoo.tools.config["db_port"]})
    if odoo.tools.config["db_user"]:
        connection.update({"user": odoo.tools.config["db_user"]})
    if odoo.tools.config["db_password"]:
        connection.update({"password": odoo.tools.config["db_password"]})
    with closing(psycopg2.connect(**connection)) as conn, conn.cursor() as cr:
        cr.execute(
            """ALTER TABLE ir_logging ADD COLUMN IF NOT EXISTS "test_run" INTEGER;"""
        )
        conn.commit()
    try:
        yield odoo.service.server.start(preload=[self.database], stop=True)
    finally:
        with closing(psycopg2.connect(**connection)) as conn, conn.cursor() as cr:
            cr.execute(
                """
                SELECT name,
                       LEVEL,
                       message,
                       path,
                       func,
                       line
                FROM ir_logging WHERE test_run IS NULL;
                """
            )
            logs = cr.fetchall()
            # Mark logs for subsequent runs to filter.
            cr.execute(
                """
                SELECT DISTINCT test_run
                FROM ir_logging
                WHERE test_run IS NOT NULL;

                """
            )
            next_run = max([run for (run,) in cr.fetchall()] or [0]) + 1
            cr.execute(
                """UPDATE ir_logging SET test_run = %s WHERE test_run IS NULL;""",
                (next_run,),
            )
            conn.commit()
            # PostgreSQL 9.2 renamed pg_stat_activity.procpid to pid:
            # http://www.postgresql.org/docs/9.2/static/release-9-2.html#AEN110389
            pid_col = "pid" if conn.server_version >= 90200 else "procpid"
            cr.execute(
                """
                SELECT pg_terminate_backend(%(pid_col)s)
                FROM pg_stat_activity
                WHERE datname = %%s
                AND %(pid_col)s != pg_backend_pid()"""
                % {"pid_col": pid_col},
                (self.database,),
            )

    ctx = click.get_current_context()
    success = process(logs)
    if not success:
        ctx.fail("Tests failed")


@contextmanager
def OdooPyTestExecution(self):
    odoo.service.server.start(preload=[self.database], stop=True)
    with odoo.api.Environment.manage():
        yield
    connection = {"dbname": self.database}
    if odoo.tools.config["db_host"]:
        connection.update({"host": odoo.tools.config["db_host"]})
    if odoo.tools.config["db_port"]:
        connection.update({"port": odoo.tools.config["db_port"]})
    if odoo.tools.config["db_user"]:
        connection.update({"user": odoo.tools.config["db_user"]})
    if odoo.tools.config["db_password"]:
        connection.update({"password": odoo.tools.config["db_password"]})
    with closing(psycopg2.connect(**connection)) as conn, conn.cursor() as cr:
        # PostgreSQL 9.2 renamed pg_stat_activity.procpid to pid:
        # http://www.postgresql.org/docs/9.2/static/release-9-2.html#AEN110389
        pid_col = "pid" if conn.server_version >= 90200 else "procpid"
        cr.execute(
            """
            SELECT pg_terminate_backend(%(pid_col)s)
            FROM pg_stat_activity
            WHERE datname = %%s
            AND %(pid_col)s != pg_backend_pid()"""
            % {"pid_col": pid_col},
            (self.database,),
        )
