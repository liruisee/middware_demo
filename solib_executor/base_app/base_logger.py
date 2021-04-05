from functools import partial
from django.conf import settings
from utils.log_utils.log_simple_util import get_logger, get_request_logger
import os


is_debug = settings.IS_DEBUG
log_path = str(os.path.abspath(__file__).rsplit('/', 2)[0]) + '/logs'
if is_debug is False:
    get_logger = partial(get_logger, is_debug=False, is_write_file=False, log_path=log_path, level='INFO')
    get_request_logger = partial(get_request_logger, is_debug=False, is_write_file=False, log_path=log_path, level='INFO')
else:
    get_logger = partial(get_logger, is_debug=True, is_write_file=False, log_path=log_path, level='DEBUG')
    get_request_logger = partial(get_request_logger, is_debug=True, is_write_file=False, log_path=log_path, level='DEBUG')
