import json
from functools import wraps


def handle_resp(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            resp = func(*args, **kwargs)
            return json.loads(resp.content.decode('utf-8'))
        except Exception as e:
            return {"succeed": 0, 'code': 5000, 'result':f"请求失败:{str(e)}"}
    return wrapper

