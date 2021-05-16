from base_app.base_view import BaseView
from django.core.handlers.wsgi import WSGIRequest
from base_app.responses import JsonResponse
import json
from executors.rule_parser_util import RuleParser


class RuleParse(BaseView):

    def post(self, request: WSGIRequest):
        body = json.loads(request.body)
        rp = RuleParser()
        bodys = rp.render_rule_to_body(body)

        result = {
            'result': bodys,
            'message': 'success',
            'status': 200
        }
        return JsonResponse(result)
