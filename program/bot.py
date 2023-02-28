from fastapi import FastAPI, Request, HTTPException
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage


from program.map import Search_map
from program.config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, logger


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




# main function: msging
@handler.add(MessageEvent)
def handling_message(event):
    replyToken = event.reply_token
    msg_type = event.message.type

    if msg_type == 'text':
        text = event.message.text



    

    # echoMessages = TextSendMessage(text=result)
    line_bot_api.reply_message(reply_token=replyToken, messages=echoMessages)
