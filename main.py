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
    replyUrl = recipeClass.get_recipe(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        [TextSendMessage(text=replyUrl[0]), TextSendMessage(text=replyUrl[1]), TextSendMessage(text=replyUrl[2]), TextSendMessage(text=replyUrl[3])])

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
    replyUrl = recipeClass.get_recipe(rankName[0])

    line_bot_api.reply_message(
    event.reply_token,
    columns=[
        CarouselColumn(
            thumbnail_image_url=column['thumbnail_image_url'],
            title=column['title'],
            text=column['text'],
            actions=[URITemplateAction(label=column['actions']['label'],uri=column['actions']['uri'])]
        )
        url = ['replyUrl[0]', 'replyUrl[1]', 'replyUrl[2]', 'replyUrl[3]']
        for column in url
    ]
    TemplateSendMessage(alt_text='template',template=CarouselTemplate(columns=columns))
    #[TextSendMessage(text=replyUrl[0]), TextSendMessage(text=replyUrl[1]), TextSendMessage(text=replyUrl[2]), TextSendMessage(text=replyUrl[3])]
    )

    #except Exception as e:
    #    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=' エラーが発生しました'))
    


if __name__ == "__main__":
    # app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
