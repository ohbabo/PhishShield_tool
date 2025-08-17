from flask import Flask,request,jsonify,Blueprint
import requests #외부에 API 호출을 위해 사용

from routers import route_bp


def create_app():
    
    app = Flask(__name__) #플라스크 객체 생성

    app.config.from_pyfile('config.py') # config.py에서 변수명이 대문자로 되어 있는것만 불러옴 
    app.register_blueprint(route_bp)


    return app

#이파일이 app이 직접 실행 될때만 작동
if __name__ == "__main__":
    flask_app = create_app()
    port = flask_app.config.get('PORT',8000)
    flask_app.run(port=port,debug=True)
    
