from flask import Flask,request,abort
from linebot import LineBotApi,WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent,TextMessage,TextSendMessage
import os

app=Flask(__name__)
#環境変数の取得
YOUR_CHANNEL_ACCESS_TOKEN="pva3jcNvg8QmawE0iiwvJTG04//LLhNKijeKJ4NhSQBxIhn6rkHhfV0V29nBf1onqKaGtGEcjuDXWVSHTBTGCTtkL8HTnQ3lBGLDx826dxK93lmmjSij5Skyw1zdEvXz9g0StelErFNdN7X9kQiUqAdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET="f6342f757b8c11faf010f0df093e16ac"
line_bot_api=LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler=WebhookHandler(YOUR_CHANNEL_SECRET)

@app.route("/callback",methods=["POST"])
def callback():
    signature=request.headers["X-Line-Signature"]

    body=request.get_data(as_text=True)
    app.logger.info("Request body"+body)

    try:
        handler.handle(body,signature)
    except InvalidSignatureError:
        abort(400)
    return "OK"

@handler.add(MessageEvent,message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=event.message.text))

if __name__=="__main__":
    port=int(os.getenv("PORT",5000))
    app.run(host="0.0.0.0",port=port)