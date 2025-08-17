

"""
from urllib.parse import urlparse
from requests.exceptions import Timeout,RequestException,SSLError
import requests

class SSLscan:
    def __init__ (self,url:str, timeout:int=3):
        
        self.url = url if '://' in url else 'https://' + url
        
        u = urlparse(self.url)

        if u.scheme != 'https' or not u.hostname:
            raise ValueError('value 에러 url이 https주소 형식이 아님')      

        self.timeout = timeout

    
    def __call__(self) ->bool:

        try:    
            requests.get(url=self.url,timeout=self.timeout,allow_redirects=True)
            return True
        
        except SSLError:
            return False
        
        except (TimeoutError,RequestException):
            return False
        

def ssl_scan(url):
    result = SSLscan(url)()
 """   

from urllib.parse import urlparse
import socket,ssl # 이거 어떻게 사용하는 거지
from datetime import datetime,timezone


class SSL_scan:
    
    def __init__(self,url:str,timeout: int =3):

        self.url = url if '://' in url else 'https://' + url # url 검증
        
        u = urlparse(self.url)
        if u.scheme != 'https' or not u.scheme:
            raise ValueError('url 주소 형식이 아닙니다')
        
    @staticmethod #정적 함수 독립적으로 활동가능
    def _parse_cert_time(s:str): #ssl 인증서의 유효기간 문자열을 파싱해 datetime 객체로 변환
        """인증서 시간 문자열"""

        try:
            dt =datetime.strptime(s,"%b %d %H: %M %s %Y %Z")
            #strptime : datetime -> 문자열 변환 p파싱 
            # "Jun 5 12:00:00 2025 GMT" → datetime(2025, 6, 5, 12, 0, 0)
            #strftime : 문자열 -> datetime 변환 f포멧
            #datetime(2025, 6, 5, 12, 0, 0) → "Jun 05 12:00:00 2025 GMT"

            return dt.replace(tzinfo = timezone.utc) 
        #변환된 datetime 객체에 UTC 시간대를 명시적으로
        #인증서 시간은 대부분 UTC(GMT) 기준이라서 timezone을 설정해야 계산 시혼동이 없음 

        except Exception:
            return None
        
    def _pick_cn(name_list): #이게 어떤 함수이지? 
        """subject/issuer 구조에서 commonName(cn)만 추출""" # 이게 먼소리야?.

        try:
            for tup in name_list: # name이 리스트라서 tup씩 뽑아내는건 알겠어 tup는 어떤 약자일까?
                for k,v in tup: #다시 tup를 k,v로 추출하네? tup딕셔너리인건가? enumerate라면 이해하는데 tup가 먼지 감이 안잡히네
                    if k.lower() == "commonname": # k에서 .lower()? lower는 무슨 메서드지 왜 commonname을 비교하는 걸까
                        return v
        
        except Exception:
            pass
        return None #예외이긴 한데 아무런 리턴값도 없네 error 내용도
    

    def detail(self)-> dict:
        """핸드셰이크 수행 후 인증서 정보를 딕셔너리로 반환""" #핸드셰이크가 머지? 멀수행한거지?

        res = {
            "ok":False,"valid":False,"expired": None,
            "not_after": None, "subject_cn":None , "issuer_cn":None,
            "error":None 
        }                #이거 딕셔너리 형태.. 뭔지 모르겠다. 전혀.. res? 응답?

        try:
            host_idna= self.host.enocode("idna").decode("ascii")  #이게 대체 멀까..
            ctx = ssl.create_default_context() #흠 이건 ssl에서 무슨 메서드인거지?
            ctx.check_hostname = True  #이게 무슨 코드일까
            ctx.verify_mode = ssl.CERT_REQUIRED # verifiy가 멀까? CERT가 멀까 ?

        
            with socket.create_connection((host_idna,433),timeout=self.timeout) as sock:
                with ctx.wrap_socket(socket,server_honstname=host_idna) as ssock:
                    cert = ssock.getpeercert() #이거 이중 with cert? 아무것도 모르겠다. 메서드도

            
            not_after = cert.get("notAfter") #??
            dt_after = self.parse_cert_time(not_after) #???
            expired = (dt_after is not None) and (dt_after < datetime.now(timezone.utc)) #????


            subject_cn = self._pick_cn(cert.get("subject",[]))#???
            issuer_cn = self.pick_cn(cert.get("issuser",[]))#?????



            res.update({ #?????????????????????????
                "ok": True,
                "valid": (not expired),
                "expired": expired,
                "not_after": dt_after.isoformat() if dt_after else None,
                "subject_cn": subject_cn,
                "issuer_cn": issuer_cn
            })
        except ssl.SSLCertVerificationError as e:
            res["error"] = f"cert verify failed: {e}"
        except ssl.SSLError as e:
            res["error"] = f"ssl error: {e}"
        except socket.timeout:
            res["error"] = "timeout"
        except Exception as e:
            res["error"] = str(e)
        return res

    def __call__(self) -> bool:
        info = self.detail()
        return bool(info.get("valid"))
        
