# -*- coding: utf-8 -*-
# from  타인모듈 import *
import json
import re
from firsts import *
from detail_Team import *
from Today_matchs import *
from Total_Rank import *
from slackclient import SlackClient
from flask import Flask, request, make_response

app = Flask(__name__)

slack_token = "xoxb-502761537154-508893399238-9KZcm5vdRL5ab8D4mUHW68Re"
slack_client_id = "502761537154.508890214422"
slack_client_secret = "3a6ac09ec7aed09163877182fe54f2a3"
slack_verification = "cVdwBayYG4jCpqLOkhaWTVQE"
sc = SlackClient(slack_token)
pre_timestamp = ""


# 크롤링 함수 구현하기
def answer(text):
    # 여기에 함수를 구현해봅시다.
    result = re.sub(r'<@\S+>', '', text).strip()

    if result is not '':
        a = total_rank(result)
        if a is False:
            if len(result.split(' ')) > 1 and result.split(' ')[1] == '오늘일정':
                return today_match(result.split(' ')[0])
            else:
                return detail_team(result)
        else:
            return a
    else:
        return first()


# 이벤트 핸들하는 함수
def _event_handler(event_type, slack_event):
    print(slack_event["event"])

    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]
        text = slack_event["event"]["text"]
        # [메뉴, 딕셔너리]
        keywords = answer(text)
        if keywords[0] == 0:
            daily = keywords[1]

            for i in range(len(daily['date'])):
                msg = {}
                msg["title"] = daily['date'][0]
                a = " "
                b = " "
                if i * 2 >= len(daily['score']):
                    pass
                else:
                    a= daily['score'][i*2]
                    b= daily['score'][i*2+1]
                msg["title"] = daily['time'][i] + " : " + daily['place'][i]
                msg["fields"] = [
                    {
                        "title" : daily['name'][i*2],
                        "value": a,
                        "short" : True
                    },
                    {

                        "title" : daily['name'][i*2+1],
                        "value": b,
                        "short": True
                    }
                ]
                msg["color"] = "#F36F81"
                sc.api_call(
                    "chat.postMessage",
                    channel=channel,
                    text="",
                    attachments=json.dumps([msg])
                )
        else:
            msg = {}
            msg["text"] = keywords
            msg[
                "thumb_url"] = ""
            msg["color"] = "#F36F81"
            sc.api_call(
                "chat.postMessage",
                channel=channel,
                text="",
                attachments=json.dumps([msg])
            )

        return make_response("App mention message has been sent", 200, )

    # ============= Event Type Not Found! ============= #
    # If the event_type does not have a handler
    message = "You have not added an event handler for the %s" % event_type
    # Return a helpful error message
    return make_response(message, 200, {"X-Slack-No-Retry": 1})


@app.route("/listening", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)

    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type":"application/json"})

    if slack_verification != slack_event.get("token"):
        message = "Invalid Slack verification token: %s" % (slack_event["token"])
        make_response(message, 403, {"X-Slack-No-Retry": 1})

    # oldstamp 반복으로 안나오게 하는 부분
    if "event" in slack_event:
        # event_type = slack_event["event"]["type"]
        # return _event_handler(event_type, slack_event)
        global pre_timestamp
        if pre_timestamp < slack_event["event"]["ts"]:
            event_type = slack_event["event"]["type"]
            pre_timestamp = slack_event["event"]["ts"]
            return _event_handler(event_type, slack_event)
        else:
            print("Duplicated message : " + slack_event["event"]["ts"])
            return make_response("duplicated message", 200, )


    # If our bot hears things that are not events we've subscribed to,
    # send a quirky but helpful error response
    return make_response("[NO EVENT IN SLACK REQUEST] These are not the droids\
                         you're looking for.", 404, {"X-Slack-No-Retry": 1})


@app.route("/", methods=["GET"])
def index():
    return "<h1>Server is ready.</h1>"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5050)


