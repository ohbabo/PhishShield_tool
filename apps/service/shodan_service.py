import shodan
from config import shodan_key #config에서 shodankey 불러오기


api = shodan.Shodan(shodan_key) #쇼단 key로 api 활성화

#api 주소 검색 쿼리로 올바른 도메인인지 판단하는 로직

class shodan_search:
    