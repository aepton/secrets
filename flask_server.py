import boto
import boto.s3
from boto.s3.key import Key

import hashlib
import json

from flask import Flask, request
app = Flask(__name__)


@app.route("/", methods=["POST"])
def save():
    secret_list = 'secrets/secret_list'
    name = _get_filename_from_message(request.form['secret'])
    _write_string_to_s3('secrets/%s' % name, request.form['secret'])
    try:
        existing_list = json.loads(_get_string_from_s3(secret_list))
    except:
        existing_list = []
    existing_list.append(name)
    _write_string_to_s3(secret_list, json.dumps(existing_list))
    return "completed"


def _get_filename_from_message(message):
    m = hashlib.md5()
    m.update(message)
    return m.hexdigest()


def _get_string_from_s3(key_path):
    k = _get_key_from_keypath(key_path)
    return k.get_contents_as_string()


def _write_string_to_s3(key_path, write_str):
    k = _get_key_from_keypath(key_path)
    k.set_contents_from_string(write_str)
    k.make_public()


def _get_key_from_keypath(key_path):
    conn = boto.connect_s3()
    bucket = conn.get_bucket('secrets.epton.org')
    k = Key(bucket)
    k.key = key_path
    return k

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
