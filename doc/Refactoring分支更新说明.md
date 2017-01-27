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
