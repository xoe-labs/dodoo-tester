from contextlib import closing, contextmanager

import click
import psycopg2
from dodoo import odoo

from .format import process


@contextmanager
def OdooTestExecution(self):
    try:
        yield odoo.service.server.start(preload=[self.database], stop=True)
    finally:
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
                """SELECT name, level, message, path, func, line
                          FROM ir_logging"""
            )
            logs = cr.fetchall()
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
