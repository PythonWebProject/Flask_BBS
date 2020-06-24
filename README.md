### 安装环境依赖
在克隆或下载项目后，在项目目录下执行`pip install -r requirements.txt`命令安装项目所需库。

### 项目版本
#### V1.0
项目整体目录框架搭建完毕，后台管理员模型创建完成，实现命令行添加用户，后台登录页面实现。

#### V1.1
在V1.0的基础上进一步实现CMS用户登录、错误信息返回、登录限制和CSRF保护、CMS用户名渲染和注销、CMS个人页面和模板抽离等功能，进一步丰富后台管理功能。

#### V1.2
在V1.1的基础上实现后台修改密码布局、通过Ajax实现局部更新修改密码、优化Json数据返回、sweetalert美化提示框、修改邮箱界面搭建功能。

#### V1.3
在V1.2的时候进一步完善，首先实现在Flask中发送邮件，并进一步定义发送验证码，并进一步实现修改邮箱，还对权限和角色模型进行了定义。

注意：
在配置文件config.md中需要将自己的邮箱信息输入，才能正常实现其功能。

#### V1.4
在V1.3的基础上进一步完善权限验证功能，首先在manage.py中实现添加用户角色，再实现页面修改，最后在客户端和服务端进行双重权限验证，是吸纳了权限验证的基本功能。

#### V1.5
这一版本开始进入前台开发阶段，首先定义前台的用户模型，并在此基础上搭建前台注册页面和完成图形验证码类，再实现点击更换图形验证码的功能，接下来实现发送短信验证码的功能，并实现短信验证码接口的MD5加密和JS加密代码的加密。