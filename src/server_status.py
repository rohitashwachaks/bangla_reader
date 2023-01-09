from flask import Blueprint, render_template

server_status = Blueprint('server_status', __name__)

@server_status.route('/')
def hello():
    return 'Hello, World!'


@server_status.route('/health-check/', methods=['GET'])
def health_check():
    return 'Everything working well'
