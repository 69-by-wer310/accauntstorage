from flask import Flask, request, redirect, render_template, jsonify, Response
import requests as r
import json
import uuid
about_codes = {}
app = Flask(__name__)
@app.route("/login/auth", methods=["GET"])
def login():
    try:
        url = request.args["redirect_uri"]
    except KeyError:
        return redirect("/docs#redirect-to-accauntstorage-login")
    return render_template("login.html", url=url)
@app.route("/login", methods=["POST"])
def loginin():
    try:
        if not r.post("https://hcaptcha.com/siteverify", data={"secret": "0x9f8F29098309A81b6DE1D384C651557dE6262861", "response": request.form["h-captcha-response"]}).json()["success"]: return redirect("/login/auth?redirect_uri=" + request.args["url"])
    except KeyError:
        return redirect("/login/auth?redirect_uri=" + request.args["url"])
    f = open("db/accaunts.json", "r")
    wering = json.load(f)
    f.close()
    try:
        if request.form["password"] == wering[request.form["username"]]["password"]:
            wer = wering[request.form["username"]]
            del wer["password"]
            code = str(uuid.uuid4())
            about_codes[code] = wer
            return redirect(request.args["url"] + code)
        else:
            return redirect("/login/auth?redirect_uri=" + request.args["url"])
    except KeyError:
        wering[request.form["username"]] = {"id": str(uuid.uuid4()), "username": request.form["username"], "password": request.form["password"]}
        f = open("db/accaunts.json", "w")
        json.dump(wering, f)
        f.close()
        wer = wering[request.form["username"]]
        del wer["password"]
        code = str(uuid.uuid4())
        about_codes[code] = wer
        return redirect(request.args["url"] + code)
@app.route("/api/v1/about/<string:about_code>", methods=["GET"])
def api_v1_about(about_code):
    try:
        about = about_codes[about_code]
    except KeyError:
        return redirect("/docs#using-adout-code")
    del about_codes[about_code]
    return jsonify(ok=True,user=about)
@app.route("/docs")
def docs_site():
    return render_template("docs.html")
@app.route("/")
def index():
    return render_template("index.html")
@app.route("/robots.txt")
def robots():
 return """
    user-agent: *
    allow: /
    allow: /docs
    allow: /exemple
    deallow: /login
    deallow: /login/*
    deallow: /robots.txt
    deallow: /favicon.ico
    deallow: /api/*
"""
@app.route("/exemple")
def exemple():
    response = redirect("/login/auth?redirect_uri=/exemple/end_url?code=")
    return response
@app.route("/exemple/end_url")
def exemple_end_url():
    data = r.get("http://" + request.headers["Host"] +"/api/v1/about/" + request.args["code"]).json()["user"]
    return """
        your ID: %s</br>
        your username: %s
    """ % (data["id"], data["username"])
@app.route("/yandex_3872704e789fd33b.html")
def yandex_3872704e789fd33b():
    return """
        <html>
            <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
            </head>
            <body>Verification: 3872704e789fd33b</body>
        </html>
    """


app.run(port=80, debug=True, host="")
