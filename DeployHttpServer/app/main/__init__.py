from flask import Blueprint
import logging

main = Blueprint('main', __name__)
main.all_files_list = []
main.deploy_files_list = []
main.backup_result = []
main.deploy_result = []
main.restart_server_result = []

from . import views
