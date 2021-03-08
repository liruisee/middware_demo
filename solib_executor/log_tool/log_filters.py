import logging


class NoDebugFilter(logging.Filter):

    def __init__(self):
        super().__init__()

    def filter(self, record):
        return False


class DebugFilter(logging.Filter):

    def filter(self, record):
        return True


class InfoFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level in {'INFO', 'WARN', 'ERROR'}:
            return True
        return False


class WarningFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'WARN':
            return True
        return False


class ErrorFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'ERROR':
            return True
        return False


class CriticalFilter(logging.Filter):

    def filter(self, record):
        level = record.levelname.upper()
        if level == 'CRITICAL':
            return True
        return False
