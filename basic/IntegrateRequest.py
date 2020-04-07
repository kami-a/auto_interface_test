#!/usr/bin/env python
# 多种请求方法集成

import requests
import json

class IntegrateRequest(object):
    # 请求 request方法
    def get_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.get(url, json=data, headers=header)
        else:
            res = requests.get(url, json=data)
        return res.json()

    # post 请求方式
    def post_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.post(url=url, json=data, headers=header)
        else:
            res = requests.post(url=url, json=data)
        try:
            return res.json()
        except json.JSONDecodeError as e:
            return None

    # delete 请求方式
    def delete_req(self, url, data=None, header=None):
        if header is not None:
            res = requests.delete(url, json=data, headers=header)
        else:
            res = requests.delete(url, json=data)
        return res.json()

    def main_req(self, method, url, data, header):
        if method == "get" or method == "GET":
            res = self.get_req(url, data, header)
        elif method == "post" or method == "POST":
            res = self.post_req(url, data, header)
        elif method == "delete" or method == "DELETE":
            res = self.delete_req(url, data, header)
        else:
            res = "你的请求方式暂未开放，请耐心等待"
        return json.dumps(res, ensure_ascii=False, indent=4, sort_keys=True)


if __name__ == "__main__":
    ir = IntergrateRequest()
    # get_method = 'get'
    # get_url = 'http://127.0.0.1:8000/query_article/'
    # get_data = None
    # get_header = None
    # print(ir.main_req(get_method, get_url, get_data, get_header))

    post_method = 'post'
    post_url = 'http://127.0.0.1:8000/add_article/'
    post_payload = {
        "title": "title54",
        "content": "content54",
    }
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Accept": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
        "X-Token": "0a6db4e59c7fff2b2b94a297e2e5632e",
    }
    ir.main_req(post_method, post_url, post_payload, headers)

    # modify_method = 'post'
    # modify_url = 'http://127.0.0.1:8000/modify_article/49'
    # modify_payload = {
    #     "title": "title149_m",
    #     "content": "content49_m",
    # }
    # headers = {
    #     "Content-Type": "application/json; charset=utf-8",
    #     "Accept": "application/json",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
    #     "X-Token": "0a6db4e59c7fff2b2b94a297e2e5632e",
    # }
    # ir.main_req(modify_method, modify_url, modify_payload, headers)

    # delete_method = 'delete'
    # delete_url = 'http://127.0.0.1:8000/delete_article/5'
    # delete_payload = {
    #     "title": "title5",
    #     "content": "content5",
    # }
    # headers = {
    #     "Content-Type": "application/json; charset=utf-8",
    #     "Accept": "application/json",
    #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3730.400 QQBrowser/10.5.3805.400",
    #     "X-Token": "0a6db4e59c7fff2b2b94a297e2e5632e",
    # }
    # print(ir.main_req(delete_method, delete_url, delete_payload, headers))
