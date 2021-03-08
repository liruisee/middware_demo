from django.http import JsonResponse
from functools import partial


JsonResponse = partial(JsonResponse, json_dumps_params={'ensure_ascii': False, 'indent': 2})


def create_success_response(**kwargs):
    result = {
        'message': 'create success',
        'status': 201,
        **kwargs
    }
    response = JsonResponse(result)
    return response


def update_success_response(**kwargs):
    result = {
        'message': 'update success',
        'status': 202,
        **kwargs
    }
    response = JsonResponse(result)
    return response


def delete_success_response(**kwargs):
    result = {
        'message': 'delete success',
        'status': 204,
        **kwargs
    }
    response = JsonResponse(result)
    return response
