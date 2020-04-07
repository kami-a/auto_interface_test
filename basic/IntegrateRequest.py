
import requests
import json

class IntegrateRequest(object):
    # get 请求方式
    def get_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.get(url, json=data, headers=header)
        else:
            res = requests.get(url, json=data)
        return res
        
    # post 请求方式
    def post_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.post(url=url, json=data, headers=header)
        else:
            res = requests.post(url=url, json=data)
        return res

    # delete 请求方式
    def delete_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.delete(url, json=data, headers=header)
        else:
            res = requests.delete(url, json=data)
        return res

    # options 请求方式
    def options_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.options(url, json=data, headers=header)
        else:
            res = requests.options(url, json=data)
        return res

    def main_req(self, method, url, data, header):
        if method == "get" or method == "GET":
            res = self.get_req(url, data, header)
        elif method == "post" or method == "POST":
            res = self.post_req(url, data, header)
        elif method == "delete" or method == "DELETE":
            res = self.delete_req(url, data, header)
        elif method == "options" or method == "OPTIONS":
            res = self.options_req(url,data,header)
        else:
            res = "你的请求方式暂未开放，请耐心等待"
        return res
