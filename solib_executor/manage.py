#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import signal
from log_tool.log_simple_util import get_logger


logger = get_logger(app_name='manage', level='DEBUG')
project_path = os.path.abspath(__file__).rsplit('/', 1)[0]
sys.path.append(project_path)


# 回收子进程，避免出现僵尸进程
def sig_handler(sig, frame):
    logger.info(f'触发信号{sig}')
    os.wait()


# SIGINT, SIGSEGV, SIGTERM, SIGSTOP, SIGUSR2
sigs = [1, 15, 2, 3]
result = []
for sig in sigs:
    try:
        signal.signal(sig, sig_handler)
        result.append(str(sig))
    except OSError:
        continue


sigs_str = ', '.join(result)
logger.info(f'监测的所有进程的信号列表为：{sigs_str}')


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'solib_executor.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
