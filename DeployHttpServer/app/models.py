import logging
from flask_login import UserMixin
from . import login_manager
import salt.config
from flask import current_app


master_config = salt.config.client_config('/etc/salt/master')
upload_folder = master_config['file_roots']['base'][0]
tomcat_server_list = ['vshow-api.war', 'vshow-console.war', 'vshow-task.war', 'vshow-config.war']
im_server_list = ['VShowCenterServer', 'VShowIMServer', 'VShowRobot']
administrator_password = {'yinshuo': 'gotye2013', 'xialonghua': 'gotye2013',
                                        'zoulifeng': 'gotye2013', 'zhanglong': 'gotye2013',
                                        'admin': 'gotye2013'}


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    if username not in administrator_password:
        return
    user = User()
    user.id = username
    return user



