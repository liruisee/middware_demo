from django.middleware.common import MiddlewareMixin
from django.http.response import HttpResponseBase
from base_app.responses import JsonResponse
import traceback
from base_app.base_logger import get_logger, get_request_logger
from base_app.exceptions import ViewException
import json
from django.core.handlers.wsgi import WSGIRequest
from oslo_utils import uuidutils
import time
import chardet


# 请求日志中间件
class RequestLogMiddleWare(MiddlewareMixin):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request_logger_dict = {}
        self.logger_dict = {}
        self.log_template = "module:%(module)s|func_name:%(func_name)s|method:%(method)s|args:%(args)s|kwargs:%(kwargs)s|" \
                            "request_id:%(request_id)s|remote_ip:%(remote_ip)s|url:%(url)s"

    @staticmethod
    def get_decode_type(byte_str: bytes) -> str:
        encode_name = chardet.detect(byte_str)['encoding'] or 'utf-8'
        if encode_name == 'ascii':
            encode_name = 'unicode_escape'
        return encode_name

    # 当请求过来，首先经过process_request函数
    def process_request(self, request):
        pass

    # 请求日志主函数，这里处理异常后，会屏蔽掉django默认的异常处理
    def process_view(self, request: WSGIRequest, callback, callback_args, callback_kwargs):
        # 绑定请求id
        url = request.get_full_path().split('?', 1)[0]

        def get_err_data():
            nonlocal request, callback_args, callback_kwargs, url
            # 如果出现异常，将请求的body打印出来
            encode_name = self.get_decode_type(request.body)
            request_body = request.body.decode(encode_name)
            try:
                user_id = request.user_info['id']
                user_name = request.user_info['name']
            except Exception:
                user_id = None
                user_name = None
            err_data = '\nuser_id：%s\nuser_name：%s\n请求body为：%s\nget信息为：%s\npost信息为：%s\nargs信息为：%s' \
                       '\nkwargs信息为：%s\n%s\nrequest_id:%s\nurl:%s'\
                       % (user_id,
                          user_name,
                          request_body,
                          json.dumps(request.GET, ensure_ascii=False),
                          json.dumps(request.POST, ensure_ascii=False),
                          json.dumps(callback_args, ensure_ascii=False),
                          json.dumps(callback_kwargs, ensure_ascii=False),
                          request.method,
                          request.request_id,
                          url
                          )
            return err_data

        request.request_id = uuidutils.generate_uuid().replace('-', '')
        log_dict = {
            'module': callback.__module__,
            'func_name': callback.__name__,
            'method': request.method,
            'args': str(callback_args),
            'kwargs': str(callback_kwargs),
            'remote_ip': request.META['REMOTE_ADDR'],
            'request_id': request.request_id,
            'url': url
        }
        log_prefix = self.log_template % log_dict

        app_name = log_dict['module'].split('.', 1)[0]
        if app_name not in self.request_logger_dict:
            self.request_logger_dict[app_name] = get_request_logger(app_name=app_name)
        if app_name not in self.logger_dict:
            self.logger_dict[app_name] = get_logger(app_name=app_name)
        request_logger = self.request_logger_dict[app_name]
        logger = self.logger_dict[app_name]
        try:
            time_start = time.time()
            request_logger.info("%s|start request" % log_prefix)

            logger.debug(f'\033[31;1mbody: {request.body.decode("utf-8")}\033[0m')
            logger.debug(f'\033[34;1m{str(request.COOKIES)}\033[0m')

            get_data = request.GET
            get_data._mutable = True
            if request.method == 'GET':
                for key in ('page_total', 'record_cnt'):
                    if key in get_data:
                        del get_data[key]
            get_data._mutable = False

            response = callback(request, *callback_args, **callback_kwargs)
            use_time = time.time() - time_start
            request_logger.info("%s|success request,use_time:%s sec" % (log_prefix, use_time))

            if not issubclass(type(response), HttpResponseBase):
                logger.error("%s|the return object type is not the subclass of HttpResponseBase"
                             "返回数据类型为：%s，返回数据值为：%s" % (log_prefix, str(type(response)), str(response)))
                return JsonResponse({
                    'message': '返回的内容非HttpResponseBase类型，请检查数据', 'status': -1},
                    json_dumps_params={'ensure_ascii': False}
                )
            return response

        except ViewException as e:
            if e.traceback != '':
                logger.error(e.traceback)
            else:
                logger.warning(str(e.err_dict))

            err_data = get_err_data()
            logger.error(traceback.format_exc() + err_data)
            return e.response(request.request_id, err_data.strip('\n').split('\n'))

        # 处理一般情况下的异常（主要是开发者忘记处理的异常）
        except Exception as e:
            # 请求出现异常，记录到日志中
            err_data = get_err_data()

            err_traceback = traceback.format_exc()
            logger.error("%s <====> %s\n%s" % (log_prefix, err_traceback, err_data))
            err_dict = {
                'status': -1,
                'message': 'unexpect error',
                'result': str(e),
                'request_id': request.request_id
            }
            return JsonResponse(err_dict)

    def process_response(self, request, response):
        if 'default' not in self.logger_dict:
            self.logger_dict['default'] = get_logger(app_name='default')
        logger = self.logger_dict['default']
        if response.status_code <= 400:
            return response
        if type(response) is JsonResponse:
            return response
        url = request.get_raw_uri()
        logger.error('%s ,%s，url：%s' % (str(response.status_code), str(response.reason_phrase), url))
        return JsonResponse(
            {
                'status': response.status_code, 'message': 'unexpect error',
                'result': '%s ,%s' % (str(response.status_code), str(response.reason_phrase))
            },
            json_dumps_params={'ensure_ascii': False}
        )
