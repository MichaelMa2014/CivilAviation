from django.core.management.base import BaseCommand, CommandError
from urllib import request
from json import loads
from Map.models import Record

class Command(BaseCommand):
    help = 'Get real time data'

    def handle(self, *args, **options):
        data = request.urlopen(url='http://219.224.134.225:5050/real-time')
        dataList = loads(data.read().decode('utf-8'))
        cnt = 1
        for item in dataList:
            newRecord = Record(item)
            try:
                newRecord.save()
                cnt += 1
            except:
                self.stderr.write("A Record failed to be saved")

        self.stdout.write(str(cnt) + " Record(s) has been saved")