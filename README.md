# moyanlishang
[moyanlishang](https://github.com/moyanlishang/moyanlishang)现在开源，并托管在github上。希望大家可以多多交流~~

一、启动项目


1. 配置开发环境

首先你需要安装python2.7.11环境。下面的命令都是在Ubuntu16.04开发环境执行的，如果你使用的是Windows请留意安装命令的区别。

$sudo apt-get install python

安装使用虚拟环境
$sudo apt-get install python-virtualenv

现在你需要下载示例代码
$git clone https://github.com/moyanlishang/moyanlishang.git

在源码中创建虚拟环境
cd code
virtualenv venv

激活虚拟环境
source venv/bin/activate

在虚拟环境中安装依赖库
$sudo pip install -r requirements.txt （此版本使用的Flask版本是0.10版，如果你使用的是0.11版，会有所不同，详情请参考 http://codingpy.com/article/flask-just-upgraded-to-0.11/ ）

配置好run.sh中的环境变量，在命令行中使用sudo执行，权限不足，可以使用chmod命令来给run.sh添加执行权限。这时候系统已经保存有这些环境变量了。为了保护你的隐私请不要在config.py文件直接配置。

2. 数据库迁移

删除源码中的 migrations 文件夹和sqllite文件 

迁移工程初始化
python manage.py db init

生成迁移脚本
$python manage.py db migrate -m "init version"

该命令会显式创建数据库表，同时运行迁移脚本，迁移数据库
python manage.py db upgrade

3.新建角色（本博客系统实现了简单的权限管理，所以必须显式的建立权限角色，否则会出现绑定角色失败，用户只能沦为无权限状态）

$python manage.py shell

>>> Role.insert_roles()
>>> Role.query.all()
[<Role u'Moderator'>, <Role u'Administrator'>, <Role u'User'>]
>>>

建立一个初始的超级管理员，步骤如下：

$python manage.py shell

>>> u = User(username='Bevis', email='*****@**.com', role=Role.query.filter_by(name='Administrator').first(), password='***')

>>> u.generate_avatar_url()

>>> u
<User 'Bevis'>

>>> db.session.add(u)
>>> db.session.commit()
现在你只需要完成邮件验证就好了，也可以通过后台数据库操作。

此博客实现了匿名评论功能，你需要主动的添加一个匿名用户，如果没有设置，系统会报异常来提示。

$python manage.py shell

>>> User.insert_Anonymous()

4.运行服务器

$python manage.py runserver


二、在shell环境中使用flask和数据库

键入命令后，后台模板会自动把app实例、sqlalchemy实例、数据库定义自动的加载到shell中，你可以在其中自由做测试，或者手动添加、修改数据库等。博客建立的所有模型，在这个交互环境中都有映射。

$python manage.py shell

>>> app

<Flask 'app'>

>>> db

<SQLAlchemy engine='sqlite:////home/moyanlishang/moyanlishang/code/data-dev.sqlite'>


三、使用数据库迁移工具

数据库迁移已经建立了一个基本版本，如果需要更新数据库模型，如果移动到新的部署环境，可以直接运行下面命令来同步数据库。也就是说如果初次建立后，如果更新了数据库模型，那么你可以使用如下命令来更新数据库，一个是生成迁移脚本，一个执行升级功能，但是需要注意新增表和属性好办，如果删除了现有的表和属性，那么你得手动处理migrate命令生成的脚本是否正确。

$python manage.py db migrate
$python manage.py db upgrade


四、修改配置文件

该结构框架提供了灵活的修改模式，如果添加一些配置项，可以添加在Config类中，如果想在生产环境和开发、测试环境使用不同的参数，需要在扩展类中进行修改，不过最通用的参数使用系统的环境变量。

这时一个从环境变量中引用密钥的例子，or的作用是在环境变量不起作用时，拥有替代方案。

import os

SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess'
在配置文件可以同代项app.config字典中添加键值对，满足flask扩展库和全局通用量的需要，这些代码应写在如下：

    @staticmethod

    def init_app(app):

        # you should write here

        pass
也就是说，我们的SECRET_KEY和DATABASE_URL默认从环境变量中引用，否则就使用默认字符串，或者在本地目录新建、寻找数据库。

同时我们还在Config中添加了，如下几个字段，用于配置生产环境时候。

    HOST = 'blog.liketobe.cn'
    PORT = 8080
    ACCESSIPS = '127.0.0.1'


五、增加模型

数据模型文件存在app目录下，添加数据模型很简单，只需要按照按照例子添加一个类就可以了，后台会自动完成，同时若想学习更多的SQLalchemy的ORM操作，可以访问SQLAlchemy官网来获取资源。

# test model

@addModel

class System(db.Model):

    name = db.Column(db.String(64), primary_key=True)

    def __repr__(self):

        return '<System %r>' % self.name
		

六、模板与静态文件

flask会自动分发和处理对于static下的静态文件，一般包括css样式、js脚本、img图片等等。

templates目录下是所有的模板文件，由程序控制渲染展示给用户，这些都是flask的基础知识，这里不阐述，需要说明的是，我们提供了一个默认的根目录的模板index.html，还有常见错误类型404.html、500.html。如果想换成自己的样式，必须进行替换和更改，同时不影响你的其他创作。



七、添加新的路由映射

模板提供了一个index路由的例子，可以先复制直接修改使用。值得提醒的是，可以把errors文件夹删除，因为他们定义的是全局的错误路由处理，主要修改的是views.py脚本，如果需要增加新的类声明的，在该文件夹下进行，最后当然需要在init.py中修改蓝图的名字，记得与包文件名一致，这些都是好的编码习惯哦。



八、自动生成配置文件

使用python直接负责后台可能会有弊端，一般构造一个生产环境，现在是一个比较简单的，它会生成nginx和uwsgi的配置文件，这都是自动的，然后分别把配置文件放到相应的目录即可。更重要的是在其中会执行pip的依赖库备份，还有自动迁移和更新数据库。

    # 利用bash命令删除所有的xml 和 conf文件，这些就是nginx和uwsgi的配置文件
    os.system('rm *-nginx.conf')
    os.system('rm *-uwsgi.xml')
    # 执行数据迁移和更新
    os.system('python manage.py db migrate')
    os.system('python manage.py db upgrade')
    # 执行角色更新
    Role.insert_roles()
    # 自动更新需求库
    os.system('pip freeze > requirements.txt')
命令执行如下：

$python manage.py conf
执行上述命令就会发现在本地目录出现一个*-nginx.conf和*-uswgi.xml两个文件，现在你需要电脑安装好这两个程序，一个是反向代理服务器nginx，另一个是python的通用网关接口uwsgi。安装命令如下：

$sudo apt-get install nginx
$sudo apt-get install uwsgi
把****-nginx.conf移动到nginx的配置文件，并且重新加载nginx的配置。

$sudo cp ./****-nginx.conf /etc/nginx/con.f/
$sudo /usr/sbin/nginx -s reload
启动uwsgi服务器，并手动设置log文件。

$sudo uwsgi -x ****-uwsgi.xml -d ./****.log
这样就简单搭建了生产环境。

我们提供了run.sh和exit.sh的脚本，用于自动运行和退出。如果有必须，可以使用chmod命令来给run.sh、exit.sh添加执行权限。



九、添加新的库

在开发中往往需要添加新的库，请大家自行进入虚拟环境中，使用pip安装。

如果安装了新的库，记得更新一下依赖库列表。运行如下命令。

$pip freeze > requiremwnts.txt
