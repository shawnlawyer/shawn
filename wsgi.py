from flask import Flask, render_template, redirect, request, url_for, abort, jsonify, json, Markup

app = Flask(__name__,'/')


@app.route('/',methods = ['GET'])
def home():
    return "hello"

@app.before_request
def before_request():
    pass

@app.after_request
def after_request(response):
    return response

def run_app(app, log=False, debug=False):

    app.run(debug=debug, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run_app(app, True, True)


