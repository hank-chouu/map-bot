from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, FollowEvent, UnfollowEvent


from program.map import Search
from program.config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, logger
from program.db import Mongo


app = FastAPI()

# Line Bot config


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

@app.post("/")
async def Bot(request: Request):
    signature = request.headers["X-Line-Signature"]
    body = await request.body()
    # logger.info(body.decode())
    try:
        handler.handle(body.decode(), signature)
    except InvalidSignatureError:
        raise HTTPException(status_code=400, detail="Missing Parameters")
    return "OK"


# handlers
# main function: msging
@handler.add(MessageEvent)
def handling_message(event):
    reply_token = event.reply_token
    user_id = event.source.user_id
    msg_type = event.message.type

    user_status = Mongo.return_status(user_id)

    if msg_type == 'text':

        received_text = event.message.text

        # phase one: determine type
        if (received_text[:5] == '附近有什麼' or received_text['5'] == '附近有甚麼') and user_status == 0:
            if received_text[5:7] == '餐廳':

                search_type = 'restaurant'
                Mongo.saving_type(user_id, search_type)
                
                reply_msg = TextSendMessage(text='我來找找！接下來請傳送你目前的位置資訊給我')
                line_bot_api.reply_message(reply_token = reply_token, messages = reply_msg)

    # phase 2: determine location
    elif msg_type == 'location' and user_status == 1:

        latitude = event.message.latitude
        longitude = event.message.longitude

        # logger.info(type(latitude))
        # logger.info(latitude)

        Mongo.saving_location(user_id, latitude, longitude)

        reply_msg = TextSendMessage(text='好喔！最後的問題：你比較偏好走路還是搭車呢？')
        line_bot_api.reply_message(reply_token = reply_token, messages = reply_msg)

        


        





    

    # echoMessages = TextSendMessage(text=result)
    # line_bot_api.reply_message(reply_token=replyToken, messages=echoMessages)

@handler.add(FollowEvent)
def create_new_user(event):

    user_id = event.source.user_id
    reply_token = event.reply_token

    # logger.info(event.source.__dir__())

    reply_msg = TextSendMessage(text = '哈囉！請從輸入「附近有什麼餐廳」開始')

    Mongo.insert_new(user_id)
    line_bot_api.reply_message(reply_token=reply_token, messages=reply_msg)


@handler.add(UnfollowEvent)
def remove_user(event):

    user_id = event.source.user_id
    Mongo.delete(user_id)
