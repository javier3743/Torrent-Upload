from flask import Flask, request
from flask import render_template
from flask import jsonify, make_response
import datetime
import psycopg2
import urllib.parse as urlparse
import os

url = urlparse.urlparse(os.environ['DATABASE_URL'])
dbname = url.path[1:]
user = url.username
password = url.password
host = url.hostname
port = url.port

conn = psycopg2.connect(
            dbname= dbname,
            user= user,
            password= password,
            host= host,
            port= port
            )


app = Flask(__name__)

@app.route('/')
def homepage():
    return """<h1>Hello Mate</h1>"""

@app.route('/post', methods = ['POST'])
def datamanager():
    data = request.get_json(force=True)
    time = '{:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
    user =  data.get("users")
    os = data.get('kernel')
    mem = data.get('mem free')
    swap = data.get('swap so')
    cpu = data.get('cpu sy')
    size = data.get('Disk Size')
    free = data.get('Free Disk Space')
    curP = conn.cursor()
    curP.execute("""INSERT INTO monitoring VALUES('"""+ time + """ ' , '""" + user + """ ' , '""" + os + """ ' , ' """
                 + mem + """  ' , ' """ + swap + """ ' , ' """ + cpu + """ ' , ' """ + size + """ ' , ' """
                 + free + """ ')""")
    curP.execute(""" COMMIT """)

    return "funca"
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, port = 5001)
