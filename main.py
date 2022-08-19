import os
import re
import json
import random
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

# For Test

load_dotenv()  # Load your local environment variables


CHANNEL_TOKEN = os.environ.get('LINE_TOKEN')
CHANNEL_SECRET = os.getenv('LINE_SECRET')

app = FastAPI()

# Connect Your API to Line Developer API by Token
My_LineBotAPI = LineBotApi(CHANNEL_TOKEN)
# Event handler connect to Line Bot by Secret key
handler = WebhookHandler(CHANNEL_SECRET)

# For any message pushing to or pulling from Line Bot using this ID
CHANNEL_ID = os.getenv('LINE_UID')
# My_LineBotAPI.push_message(CHANNEL_ID, TextSendMessage(text='Welcome to my pokedex !')) # Push a testing message

# Create my emoji list
my_emoji = [
    [{'index': 0, 'productId': '5ac1bfd5040ab15980c9b435', 'emojiId': '001'}],
    [{'index': 0, 'productId': '5ac1bfd5040ab15980c9b435', 'emojiId': '041'}],
    [{'index': 0, 'productId': '5ac1bfd5040ab15980c9b435', 'emojiId': '048'}]
]


@app.post('/')
async def callback(request: Request):
    body = await request.body()  # Get request
    # Get message signature from Line Server
    signature = request.headers.get('X-Line-Signature', '')
    try:
        # Handler handle any message from LineBot and
        handler.handle(body.decode('utf-8'), signature)
    except InvalidSignatureError:
        raise HTTPException(404, detail='LineBot Handle Body Error !')
    return 'OK'

# Check if input operant is a number


def isNum(operant):
    if (operant.lstrip('-').isdigit()):
        return True
    else:
        return False


@handler.add(MessageEvent, message=TextMessage)
def handle_textmessage(event):
    ''' Basic Message Reply
    message = TextSendMessage(text= event.message.text)
    My_LineBotAPI.reply_message(
        event.reply_token,
        message
    )
    '''
    # Split msg from input message
    splitMsg = str(event.message.text).split(' ')
    getExpression = ''.join(splitMsg).replace('=', '')
    # Expression : a op b
    a = ''
    op = ''
    b = ''
    isNextOperant = False
    OP = {'+', '-', '*', '/'}
    for i, ch in enumerate(getExpression):
        if i == 0 and ch == '-':
            a = ch
        elif ch in OP:
            op = ch
            isNextOperant = True
        elif isNextOperant:
            b += ch
        else:
            a += ch
    # Exception handler
    replyEmoji = random.choice(my_emoji)
    if not isNum(a) or not isNum(b) or not op in OP:
        My_LineBotAPI.reply_message(
            event.reply_token,
            TextSendMessage(
                text='$ Calculator does not recognize the method. Please enter your expression again.',
                emojis=replyEmoji
            )
        )
        return

    # Calculate
    replyEmoji = random.choice(my_emoji)
    a = int(a)
    b = int(b)
    ans = 0
    if op == '+':
        ans = a+b
    elif op == '-':
        ans = a-b
    elif op == '*':
        ans = a*b
    elif op == '/':
        if b == 0:  # Zero Division Exception
            My_LineBotAPI.reply_message(
                event.reply_token,
                TextSendMessage(
                    text='$ Dividing a number by Zero is a mathematical error. Please enter your expression again.',
                    emojis=replyEmoji
                )
            )
            return
        else:
            ans = a/b

    # send result
    My_LineBotAPI.reply_message(
        event.reply_token,
        TextSendMessage(text=f'{a} {op} {b} = {ans}')
    )


class My_Sticker:
    def __init__(self, p_id: str, s_id: str):
        self.type = 'sticker'
        self.packageID = p_id
        self.stickerID = s_id


# Add stickers into my_sticker list
my_sticker = [My_Sticker(p_id='789', s_id='10856'), My_Sticker(p_id='789', s_id='10868'),
              My_Sticker(p_id='789', s_id='10876'), My_Sticker(p_id='789', s_id='10884'), ]


# Line Sticker Event
@handler.add(MessageEvent, message=StickerMessage)
def handle_sticker(event):
    # Random choice a sticker from my_sticker list
    ranSticker = random.choice(my_sticker)
    # Reply Sticker Message
    My_LineBotAPI.reply_message(
        event.reply_token,
        StickerSendMessage(
            package_id=ranSticker.packageID,
            sticker_id=ranSticker.stickerID
        )
    )


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app='main:app', reload=True, host='0.0.0.0', port=8787)
