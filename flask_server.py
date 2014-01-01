import boto
import boto.s3
from boto.s3.key import Key

from flask import Flask
app = Flask(__name__)

@app.route("/", methods=["POST"])
def save():
    _write_string_to_s3('secrets/secret_list', 'secretswoo')
    return "Hello World!"

def _write_string_to_s3(key_path, write_str):
    conn = boto.connect_s3()
    bucket = conn.get_bucket('secrets.epton.org')
    k = Key(bucket)
    k.key = key_path
    k.set_contents_from_string(write_str)
    k.make_public()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
