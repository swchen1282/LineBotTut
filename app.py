from __future__ import unicode_literals
from flask import Flask, request
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    PostbackTemplateAction,
    PostbackEvent
)
import configparser
app = Flask(__name__)


# LINE 聊天機器人的基本資料
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
# handler = WebhookHandler(config.get('line-bot', 'channel_secret'))
parser = WebhookParser(config.get('line-bot', 'channel_secret'))


# 接收 LINE 的資訊
@app.route("/callback", methods=['POST'])
def callback():
    global score
    if request.method == 'POST':
        signature = request.headers['X-Line-Signature']
        body = request.get_data(as_text=True)
        app.logger.info("Request body: " + body)

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError as I:
            return f'[InvalidSignatureError] {I}'
        except LineBotApiError as L:
            return f'[LineBotApiError] {L}'

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                if event.message.text == '測驗':
                    line_bot_api.reply_message(  # 回覆傳入的訊息文字
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='第一題',
                                text='請問下列何者 "不是" 常見的工程師職稱？',
                                actions=[
                                    PostbackTemplateAction(label='軟體工程師', text='軟體工程師', data='1軟體工程師'),
                                    PostbackTemplateAction(label='全端工程師', text='全端工程師', data='1全端工程師'),
                                    PostbackTemplateAction(label='外送工程師', text='外送工程師', data='1外送工程師'),
                                    PostbackTemplateAction(label='資料工程師', text='資料工程師', data='1資料工程師')
                                ]
                            )
                        )
                    )
            elif isinstance(event, PostbackEvent):  # 如果有回傳值事件
                if event.postback.data[0] == '1':  # 回答第1題
                    if event.postback.data[1:] in ['軟體工程師', '全端工程師', '資料工程師']:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    text='答錯囉!!!!',
                                    actions=[PostbackTemplateAction(label='下一題', text='下一題', data='Next2')]
                                )
                            )
                        )
                    if event.postback.data[1:] in ['外送工程師']:
                        score += 25
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    text='恭喜答對!!!!',
                                    actions=[PostbackTemplateAction(label='下一題', text='下一題', data='Next2')]
                                )
                            )
                        )
                    print(f'current score: {score}')
                if event.postback.data == 'Next2':  # 跳出第2題
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='第二題',
                                text='請問下列何者 "不是" 常見的鍵盤配置 (layout)？',
                                actions=[
                                    PostbackTemplateAction(label='QWERTY', text='QWERTY', data='2QWERTY'),
                                    PostbackTemplateAction(label='DVORAK', text='DVORAK', data='2DVORAK'),
                                    PostbackTemplateAction(label='Colemak', text='Colemak', data='2Colemak'),
                                    PostbackTemplateAction(label='THULS', text='THULS', data='2THULS')
                                ]
                            )
                        )
                    )
                if event.postback.data[0] == '2':  # 回答第2題
                    if event.postback.data[1:] in ['QWERTY', 'DVORAK', 'Colemak']:
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    text='答錯囉!!!!',
                                    actions=[PostbackTemplateAction(label='下一題', text='下一題', data='Next3')]
                                )
                            )
                        )
                    if event.postback.data[1:] in ['THULS']:
                        score += 25
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    text='恭喜答對!!!!',
                                    actions=[PostbackTemplateAction(label='下一題', text='下一題', data='Next3')]
                                )
                            )
                        )
                    print(f'current score: {score}')
                if event.postback.data == 'Next3':  # 跳出第3題
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='第三題',
                                text='運算思維可分為4個步驟，下列何者為非？',
                                actions=[
                                    PostbackTemplateAction(label='唉聲嘆氣', text='唉聲嘆氣', data='3唉聲嘆氣'),
                                    PostbackTemplateAction(label='問題拆解', text='問題拆解', data='3問題拆解'),
                                    PostbackTemplateAction(label='規律辨識', text='規律辨識', data='3規律辨識'),
                                    PostbackTemplateAction(label='抽象化與具體化', text='抽象化與具體化', data='3抽象化與具體化')
                                ]
                            )
                        )
                    )
                if event.postback.data[0] == '3':  # 回答第3題
                    if event.postback.data[1:] in ['問題拆解', '規律辨識', '抽象化與具體化']:  # 第3題答錯
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    text='答錯囉!!!!',
                                    actions=[PostbackTemplateAction(label='下一題', text='下一題', data='Next4')]
                                )
                            )
                        )
                    if event.postback.data[1:] in ['唉聲嘆氣']:  # 第3題答對:
                        score += 25
                        line_bot_api.reply_message(
                            event.reply_token,
                            TemplateSendMessage(
                                alt_text='Buttons template',
                                template=ButtonsTemplate(
                                    text='恭喜答對!!!!',
                                    actions=[PostbackTemplateAction(label='下一題', text='下一題', data='Next4')]
                                )
                            )
                        )
                    print(f'current score: {score}')
                if event.postback.data == 'Next4':  # 跳出第4題
                    line_bot_api.reply_message(
                        event.reply_token,
                        TemplateSendMessage(
                            alt_text='Buttons template',
                            template=ButtonsTemplate(
                                title='第四題',
                                text='請問下列何者 "不是" 常見的程式語言？',
                                actions=[
                                    PostbackTemplateAction(label='Java', text='Java', data='4Java'),
                                    PostbackTemplateAction(label='JavaScript', text='JavaScript', data='4JavaScript'),
                                    PostbackTemplateAction(label='Python', text='Python', data='4Python'),
                                    PostbackTemplateAction(label='R', text='R', data='4R')
                                ]
                            )
                        )
                    )
                if event.postback.data[0] == '4':  # 回答第4題
                    if event.postback.data[1:] in ['Java', 'JavaScript', 'Python']:
                        print('我答錯了第4題')
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'第4題答錯，遊戲結束，總分為{score}'))
                        # line_bot_api.reply_message(  # 算總分
                        #     event.reply_token,
                        #     TemplateSendMessage(
                        #         alt_text='Buttons template',
                        #         template=ButtonsTemplate(
                        #             title='答錯囉!!!!',
                        #             actions=[PostbackTemplateAction(label='算總分', text='算總分', data='calc')]
                        #         )
                        #     )
                        # )
                        # print(f'按下算總分 label 後的 postback.data: {event.postback.data}')
                    elif event.postback.data[1:] in ['R']:
                        score += 25
                        print('我答對了第4題')
                        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'第4題答對，遊戲結束，總分為{score}'))
                        # line_bot_api.reply_message(  # 算總分
                        #     event.reply_token,
                        #     TemplateSendMessage(
                        #         alt_text='Buttons template',
                        #         template=ButtonsTemplate(
                        #             title='恭喜答對!!!!',
                        #             actions=[PostbackTemplateAction(label='計算總分', text='計算總分', data='calc')]
                        #         )
                        #     )
                        # )
                        # print(f'按下算總分 label 後的 postback.data: {event.postback.data}')
                    score = 0  # 遊戲結束，還原分數
                # elif event.postback.data == 'calc':  # 作答完畢，計算總分
                #     print(f'第4題選擇後是: {event.postback.data}')
                #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=f'遊戲結束，總分為{score}'))
    return 'OK'


if __name__ == '__main__':
    score = 0
    app.run(debug=True)
