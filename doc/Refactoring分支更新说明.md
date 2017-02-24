##V1.3说明
完成了index页面和airline页面的重构，现在需要在本地看修改效果的话，可以在文件夹下运行如下命令：

    python manage.py runserver
然后在提示的端口下访问即可  
同时希望写前端的同学注意几点：  
* 静态资源，包括js文件，css文件以及图片等文件都放在Map/static相应的文件夹下
* 如果要添加新的页面，在html文档中写完链接后告诉我或者别的写后端的同学，以便添加相应的后端逻辑
* 如果要使用本地数据的话，也请大家使用ajax请求数据，不要直接写死在代码中

##V1.5说明
完成了数据库的模型部分，修改了页面中的数据请求方式

**注意**：因为数据库模型的修改，需要在本地对应的django包(位置通常为(python3的路径)\Lib\site-packages\django\db\models)中做相应的修改如下：
将query.py中**ModelIterable**类中的**\_\_iter\_\_**方法中的调用代码

	obj = model_cls.from_db(db, init_list, row[model_fields_start:model_fields_end])

修改为如下代码：

	obj = model_cls.from_db(model_cls,db, init_list, row[model_fields_start:model_fields_end])

##V1.5.2说明
尝试使用django-crontab库完成定时更新数据库的任务，但由于这个库无法在windows上使用，所以暂时放弃这个方案，考虑使用celery完成定时任务。
另外添加了自定义命令`getrealtimedata`来实现获取实时数据并插入到数据库，现在只需要运行`python manage.py getrealtimedata`就可实现数据的更新。

## V1.5.4说明
修复了model中Record对象的init方法错误，现在数据库可以使用only方法了。