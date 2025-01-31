from django.db import models
import ast

# Create your models here.
class ListField(models.TextField):
#    __metaclass__ = models.SubfieldBase
    description = "Stores a python list"

    def __init__(self, *args, **kwargs):
        super(ListField, self).__init__(*args, **kwargs)


    def from_db_value(self, value, expression, connection, context):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)


    def to_python(self, value):
        if not value:
            value = []

        if isinstance(value, list):
            return value

        return ast.literal_eval(value)

    def get_prep_value(self, value):
        if value is None:
            return value

        # use str(value) in Python 3
        return str(value)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


class Record(models.Model):
    airline_code2 = models.TextField()
    lon = models.FloatField()
    _id = models.TextField()
    airport_icao_code = models.TextField()
    num5 = models.IntegerField()
    typecode = models.TextField()
    first_in = models.FloatField()
    airline_code1 = models.TextField()
    lat = models.FloatField()
    flight = models.TextField()
    height = models.IntegerField()
    num3 = models.IntegerField()
    airport_dep = models.TextField()
    timestamp = models.TextField()
    idshex = models.TextField()
    str1 = models.TextField()
    num2 = models.IntegerField()
    last_modify = models.FloatField()
    zone_range = ListField(default=[])
    airport_arr = models.TextField()
    num1 = models.IntegerField()
    num4 = models.IntegerField()
    fid = models.TextField()

    def __init__(self,record):
        super(Record, self).__init__()
        #record的所有属性
        #attrs = ['airline_code2','lon','_id','airport_icao_code','num5','typecode','first_in','airline_code1','lat','flight','height','num3','airport_dep','timestamp','idshex','str1','num2','last_modify','zone_range','airport_arr','num1','num4','fid']
        for attr in [x for x in dir(self) if x in record.keys()]:
            # 利用record中有的数据初始化属性值
            self.__dict__[attr] = record[attr]


    def from_db(cls, db, field_names, values):
        record = dict()
        for index in range(0,len(field_names)):
            record.update({field_names[index]:values[index]})
        new = cls(record)
        new._state.adding = False
        new._state.db = db
        return new

