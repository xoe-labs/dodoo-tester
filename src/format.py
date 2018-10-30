
import re

import logging

_logger = logging.getLogger(__name__)


def process(logs):
    warnings = []
    errors = []
    critical = []
    failed = 0

    incident_fmt = """



  | {name}
  | ---------------------------------------
  | {path}:{line}
  | {func}
  | _______________________________________

{message}
"""
    file_regex=r'File ".*?odoo'

    for (_, _, _, name, level, message, path, line, func) in logs:
        message.replace
        if 'FAILED' in message:
            failed += 1
        if level == 'WARNING':
            message = re.sub(file_regex, 'File "odoo', message)
            warnings.append(incident_fmt.format(**locals()))
        if level == 'ERROR':
            message = re.sub(file_regex, 'File "odoo', message)
            errors.append(incident_fmt.format(**locals()))
        if level == 'CRITICAL':
            message = re.sub(file_regex, 'File "odoo', message)
            critical.append(incident_fmt.format(**locals()))


    _logger.info("""


Summary:
======================================================
WARNING: %s     ERROR: %s   CRITICAL: %s    FAILED: %s
------------------------------------------------------


Warnings:
======================================================
%s


Errors:
======================================================
%s


Critical:
======================================================
%s
""", len(warnings), len(errors), len(critical), len(failed),
                 ('').join(warnings),
                 ('').join(errors),
                 ('').join(critical))

    return not bool(len(errors) or len(critical) or failed)
