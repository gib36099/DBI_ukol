#!/usr/bin/env python3

from flask import Flask, render_template, session, redirect, request, url_for, flash
import os
import functools

app = Flask(__name__)
app.secret_key = b'\xb42\xc7\xd5:\xfa\xdcS\xf5`I1\x8f! \xefK\xec\x89\xaf\x1c\x1e/\xf2'

############################################################################

slova = ("Super", "Perfekt", "Úža", "Flask")


def prihlasit(function):
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        if "user" in session:
            return function(*args, **kwargs)
        else:
            return redirect(url_for("login", url=request.path))

    return wrapper


############################################################################


@app.route("/login/", methods = ['GET'])
def login():
    return render_template('login.html.j2')


@app.route("/login/", methods = ['POST'])
def login_post():
    login = request.form.get('login')
    passw = request.form.get('passw')
    if 'login' in session:
        flash('Už jsi přihlášen jako {}'.fromat(session['login']) )
        return redirect(url_for('index'))
    if login=='Admin' and passw=='heslo123':
        session['login'] = login
        flash('Úspěšné přihlášení')
        return render_template("base.html.j2")
    else:
        flash('Špatné heslo')
    return redirect(url_for('login'))


@app.route("/")
def index():
    if 'login' in session:
        return render_template("base.html.j2")
    else:
        flash('Nejdřív se přihlas')
        return redirect(url_for('login', next_page=request.path))


@app.route("/info/")
def info():
    if 'login' in session:
        return render_template("info.html.j2")
    else:
        flash('Nejdřív se přihlas')
        return redirect(url_for('login', next_page=request.path))


@app.route("/logout/", methods = ['GET'])
def logout():
    session.pop('login', None)
    return redirect(url_for('login'))



############################################################################
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=4444, debug=True)
