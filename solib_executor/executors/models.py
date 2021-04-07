from base_app.base_model import BaseModel
from django.db import models


class TestCaseBody(BaseModel):
    id = models.AutoField(help_text='自增主键', primary_key=True)
    body = models.TextField(max_length=40960, help_text='json-用户传的原始请求参数，规则未被解析')


class MiddlewareTestCase(BaseModel):

    id = models.AutoField(help_text='自增主键', primary_key=True)
    file_id = models.CharField(max_length=256, help_text='文件id')
    test_case_body_id = models.IntegerField(help_text='原始body id')
    code_file_path = models.CharField(max_length=512, help_text='存储代码的文件路径')
    header_file_names = models.CharField(max_length=1024, help_text='json-依赖的头文件列表')
    cxx_flags = models.CharField(max_length=1024, help_text='编译时需要的c++参数')
    middleware_name = models.CharField(max_length=1024, help_text='中间件名称，基本为库名')
    class_name = models.CharField(max_length=1024, null=True, help_text='类名，中间件中的类')
    method_name = models.CharField(max_length=1024, help_text='函数名或类成员对应的方法名')
    args = models.CharField(max_length=1024, help_text='json-函数名或类成员对应的方法名')
    return_type = models.CharField(max_length=1024, help_text='json-函数名或类成员对应的方法名')
    build_result = models.CharField(max_length=1024, help_text='编译阶段的结果')
    exec_result = models.CharField(max_length=1024, help_text='执行阶段的结果')
