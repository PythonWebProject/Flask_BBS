from flask_script import Manager
from bbs import app
from flask_migrate import Migrate, MigrateCommand
from exts import db
from apps.cms.models import CMSUser, CMSRole, CMSPermission
from apps.front.models import FrontUser

manager = Manager(app)
Migrate(app, db)

manager.add_command('db', MigrateCommand)


@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
@manager.option('-e', '--email', dest='email')
def create_cms_user(username, password, email):
    user = CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print('CMS用户添加成功')


@manager.command
def create_role():
    # 访问者
    visitor = CMSRole(name='访问者', desc='只能查看数据，不能修改数据')
    visitor.permissions = CMSPermission.VISITOR  # 也可以省去，因为默认权限就是VISITOR

    # 运营者
    operator = CMSRole(name='运营', desc='管理帖子，管理评论，管理前台和后台用户')
    # 有多个权限时，使用或运算表示
    operator.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.CMSUSER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER
    # 管理员
    admin = CMSRole(name='管理员', desc='拥有本系统大部分权限')
    admin.permissions = CMSPermission.VISITOR | CMSPermission.POSTER | CMSPermission.CMSUSER | CMSPermission.COMMENTER | CMSPermission.FRONTUSER | CMSPermission.BOARDER

    # 开发人员
    developer = CMSRole(name='开发者', desc='拥有所有权限')
    developer.permissions = CMSPermission.ALL_PERMISSION

    db.session.add_all([visitor, operator, admin, developer])
    db.session.commit()
    print('角色添加成功')


@manager.command
def test_permission():
    user = CMSUser.query.first()
    if user.has_permission(CMSPermission.VISITOR):
        print('该用户有使用者权限')
    else:
        print('该用户没有使用者权限')


@manager.option('-e', '--email', dest='email')
@manager.option('-n', '--name', dest='name')
def add_user_to_role(email, name):
    user = CMSUser.query.filter_by(email=email).first()
    if user:
        role = CMSRole.query.filter_by(name=name).first()
        if role:
            role.users.append(user)
            db.session.commit()
            print('用户添加到角色添加成功')
        else:
            print('角色不存在')
    else:
        print('邮箱不存在')


@manager.option('-t', '--telephone', dest='telephone')
@manager.option('-u', '--username', dest='username')
@manager.option('-p', '--password', dest='password')
def create_front_user(telephone, username, password):
    user = FrontUser(telephone=telephone, username=username, password=password)
    db.session.add(user)
    db.session.commit()
    print('前台用户添加成功')


if __name__ == '__main__':
    manager.run()
