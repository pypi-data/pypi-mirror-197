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
        self.session = requests.session()
        self.base_url = f"{test_addr}/api/{version}"

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
            "username": base64.b64encode(
                username.encode('utf-8')).decode('utf-8'),
            "password": hash_object.hexdigest()}
        # 获取登录凭证
        try:
            resp = self.session.post(
                url=self.login_url, data=data, verify=False)
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
                return resp_content
            else:
                raise Exception(resp)
        except Exception as e:
            return e


    @handle_resp
    def user_myaccount(self):
        """GET 根据token返回登录的用户信息"""
        return self.session.get(url=self.user_myaccount_url)

    @handle_resp
    def project(self, **kwargs):
        """
        :param kwargs:
            method:(不传默认为GET)
                GET 获取项目列表
                POST 创建项目 传入data，为项目创建相关信息
            page_index: 查询起始页索引 默认1
            page_size: 每页最多展示多少个 默认10
            status: 获取项目列表时的可选过滤条件
            base64_fileds: 数组  base64_fileds = [str1,str2...]
        :return:
        """
        method = kwargs.get('method', 'get').upper()
        if method == 'GET':
            # 获取项目
            kwargs.setdefault('page_index', 1)
            kwargs.setdefault('page_size', 10)
            url = f"{self.project_url}?"

            if kwargs.get('base64_fileds', None) != None:
                b_data = kwargs["base64_fileds"]
                kwargs.pop("base64_fileds")
                if isinstance(b_data, list):
                    temp_url = ""
                    for param in kwargs['base64_fileds']:
                        temp_url += f"&base64_fileds[]={urllib.parse.quote(str(param).encode('utf-8'))}"
                    url += temp_url

            for k, v in kwargs.items():
                url += f"&{urllib.parse.quote(str(k).encode('utf-8'))}={urllib.parse.quote(str(v).encode('utf-8'))}"
            # url = urllib.parse.quote(url)
            return self.session.get(url)
        elif method == 'POST':
            # 创建项目
            data = kwargs.get('data', None)
            if data is None:
                raise Exception(f"使用{method}请求{self.project_url}未传入data")
            else:
                return self.session.post(self.project_url, data=data)
        else:
            return self.session.request(method=method)

    @handle_resp
    def user(self, **kwargs):
        """GET 获取用户
        :param kwargs:
            page_index: 查询起始页索引 默认1
            page_size: 每页最多展示多少个 默认10
        :return:
        """
        kwargs.setdefault('page_index', 1)
        kwargs.setdefault('page_size', 10)
        url = f"{self.project_url}?"
        for k, v in kwargs.items():
            url += f"&{urllib.parse.quote(str(k).encode('utf-8'))}={urllib.parse.quote(str(v).encode('utf-8'))}"
        return self.session.get(url)


if __name__ == "__main__":
    """使用说明
        1.实例化一个TestZmn()对象  
            【必填】请求地址 protocol://ip:port，如果使用协议默认端口，则端口可省略
            【可选】版本 默认 v1
        2.根据url调用相关接口，传入相关参数
    """
    url = "http://192.168.2.123"
    test_obj = TestZmn(url)
    print(test_obj.login("tianhy", "123qwe"))
    print(test_obj.login("tianhy23", "123qwe"))
    print(test_obj.user_myaccount())
    print(test_obj.project())
    print(test_obj.project(method='PUT'))
    print(test_obj.project(status="进行中"))
    print(test_obj.user())
