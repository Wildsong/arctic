import os
from urllib import response
from version import version
from flask import Blueprint, make_response, send_file, url_for, request, redirect
from . import main
from database import Database
from app import app
import telegram

@main.route('/update', methods=['GET', 'POST'])
def update():
    bot = telegram.Bot(token=app.config['BOT_TOKEN'])
    rval = bot.send_message(chat_id=app.config['CHAT_ID'],
        text="I got a message from Portal.")
    return "Hi Portal"


@main.route('/status', methods=['GET'])
def status():
    msg = f"""<h1>{version}</h1>
<h2>environment</h2>
<table border=1>"""
    for item in os.environ:
        msg += f"<tr><td>{item}</td><td>{os.environ[item]}</td></tr>"
    msg += "</table>"
    return msg


@main.route('/', methods=['GET'])
def mainpage():
    return """
    <h1>Arctic Webhooks</h1>
        <a href="/update">update</a><br />
        <a href="/status">status</a><br />
    """

# That's all!
