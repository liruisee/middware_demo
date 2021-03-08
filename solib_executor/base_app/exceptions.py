from base_app.responses import JsonResponse
import traceback


DEFAULT_FAILED_RESPONSE = {
    'result': 'failed',
    'status': 400
}


# 自定义app Exception
class ViewException(BaseException):

    def __init__(self, error_key, tb='', update_result: dict=None, is_show_error_detail=False, *args):
        self.args = (error_key, ) + args
        self.err_dict = DEFAULT_FAILED_RESPONSE.copy()
        self.err_dict['message'] = error_key
        if update_result is not None:
            assert(type(update_result) is dict)
            self.err_dict.update(update_result)
        self.traceback = tb
        self.is_show_error_detail = is_show_error_detail

    def response(self, request_id: str, request_info: str):
        if self.is_show_error_detail is True:
            err_traceback = traceback.format_exc()
            self.err_dict['err_detail'] = err_traceback
            self.err_dict['request_info'] = request_info
        self.err_dict['request_id'] = request_id
        response = JsonResponse(self.err_dict)
        return response
