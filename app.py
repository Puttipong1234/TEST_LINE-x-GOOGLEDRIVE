from __future__ import unicode_literals

import json
import os
import sys
from argparse import ArgumentParser

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookParser
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,FileMessage
)
from flask_sqlalchemy import SQLAlchemy


# from Download import download_file

app = Flask(__name__)
db = SQLAlchemy(app)
from connect import create_connection

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{}'.format(create_connection('Test01'))


#### _____________ end g drive setup_____________#####





# get channel_secret and channel_access_token from your environment variable

line_bot_api = LineBotApi('1RfIiAbjneORMpj+sIGYx+Yi0esjdG/F/VQxyIc6/dFoCVym6hZzDrBqxpd5Ui8XFLsdzohfRuvZRU1dsCP0yaSN3Rdx7U3PeT/0kZfnkrAXrmtrclZaw0v/tA6vOe2fM93R+JvDab5xhxN/4vtGYQdB04t89/1O/w1cDnyilFU=')
parser = WebhookParser('31d9c964d1afd080749b16d09f2f016c')

#### ให้ลอง download file จาก line


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    session = ''

    with open('session.json') as file:
        session = json.load(file)
        print(session['session'])
    # upload session
        for event in events:

            if isinstance(event, MessageEvent) and TextMessage is type(event.message):
                if event.message.text == 'UPLOAD':
                    session['session'] = 'UPLOAD'
                    line_bot_api.reply_message(event.reply_token,TextMessage(text = "Please Upload Some File"))
                
                if event.message.text == 'CANCEL':
                    session['session'] = ''
                    line_bot_api.reply_message(event.reply_token,TextMessage(text = "You have cancel upload session"))

            if isinstance(event, MessageEvent) and (FileMessage is type(event.message)):
                if session['session'] == 'UPLOAD':
                    session['file_name'] = str(event.message.file_name).split('.')[0]

                    filetype = str(event.message.file_name).split('.')[-1]
                    print(filetype)

                    download_file(str(event.message.id),filetype,session['file_name'])
                    line_bot_api.reply_message(event.reply_token,TextMessage(text = session['file_name'] + "     " + "ํYour Upload session is Complete"))
                    session['session'] = ''
        file.close()

    with open('session.json','w') as w_file:
        json.dump(session,w_file)
        w_file.close()

              


    return 'OK'


if __name__ == "__main__":

    app.run(port=80)
    