from dotenv import load_dotenv
from flask import request
from mitmproxy import http,ctx
import requests
import json
import os


#목적 .env api키 불러오기

#1.app 서버 주소
sever_url = os.getcwd() #cwd current work diretory 약자

#2. 주소작성 .env
env_address = os.path.join(sever_url,".env")

#3 .env 로드
load_dotenv(env_address)


#클래스 작성 서버통신

class pishshieldaddon:
    def __init__(self):
        self.counter =0

    #proxy-> app으로 url 전달 과정
    def request(self, flow:http.HTTPFlow):


        #app으로 보낼 url 받아오기
        web_url = flow.request.pretty_url

        #ctx 로그 표시 -모니터링 하기 위함
        self.counter += 1
        ctx.log.info(f"[{self.counter}] checking_url: {web_url}]")

        #app접속
        try:
            resp = requests.post("http://localhost:8000/web_url",
                          headers={"auhthorization" : f"bearer {os.getenv("APP_API_KEY")}"},
                          json={"url":web_url},
                          timeout=3,
                          )

            data = resp.json()

        except Exception as e:
            ctx.log.error("phish error {e}")
            return

        receive_data = data.get() # 불러오는 데이터에 따라 사용자에게 경고알림 보내줌 이건 app 부분 작성되면 이어서 작성할 예정
        #json 형태로 4가지 진단을 통해 ssl,쇼단,virustotal,구글피싱사이트 // 통해 json 결과 반환할 예정

