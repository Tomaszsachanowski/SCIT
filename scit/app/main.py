import random 

import requests
from flask import Flask, Response
from flask import Flask, session, render_template, request, redirect, url_for


SES = requests.Session()

app = Flask(__name__)

SITE_NAMES = ["http://172.24.2.1:5000", "http://172.24.2.2:5000", "http://172.24.2.3:5000"]


@app.route('/')
def main():
    print(f"{SITE_NAMES[random.randint(0, 2)]}{'/'}")
    resp = SES.get(f"{SITE_NAMES[random.randint(0, 2)]}")
    return Response(
        resp.text,
        status=resp.status_code,
        content_type=resp.headers['content-type'])


@app.route('/add', methods=['POST'])
def add():
    SES.post(f"{SITE_NAMES[random.randint(0, 2)]}{'/add'}", json=request.get_json(), data=request.form)
    return redirect(url_for('.main'))


@app.route('/delete/<string:code>', methods=['GET'])
def delete(code):
    print(f"{SITE_NAMES[random.randint(0, 2)]}{'/delete/'}{code}")
    SES.get(f"{SITE_NAMES[random.randint(0, 2)]}{'/delete/'}{code}")
    return redirect(url_for('.main'))


@app.route('/empty', methods=['GET'])
def empty():
    SES.get(f"{SITE_NAMES[random.randint(0, 2)]}{'/empty'}")
    return redirect(url_for('.main'))


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
