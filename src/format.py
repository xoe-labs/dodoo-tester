from __future__ import absolute_import, division, print_function, unicode_literals

import logging
import re
import textwrap
from builtins import range

from future import standard_library

standard_library.install_aliases()

_logger = logging.getLogger(__name__)

BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, _NOTHING, DEFAULT = range(10)
# The background is set with 40 plus the number of the color, and the foreground with 30
# These are the sequences need to get colored ouput
RESET_SEQ = "\033[0m"
COLOR_SEQ = "\033[1;%dm"
BOLD_SEQ = "\033[1m"
COLOR_PATTERN = "{}{}%s{}".format(COLOR_SEQ, COLOR_SEQ, RESET_SEQ)


def process(logs):
    warnings = []
    errors = []
    critical = []
    failed = 0

    incident_fmt = """



    {_name}
    ---------------------------------------
    {_path}:{_line}
    {_func}
    _______________________________________

{message}
"""
    file_regex = r'File ".*?odoo'

    def _process_msg(msg):
        try:
            # PY3
            return textwrap.indent(re.sub(file_regex, 'File "odoo', msg), "    *   ")
        except AttributeError:
            wrapper = textwrap.TextWrapper(
                initial_indent="    *   ", subsequent_indent="    *   "
            )
            return wrapper.wrap(re.sub(file_regex, 'File "odoo', msg))

    for (_name, level, message, _path, _func, _line) in logs:
        message.replace
        if "FAILED" in message:
            failed += 1
        if level == "WARNING":
            message = _process_msg(message)
            warnings.append(incident_fmt.format(**locals()))
        if level == "ERROR":
            message = _process_msg(message)
            errors.append(incident_fmt.format(**locals()))
        if level == "CRITICAL":
            message = _process_msg(message)
            critical.append(incident_fmt.format(**locals()))

    summary_fmt = COLOR_PATTERN % (
        30 + CYAN,
        40 + DEFAULT,
        """
    SUMMARY
    ======================================================
    WARNING: {: 3}   ERROR: {: 3}   CRITICAL: {: 3}  FAILED: {: 3}
    ------------------------------------------------------
""".format(
            len(warnings), len(errors), len(critical), failed
        ),
    )

    warnings_fmt = (
        COLOR_PATTERN
        % (
            30 + YELLOW,
            40 + DEFAULT,
            """
    Warnings:
    ======================================================
    {}
""".format(
                ("").join(warnings)
            ),
        )
        if len(warnings)
        else ""
    )
    errors_fmt = (
        COLOR_PATTERN
        % (
            30 + RED,
            40 + DEFAULT,
            """
    Errors:
    ======================================================
    {}
""".format(
                ("").join(errors)
            ),
        )
        if len(errors)
        else ""
    )
    critical_fmt = (
        COLOR_PATTERN
        % (
            30 + RED,
            40 + YELLOW,
            """
    Critical:
    ======================================================
    {}
""".format(
                ("").join(critical)
            ),
        )
        if len(critical)
        else ""
    )
    _logger.info(
        """


    %s


    %s


    %s


    %s
""",
        summary_fmt,
        warnings_fmt,
        errors_fmt,
        critical_fmt,
    )

    return not bool(len(errors) or len(critical) or failed)
