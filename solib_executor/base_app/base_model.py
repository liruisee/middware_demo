from django.db import models
from base_app.exceptions import ViewException
import datetime
import json
from json.decoder import JSONDecodeError
import re


class BaseModel(models.Model):

    # 抽象模型，不然继承会有问题
    class Meta:
        abstract = True

    # 获取除id外所有的字段名，同get_columns，此方法更直观，后续建议用这个
    @classmethod
    def get_fields(cls) -> list:
        result = []
        for field in cls._meta.fields:
            field_name = field.name
            result.append(field_name)
        return result

    @classmethod
    # @lru_cache
    def get_fields_info(cls) -> dict:
        fields = cls._meta.fields
        result = {}
        for field in fields:
            name = field.name
            _type = type(field)
            help_text = field.help_text
            result[name] = {
                'type': _type,
                'help_text': help_text
            }
        return result

    @classmethod
    def trans_kwargs(cls, kwargs: dict):
        fields_info = cls.get_fields_info()
        for k, v in kwargs.items():
            if k not in fields_info:
                continue
            if k in ('is_delete', 'create_time', 'update_time'):
                continue
            # 时间格式判断
            if fields_info[k]['type'] is models.DateTimeField:
                regexp = re.compile('^\d{4}-\d{2}-\d{2}$')
                if v in ('', None):
                    kwargs[k] = None
                elif type(v) is datetime.datetime:
                    pass
                elif re.match(regexp, v) is not None:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%d')
                elif 'T' in v:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

            # 日期格式判断
            elif fields_info[k]['type'] is models.DateField:
                if v in ('', None):
                    kwargs[k] = None
                elif type(v) is datetime.datetime:
                    kwargs[k] = v.date()
                elif 'T' in v:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                else:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%d')

            # bool类型判断
            elif fields_info[k]['type'] is models.BooleanField:
                if v == '':
                    kwargs[k] = False
        return kwargs

    @classmethod
    def trans_update_kwargs(cls, kwargs: dict):
        fields_info = cls.get_fields_info()
        result = {}
        for k, v in kwargs.items():
            if k not in fields_info:
                continue
            if k in ('record_no', 'is_delete', 'create_time', 'update_time'):
                continue
            # 时间格式判断
            if fields_info[k]['type'] is models.DateTimeField:
                regexp = re.compile('^\d{4}-\d{2}-\d{2}$')
                if v in ('', None):
                    kwargs[k] = None
                elif type(v) is datetime.datetime:
                    pass
                elif re.match(regexp, v) is not None:
                    continue
                elif 'T' in v:
                    v = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ')
                else:
                    v = datetime.datetime.strptime(v, '%Y-%m-%d %H:%M:%S')

            # 日期格式判断
            elif fields_info[k]['type'] is models.DateField:
                if v in ('', None):
                    kwargs[k] = None
                elif type(v) is datetime.datetime:
                    kwargs[k] = v.date()
                elif 'T' in v:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%dT%H:%M:%S.%fZ').date()
                else:
                    kwargs[k] = datetime.datetime.strptime(v, '%Y-%m-%d')

            # bool类型判断
            elif fields_info[k]['type'] is models.BooleanField:
                if v == '':
                    v = None
            result[k] = v
        return result

    @classmethod
    def create(cls, **kwargs):
        kwargs = cls.trans_kwargs(kwargs)
        result = {}
        fields_info = cls.get_fields_info()
        if 'record_no' in fields_info:
            kwargs['record_no'] = cls.get_record_no(kwargs['project_id'])
        del fields_info['id']
        for k, v in kwargs.items():
            if k not in fields_info:
                continue
            if v is None:
                continue
            if fields_info[k]['type'] is models.IntegerField:
                try:
                    tmp = int(v)
                except (ValueError, TypeError) as e:
                    msg = f'create failed, model: {cls.__name__}, field_name: {k}, can not trans to int, the value is {repr(v)}'
                    raise ViewException(msg)
            help_text = fields_info[k]['help_text']
            if help_text.startswith('json-'):
                if v is not None:
                    v = json.dumps(v, ensure_ascii=False)
            elif help_text.startswith('enum-'):
                if v is not None:
                    tmp_dict = json.loads(help_text.split('|', 1)[1].strip())
                    if str(v) not in tmp_dict:
                        msg = f'create failed, model: {cls.__name__}, field_name: {k} is enumable, ' \
                              f'the value {repr(v)} not in keys: {list(tmp_dict.keys())}'
                        raise ViewException(msg)
            result[k] = v

        obj = cls.objects.create(**result)
        return obj

    def to_origin_dict(self):
        fields_info = self.get_fields_info()
        result = {}
        for field, field_info in fields_info.items():
            # 忽略掉是否删除字段
            if field == 'is_delete':
                continue
            # 获取字段的值
            val = getattr(self, field)
            if field_info['help_text'].startswith('json-'):
                if val is not None:
                    val = json.loads(val)
            # 记录下val
            result[field] = val
        return result

    def to_dict(self, keys: set=None):
        fields_info = self.get_fields_info()
        if keys is not None:
            assert (type(keys) is set), f'the keys type is not set, type: {type(keys)}, val: {keys}'
            fields_info = {key: fields_info[key] for key in keys if key in fields_info}
        result = {}
        ignore_key_set = {'is_delete'}
        for field, field_info in fields_info.items():
            # 忽略掉是否删除字段
            if field in ignore_key_set:
                continue
            # 获取字段的值
            val = getattr(self, field)
            # 日期的格式判定及转化
            if type(val) is datetime.datetime:
                # val = val.strftime('%Y-%m-%d %H:%M:%S')
                val = val.strftime('%Y-%m-%d')
            elif type(val) is datetime.date:
                val = val.strftime('%Y-%m-%d')
            elif field_info['help_text'].startswith('json-'):
                if val is not None and val != '':
                    val = json.loads(val)
            # 记录下val
            result[field] = val

            help_text = field_info['help_text']

            if val is None:
                if help_text.startswith('enum-') or help_text.startswith('json-'):
                    result[f'{field}_text'] = None
                    continue
            # 将枚举类型和bool值映射成text
            if field_info['type'] is models.BooleanField:
                result[f'{field}_text'] = '是' if val is True else '否'
            # 整形情况下，判定枚举
            elif field_info['type'] is models.IntegerField:
                if not help_text.startswith('enum-'):
                    continue
                msg_prefix = f'class: {self.__class__.__name__}, field_name: {field}, help_text: {help_text}'
                try:
                    tmp_dict = json.loads(help_text.split('|', 1)[1].strip())
                except (IndexError, JSONDecodeError):
                    raise Exception(f'枚举类型字段配置错误：{msg_prefix}')
                result[f'{field}_text'] = tmp_dict.get(str(val))
            elif help_text.startswith('json-'):
                if 'id' in val and 'name' in val:
                    result[f'{field}_name'] = val['name']
        return result

    def update(self, **kwargs):
        kwargs = self.__class__.trans_update_kwargs(kwargs)
        fields = set(self.get_fields()) - {'is_delete', 'create_time', 'update_time'}
        # extra_fields = kwargs.keys() - fields
        # if len(extra_fields) > 0:
        #     class_name = self.__class__.__name__
        #     raise ViewException(f'please check args, class {class_name} have no attrs {extra_fields}')

        fields_info = self.get_fields_info()
        del fields_info['id']
        for k, v in kwargs.items():
            if k not in fields_info:
                continue
            if v is None:
                continue

            if fields_info[k]['type'] is models.IntegerField:
                try:
                    tmp = int(v)
                except ValueError as e:
                    msg = f'update failed, model: {self.__class__.__name__}, field_name: {k}, can not trans to int, the value is {repr(v)}'
                    raise ViewException(msg)
            help_text = fields_info[k]['help_text']
            if help_text.startswith('json-'):
                if v is not None:
                    kwargs[k] = json.dumps(v, ensure_ascii=False)

        is_need_update = False
        for k, v in kwargs.items():
            if k in ('is_delete', 'create_time', 'update_time'):
                continue
            if v is None:
                continue
            db_attr = getattr(self, k)
            if type(db_attr) is datetime.datetime:
                db_value = db_attr.strftime('%Y-%m-%d %H:%M:%S')
            elif type(db_attr) is datetime.date:
                db_value = db_attr.strftime('%Y-%m-%d')
            else:
                db_value = db_attr
            if db_value != v:
                setattr(self, k, v)
                is_need_update = True
        if is_need_update:
            self.save()

    def __setattr__(self, key, value):
        fields_info = self.get_fields_info()
        if key not in fields_info:
            super().__setattr__(key, value)
            return
        if value is None:
            super().__setattr__(key, value)
            return

        field_type = fields_info[key]['type']
        if field_type is models.IntegerField:
            try:
                value = int(value)
            except ValueError:
                raise ViewException(f'class {self.__class__.__name__} attr {key} must be int, current is {repr(value)}')
        super().__setattr__(key, value)

    @classmethod
    def get_record_no(cls, project_id):
        objs = cls.objects.filter(project_id=project_id).order_by('-record_no')
        if not objs.exists():
            return 1
        obj = objs.first()
        record_no = obj.record_no
        return record_no + 1

