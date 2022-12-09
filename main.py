#物体検出用のクラスをimport
from module.yolo.detect import Detect
# レシピ取得用のクラスをimport
from module.recipe import Recipe

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    CarouselColumn, CarouselTemplate, ImageMessage, MessageEvent, TemplateSendMessage, TextMessage, TextSendMessage, URITemplateAction
)
import os

app = Flask(__name__)

# 環境変数取得
#YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
#YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]
YOUR_CHANNEL_ACCESS_TOKEN = "+25iVYmzKQ1abS+pM/Zdg6Enf/8Ul2a292hQ4eN++cxv/2WeJbA7YEhK7Qze4AALyWgP72R5K7Pt77A7ybJiz3ZfTNUBMV9flxmP2zLeh7IkH227bAW8105eK8nEoBxaBjRnqlOsbI9Lg6qdA/ozUgdB04t89/1O/w1cDnyilFU="
YOUR_CHANNEL_SECRET = "7bbd4021f2da55f08e5242df6ee70734"

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    recipeClass = Recipe()
    replyUrl, replyImg, replyTitle = recipeClass.get_recipe(event.message.text)
    #column = handle_column(replyUrl,replyImg,replyTitle)
    columns = [
                CarouselColumn(
                  thumbnail_image_url=replyImg[0],
                  title=replyTitle[0],
                  text=replyTitle[0],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[0],
                      )
                  ]
                ),
                CarouselColumn(
                  thumbnail_image_url=replyImg[1],
                  title=replyTitle[1],
                  text=replyTitle[1],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[1],
                      )
                  ]
                ),
                CarouselColumn(
                  thumbnail_image_url=replyImg[2],
                  title=replyTitle[2],
                  text=replyTitle[2],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[2],
                      )
                  ]
                ),
                CarouselColumn(
                  thumbnail_image_url=replyImg[3],
                  title=replyTitle[3],
                  text=replyTitle[3],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[3],
                      )
                  ]
                )
            ]
    line_bot_api.reply_message(
        event.reply_token,
        #[TextSendMessage(text=replyUrl[0]), TextSendMessage(text=replyUrl[1]), TextSendMessage(text=replyUrl[2]), TextSendMessage(text=replyUrl[3])])
        #messages)
        TemplateSendMessage(alt_text='カルーセル', template=CarouselTemplate(columns=columns))
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_image(event):
    print("handle_image:", event)

    message_id = event.message.id
    message_content = line_bot_api.get_message_content(message_id)

    # image = BytesIO(message_content.content)

    with open('static/' + event.message.id + '.jpg', 'wb') as f:
        f.write(message_content.content)

    contentUrl='https://recipe-bot.onrender.com/' + 'static/' + event.message.id + '.jpg'
    #try:
    detectClass = Detect()
    rankName = detectClass.detect_img(image=contentUrl)
    recipeClass = Recipe()
    replyUrl, replyImg, replyTitle = recipeClass.get_recipe(rankName[0])
    columns = [
                CarouselColumn(
                  thumbnail_image_url=replyImg[0],
                  title=replyTitle[0],
                  text=replyTitle[0],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[0],
                      )
                  ]
                ),
                CarouselColumn(
                  thumbnail_image_url=replyImg[1],
                  title=replyTitle[1],
                  text=replyTitle[1],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[1],
                      )
                  ]
                ),
                CarouselColumn(
                  thumbnail_image_url=replyImg[2],
                  title=replyTitle[2],
                  text=replyTitle[2],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[2],
                      )
                  ]
                ),
                CarouselColumn(
                  thumbnail_image_url=replyImg[3],
                  title=replyTitle[3],
                  text=replyTitle[3],
                  actions=[
                      URITemplateAction(
                          label="レシピの詳細",
                          uri=replyUrl[3],
                      )
                  ]
                )
            ]
    line_bot_api.reply_message(
    event.reply_token,
    #messages=messages,
    #[TextSendMessage(text=replyUrl[0]), TextSendMessage(text=replyUrl[1]), TextSendMessage(text=replyUrl[2]), TextSendMessage(text=replyUrl[3])]
    TemplateSendMessage(alt_text='カルーセル', template=CarouselTemplate(columns=columns))
    )

    #except Exception as e:
    #    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=' エラーが発生しました'))
    


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
