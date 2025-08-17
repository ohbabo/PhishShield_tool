from flask import Blueprint,request,jsonify,current_app
from apps.service.google_service import google_scan
from apps.service.phishing_service import phishing_scan
from apps.service .shodan_service import shodan_scan
from apps.service.ssl_service import ssl_scan

route_bp = Blueprint('scan',__name__)

#블루 프린트 생성 Blueprint(부품이름,부품출처,url 그룹이름)

@route_bp.route('/web_url',methods=['GET','POST'])
def scan():
    data  = request.get_json()

    url=data.get('url')
    app_api= data.get('app_api')

    if not url :
        return jsonify(error="empty url"),400
    
    if app_api != current_app.config.get('APP_API_KEY'):
        return jsonify (error = " KEY not access"),403
    
    #true,flase 반환
    ssl_result =ssl_scan(url) 
    shodan_result = shodan_scan(url)
    google_result = google_scan(url)
    phishing_result = phishing_scan(url)

    send_data= {"url":url,
                "result":{
                    "google" : google_result,
                    "shodan" : shodan_result,
                    "phishing": phishing_result,
                        "ssl" : ssl_result
                        }}
    
    return jsonify(send_data),200

    

