import json
from functools import wraps


def singleton(func):
	instances = {}
	def wrapper(*args, **kwargs):
		if len(args) > 0:
			username = args[0]
		else:
			username = kwargs.get('username')
		if not instances[username]:
			instances[username] = func(args, kwargs)


	return wrapper


def handle_resp(func):
	@wraps(func)
	def wrapper(*args, **kwargs):
		try:
			resp = func(*args, **kwargs)
			return json.loads(resp.content.decode('utf-8'))
		except Exception as e:
			return {"succeed": 1, 'code': 5000, 'msg': f"请求失败:{str(e)}"}
	return wrapper