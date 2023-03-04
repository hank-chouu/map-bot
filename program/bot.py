from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, FollowEvent, UnfollowEvent, JoinEvent, LeaveEvent
from linebot.models import TextSendMessage, FlexSendMessage
import json


from program.map import Search_map
from program.config import CHANNEL_ACCESS_TOKEN, CHANNEL_SECRET, allLogger
from program.db import Mongo
from program.carousel import resp_to_carousel, init_msg, init_msg2

app = Flask(__name__)

# Line Bot config


line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'




# handlers
# main function: msging
@handler.add(MessageEvent)
def handling_message(event):
    try:
        reply_token = event.reply_token
        if event.source.type == 'user':
            user_id = event.source.user_id
        elif event.source.type == 'group':
            user_id = event.source.group_id
        # should make sure id is in
        # currently not allowing join group chat, so can inplement later
        msg_type = event.message.type

        user_status = Mongo.get_status(user_id)

        if msg_type == 'text':

            received_text = event.message.text

            # need to handle the text len issue           

            # phase 1: determine type
            if user_status == 0:
                if ('附近有什麼' in received_text or '附近有甚麼' in received_text) and (
                    '餐廳' in received_text or '咖啡廳' in received_text or '酒吧' in received_text):                
                    if '餐廳' in received_text:
                        keyword = '餐廳'
                    elif '咖啡廳' in received_text:
                        keyword = '咖啡廳'
                    elif '酒吧' in received_text:
                        keyword = '酒吧'
                    Mongo.save_keyword(user_id, keyword)                            
                    reply_msg = TextSendMessage(text='我來找找！接下來請傳送你目前的位置資訊給我')
                    
                else:
                    reply_msg = FlexSendMessage(alt_text='重新開始查詢', contents=init_msg2)
                line_bot_api.reply_message(reply_token = reply_token, messages = reply_msg)

            # phase 2-1: fool-proofing
            elif user_status == 1:
                reply_msg = TextSendMessage(text='請傳送位置訊息給我！')
                line_bot_api.reply_message(reply_token = reply_token, messages = reply_msg)

            # phase 3: return api data
            elif user_status == 2:                
                if '走路' in received_text  or '搭車' in received_text:
                    if received_text == '走路':
                        radius = 600
                    elif received_text == '搭車':
                        radius = 3000
                    params = Mongo.get_params(user_id)

                    Search = Search_map()
                    Search.set_keyword(params['keyword'])
                    Search.set_coordinates(params['latitude'], params['longitude'])
                    Search.set_radius(radius)

                    resp = Search.get_result()
                    resp = json.loads(resp)
                    app.logger.info('Found ' + str(len(resp['results'])) + ' places')

                    
                    # 簡化(get first 10) 算距離 照片url 連結url 做成carousel
                    if len(resp['results']) != 0:
                        carousel = resp_to_carousel(resp, [params['latitude'], params['longitude']])
                        reply_msg = FlexSendMessage(alt_text='查詢結果', contents=carousel)
                    else:
                        reply_msg = TextSendMessage(text='附近沒有營業中的店家了-0-')

                    # 完成後要洗掉status跟params
                    Mongo.reset_user(user_id)
                else:
                    reply_msg = TextSendMessage(text='不太懂你在說什麼欸哈哈，請回覆「走路」或者「搭車」')
                line_bot_api.reply_message(reply_token = reply_token, messages = reply_msg)           
                

        # phase 2: determine location
        elif msg_type == 'location' and user_status == 1:

            latitude = event.message.latitude
            longitude = event.message.longitude

            Mongo.save_location(user_id, latitude, longitude)

            reply_msg = TextSendMessage(text='好喔！最後的問題：你比較偏好走路還是搭車呢？')
            line_bot_api.reply_message(reply_token = reply_token, messages = reply_msg)


    except Exception as e:
        app.logger.error(str(e), exc_info=True)



@handler.add(FollowEvent)
def create_new_user(event):

    user_id = event.source.user_id
    reply_token = event.reply_token

    reply_msg = FlexSendMessage(alt_text='開始查詢', contents=init_msg)

    Mongo.insert_new(user_id)
    line_bot_api.reply_message(reply_token=reply_token, messages=reply_msg)

@handler.add(JoinEvent)
def join_new_group(event):

    group_id = event.source.group_id
    reply_token = event.reply_token

    reply_msg = FlexSendMessage(alt_text='開始查詢', contents=init_msg)

    Mongo.insert_new(group_id)
    line_bot_api.reply_message(reply_token=reply_token, messages=reply_msg)



@handler.add(UnfollowEvent)
def remove_user(event):

    user_id = event.source.user_id
    Mongo.delete(user_id)


@handler.add(LeaveEvent)
def leave_group(event):

    group_id = event.source.group_id
    Mongo.delete(group_id)

if __name__ == "__main__":   
    app.run(debug=True)
