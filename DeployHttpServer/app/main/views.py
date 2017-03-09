# -*- coding: utf-8 -*-

import os
from flask import request, redirect, url_for, render_template, flash
from werkzeug.utils import secure_filename
from ..CreateInitFile import tomcat_init_data, im_init_data, FindInitFileName,\
    CreateTomcatInitFile, CreateImInitFile
from ..DataStructureTool import ClearDictNullValue, DictValueBooleanToStr,\
    NoDuplicateList, UpdateDicData
from ..SaltStackHandle import FileFind, FileDeploy, FileBackup, ChmodFile, RestartServer
import flask_login
from . import main
from .. import login_manager
from ..models import upload_folder, tomcat_server_list, im_server_list, administrator_password, User
from flask import current_app


@login_manager.unauthorized_handler
def unauthorized_handler():
    current_app.logger.info('unauthorized [open_unauthorized_handler]')
    return redirect(url_for('main.login'))


@main.route('/cleanfile', methods=['POST'])
@flask_login.login_required
def cleanfile():
    current_app.logger.info('%s [open_cleanfile]' % flask_login.current_user.id)
    if request.method == 'POST':
        allfiles = current_app.all_files_list
        if not allfiles:
            flash('no file need clean')
        for each_file in current_app.all_files_list:
            os.remove(os.path.join(upload_folder, each_file))
        current_app.all_files_list = []
        current_app.deploy_files_list = []
        current_app.backup_result = []
        current_app.deploy_result = []
        current_app.restart_server_result = []
        flash('Clean All Files.')
        current_app.logger.info('%s [cleanfile]' % flask_login.current_user.id)
    return redirect(url_for('main.uploadfile'))


@main.route('/chosefile', methods=['GET', 'POST'])
@flask_login.login_required
def chosefile():
    current_app.backup_result = []
    current_app.deploy_result = []
    current_app.restart_server_result = []
    current_app.logger.info('%s [open_chosefile]' % flask_login.current_user.id)
    if request.method == 'POST' or request.method == 'GET':
        files = request.values.getlist("uploadboxvalue")
        for each in files:
            filedic = FileFind(each)
            # print filedic
            filedic = ClearDictNullValue(filedic)
            current_app.logger.info('%s:%s [chosefile]' % (flask_login.current_user.id, filedic))
            current_app.deploy_files_list.append(filedic)
        current_app.deploy_files_list = NoDuplicateList(current_app.deploy_files_list)
        # print deploy_files_list
        return render_template('ChoseFile.html', data=current_app.deploy_files_list)


@main.route('/deployfile', methods=['GET', 'POST'])
@flask_login.login_required
def deployfile():
    current_app.logger.info('%s [open_deployfile]' % flask_login.current_user.id)
    if request.method == 'POST':
        files = request.values.getlist("deployboxvalue")
        for each in files:
            each = each.split(' ')
            hostname = each[0]
            s_filepath = each[1]
            d_filepath = each[2]
            result = FileBackup(hostname, s_filepath, d_filepath, if_remove_source=True)
            if result.values()[0] is True:
                # {'ip-10-0-0-237.cn-north-1.compute.internal': (u'/tmp/ceshi2', True)}
                result = DictValueBooleanToStr(result, d_filepath)
                current_app.logger.info('%s:%s [backupfile]' % (flask_login.current_user.id, result))
                current_app.backup_result.append(result)
                result = FileDeploy(hostname, s_filepath, d_filepath)
                ChmodFile(hostname, d_filepath)
                UpdateDicData(result, s_filepath)
                # print result
                current_app.logger.info('%s:%s [deployfile]' % (flask_login.current_user.id, result))
                current_app.deploy_result.append(result)
            else:
                flash('error: ' + result)
                current_app.logger.info('error: ' + result)
                current_app.backup_result.append(result)
        current_app.backup_result = NoDuplicateList(current_app.backup_result)
        current_app.deploy_result = NoDuplicateList(current_app.deploy_result)
        return render_template('DeployFile.html', backup_data=current_app.backup_result,
                               deploy_data=current_app.deploy_result)
    return render_template('DeployFile.html', backup_data=current_app.backup_result,
                           deploy_data=current_app.deploy_result)


@main.route('/restartserver', methods=['GET', 'POST'])
@flask_login.login_required
def restartserver():
    current_app.logger.info('%s [open_restartserver]' % flask_login.current_user.id)
    # restart_server_result = []
    if request.method == 'POST':
        data = request.values.getlist("restartboxvalue")
        for each in data:
            each = each.split(' ')
            hostname = each[0]
            deploy_file_name = each[1]
            deploy_file_path = each[2]
            if deploy_file_name in tomcat_server_list or \
                FindInitFileName(deploy_file_name) in tomcat_server_list:
                restartserver_name = CreateTomcatInitFile(tomcat_init_data,
                                                    deploy_file_name, deploy_file_path,
                                                    upload_folder)
            elif deploy_file_name in im_server_list or \
                FindInitFileName(deploy_file_name) in im_server_list:
                restartserver_name = CreateImInitFile(im_init_data,
                                                    deploy_file_name, deploy_file_path,
                                                    upload_folder)
            else:
                restartserver_name = False
                result =False
                flash('"%s" not in app.config[SERVER_LIST]' % deploy_file_name)
                current_app.logger.info('%s:%s not in app.config[SERVER_LIST]' %
                                (flask_login.current_user.id, deploy_file_name))
            if restartserver_name:
                FileDeploy(hostname, restartserver_name,
                            os.path.join('/etc/init.d', restartserver_name))
                ChmodFile(hostname, os.path.join('/etc/init.d', restartserver_name))
                result = RestartServer(hostname, restartserver_name)
                print result
            if result:
                current_app.logger.info('%s:%s [restartserver]' % (flask_login.current_user.id, result))
                current_app.restart_server_result.append(result)
                os.system('rm -f %s' % os.path.join(upload_folder, restartserver_name))
        restart_server_result = NoDuplicateList(current_app.restart_server_result)
        print restart_server_result
        return render_template('RestartServer.html', restart_data=current_app.restart_server_result)
    return render_template('RestartServer.html', restart_data=current_app.restart_server_result)


@main.route('/uploadfile', methods=['GET', 'POST'])
@flask_login.login_required
def uploadfile():
    current_app.logger.info('%s [open_uploadfile]' % flask_login.current_user.id)
    current_app.deploy_files_list = []
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            current_app.logger.info('%s:nofilepart [uploadfile]' % flask_login.current_user.id)
            return redirect(request.url)
        file = request.files['file']
        files = request.files.getlist('file')
        if file.filename == '':
            flash('no selected file')
            current_app.logger.info('%s:noselectedpart [uploadfile]' % flask_login.current_user.id)
            return redirect(request.url)
        if file:
            for file in files:
                filename = secure_filename(file.filename)
                file.save(os.path.join(upload_folder, filename))
                current_app.logger.info('%s:%s [uploadfile]' % (flask_login.current_user.id, filename))
            return redirect(url_for('main.uploadfile'))
    allfiles = os.listdir(upload_folder)
    current_app.all_files_list = allfiles
    return render_template('UploadFile.html', data=current_app.all_files_list)


@main.route('/', methods=['GET', 'POST'])
@main.route('/login', methods=['GET', 'POST'])
def login():
    current_app.logger.info('unauthorized [open_login]')
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username not in administrator_password:
            error = 'Invalid username'
            current_app.logger.info('%s [InvalidUser]' % username)
        elif password != administrator_password[username]:
            error = 'Invalid password'
            current_app.logger.info('%s:%s [InvalidUserPassword]' % (username, password))
        else:
            user = User()
            user.id = username
            flask_login.login_user(user)
            flash('%s, login' % username)
            current_app.logger.info('%s [login]' % username)
            current_app.logger.info('[%s:%s]' % (username, password))
            return redirect(url_for('main.uploadfile'))
    return render_template('Login.html', error=error)


@main.route('/logout')
@flask_login.login_required
def logout():
    flash('%s, logout' % flask_login.current_user.id)
    current_app.logger.info('%s [logout]' % flask_login.current_user.id)
    flask_login.logout_user()
    current_app.all_files_list = []
    current_app.deploy_files_list = []
    current_app.backup_result = []
    current_app.deploy_result = []
    current_app.restart_server_result = []
    return redirect(url_for('main.login'))






