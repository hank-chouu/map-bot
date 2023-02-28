from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from dotenv import load_dotenv
import os
import logging

from map import Search_map

logger = logging.getLogger("uvicorn")


load_dotenv()
app = FastAPI()

# Line Bot config
accessToken = os.getenv('CHANNEL_ACCESS_TOKEN')
secret = os.getenv('CHANNEL_SECRET')
API_KEY = os.getenv('MAP_API')


line_bot_api = LineBotApi(accessToken)
handler = WebhookHandler(secret)

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




# main function: msging
@handler.add(MessageEvent)
def handling_message(event):
    replyToken = event.reply_token
    msg = event.message
    msg_type = event.message.type

    result = msg_type

    if msg_type == 'location':
        search = Search_map(API_KEY)
        search.set_coordinates(msg.longitude, msg.latitude)
        search.set_radius(1500)
        search.set_type('restaurant')

        result = search.get_result()
        logger.info(result)
        logger.info(len(result))


    

    echoMessages = TextSendMessage(text=result)
    line_bot_api.reply_message(reply_token=replyToken, messages=echoMessages)

# uvicorn.run(app, host="0.0.0.0", port=8000)