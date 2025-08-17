def create_header(api_key):

    if not api_key:
        # 혹시 키가 없는 경우를 대비한 안전장치
        return {"Content-Type": "application/json"}
        
    return {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }