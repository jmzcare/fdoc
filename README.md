## MrDoc - 记录文档，汇聚思想

![Mrdoc首页](./captrue/mrdoc-index.png)

## 介绍

`MrDoc`是基于`Python`开发的在线文档系统，适合作为个人和小型团队的文档、知识和笔记管理工具。

### 特性：

- 简洁的站点与用户系统
    - 支持用户注册、用户登录、用户管理、管理员等控制等功能；
    - 支持全站关闭注册；
    - 支持注册邀请码配置；
    - 支持广告位自定义配置；
    - 支持统计代码自定义配置；
    
- 结构清晰地文档系统
    - 基于文集的文档撰写和阅读；
    - 使用基于`Editormd`的`Markdown`编辑器并扩展，以`Markdown`语法进行文档写作；
    - 提供文档模板功能，支持文档模板的创建、修改；
    - 两栏式文档阅读页面，支持文档阅读页面的字体缩放，字体类型修改，页面社交分享，良好的移动端阅读体验；
    - 支持三级目录层级显示；
    - 支持文集后台导出为`markdown`文本格式`.md`文件、前台导出为`EPUB`等格式文件；
    - 基于文集进行权限控制，提供公开、私密、指定用户可见、访问码可见4种权限模式；
    - 支持基于账户的`API`接口，可以借助账户`token`通过`API`获取文集、上传图片和创建文档；
    - 支持文集协作功能，一个文集可以拥有一个创建者和多个协作者，可灵活选择协作权限；
    - 支持附件上传和管理、图片上传和管理；

当前版本为：**v0.4**，版本发布时间为**2020-04-06**

完整更新记录详见：[CHANGES.md](./CHANGES.md)

在开发过程中，参考和借鉴了GitBook、ShowDoc、Wordbook等应用和网站的功能与样式，并使用了众多开源组件、插件。

## 应用核心依赖环境

MrDoc基于Python语言的Django Web框架配合前端的LayUI、JQuery等库进行开发。

后端环境推荐使用Python3.4+、Django2.1+的版本。

## 安装简明教程

### 1、安装依赖库
```
pip install -r requirements.txt
```

### 2、配置数据库信息

默认情况下，MrDoc使用Django的SQLite数据库，如果你使用Sqlite数据库，则无需另外配置数据库。

如果有配置其他数据库的需求，请在/MrDoc/MrDoc目录下打开settings.py文件，在约80行的位置，将如下代码：
```
DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.sqlite3',
 'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
 }
}
```
按照自己数据库的信息，将其修改如下格式，下面以MySQL为例：
```
DATABASES = {
 'default': {
 'ENGINE': 'django.db.backends.mysql', # 使用的数据库后端
 'NAME': 'mrdoc', # 数据库名
 'USER':'root', # 数据库用户
 'PASSWORD':'123456789', # 数据库用户密码
 'HOST':'', # 数据库主机地址
 'PORT':'3306', # 数据库端口
 }
}
```
### 3、初始化数据库

在安装完所需的第三方库并配置好数据库信息之后，我们需要对数据库进行初始化。

在项目路径下打开命令行界面，运行如下命令生成数据库迁移：
```
python manage.py makemigrations
```
接着，运行如下命令执行数据库迁移：
```
python manage.py migrate
```
执行完毕之后，数据库就初始化完成了。

### 4、创建管理员账户
在初始化完数据库之后，需要创建一个管理员账户来管理整个MrDoc，在项目路径下打开命令行终端，运行如下命令：
```
python manage.py createsuperuser
```
按照提示输入用户名、电子邮箱地址和密码即可。
### 5、测试运行
在完成上述步骤之后，即可运行使用MrDoc。

在测试环境中，可以使用Django自带的服务器运行MrDoc，其命令为：
```
python manage.py runserver
```

## 使用说明文档

详见MrDoc使用文档: [http://mrdoc.zmister.com](http://mrdoc.zmister.com)

## 问题提交和反馈

### 1、提交issue

直接在[https://gitee.com/zmister/MrDoc/issues](https://gitee.com/zmister/MrDoc/issues) 页面提交问题。

### 2、加入MrDoc交流群

加入MrDoc交流QQ群，群号为**735507293**，入群密码：**mrdoc**


## 更多应用截图

### 文集浏览页面
![MrDoc文集页面](./captrue/mrdoc-project-index.png)

### 文档阅读页面
![MrDoc文档页](./captrue/mrdoc-doc.png)

### 文档编写页面
![](./captrue/mrdoc-create-doc.png)

### 普通用户个人中心
![MrDoc普通用户后台](./captrue/mrdoc-manage-project.png)

### 管理员后台页面
![MrDoc管理员后台](./captrue/mrdoc-admin-register-code.png)

### 登录页面
![MrDoc登录页](./captrue/mrdoc-login.png)

### 注册页面
![MrDoc注册页](./captrue/mrdoc-register.png)
