import base64
import hashlib
import json
import urllib.parse

import requests
# 忽略SSL验证
# import warnings
# from requests.packages import urllib3
# urllib3.disable_warnings()
# warnings.filterwarnings("ignore")
from .decorator import handle_resp

class TestZmn():

	def __init__(self, test_addr, version="v1"):
		"""
		:param test_addr: protocol://ip:port, For example http://192.168.3.5:8050, ignore port if use default port of protocol
		:param version: For example v1
		"""
		self.base_url = f"{test_addr}/api/{version}"
		# 创建一个 hashlib.md5 对象

		self.login_url = f"{self.base_url}/login/"
		self.user_myaccount_url = f"{self.base_url}/user/myaccount/"
		self.project_url = f"{self.base_url}/projects/"
		self.user_url = f"{self.base_url}/user/"

	def login(self, username, password):
		"""登录接口
		:param username: 用户名
		:param password: 密码
		:return:
		"""
		hash_object = hashlib.md5()
		hash_object.update(password.encode('utf-8'))
		data = {
			"username": base64.b64encode(username.encode('utf-8')).decode('utf-8'),
			"password": hash_object.hexdigest()
		}
		# 获取登录凭证
		self.session = requests.session()
		try:
			resp = self.session.post(url=self.login_url, data=data, verify=False)
			if resp.status_code == 200:
				resp_content = json.loads(resp.content.decode('utf-8'))
				if resp_content['succeed'] == 0:
					# 设置token
					self.session.headers["token"] = resp_content['token']
					# 设置cookie
					cookies = resp.cookies
					cookie_content = []
					for item in cookies:
						cookie_content.append(item.name + "=" + item.value)
					self.session.headers['Cookie'] = ";".join(cookie_content)
				return True, resp_content
			else:
				raise Exception(f"响应结果：{resp}")
		except Exception as e:
			return {"succeed": 1, 'code': 5000, 'msg': f"{self.login_url}请求失败, {str(e)}"}

	@handle_resp
	def user_myaccount(self):
		return self.session.get(url=self.user_myaccount_url)

	@handle_resp
	def project(self, method, **kwargs):
		method = str(method).upper()
		if method == 'GET':
			# 获取项目
			page_index = kwargs.get('page_index', 1)
			page_size = kwargs.get('page_size', 10)
			url = f"{self.project_url}?page_index={page_index}&page_size={page_size}"
			for k, v in kwargs.items():
				url += f"&{k}={v}"
			url = urllib.parse.quote(url)
			return self.session.get(url)
		elif method == 'POST':
			# 创建项目
			data = kwargs.get('data', None)
			if data == None:
				raise Exception(f"使用{method}请求{self.project_url}未传入data")
			else:
				return self.session.post(self.project_url, data=data)
		else:
			return self.session.request(method=method)

	@handle_resp
	def user(self, **kwargs):
		"""
		获取用户
		:param kwargs:
		:return:
		"""
		page_index = kwargs.get('page_index', 1)
		page_size = kwargs.get('page_size', 10)
		url = f"{self.project_url}?page_index={page_index}&page_size={page_size}"
		for k, v in kwargs.items():
			url += f"&{k}={v}"
		url = urllib.parse.quote(url)
		return self.session.get(url)


if __name__ == "__main__":
	url = "http://192.168.2.123"
	# url = "http://127.0.0.1:8000"
	test_obj = TestZmn(url)
	test_obj.login("tianhy","123qwe")
	res = test_obj.user_myaccount()
	print(f"{res}")