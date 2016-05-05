# -*- coding:utf-8 -*-

# import urllib2.request
# import urllib.request
import http.cookiejar
import urllib
# import urllib2
# import urllib.parse
import json
import configparser


# 配置类
class ConfigHttp:
    '''配置要测试接口服务器的ip、端口、域名等信息，封装http请求方法，http头设置'''

    def __init__(self, ini_file):
        config = configparser.ConfigParser()

        # 从配置文件中读取接口服务器IP、域名，端口
        config.read(ini_file)
        self.host = config['HTTP']['host']
        self.port = config['HTTP']['port']
        self.headers = {}  # http 头

        #install cookie
        cj = http.cookiejar.CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        urllib.request.install_opener(opener)

    def set_host(self, host):
        self.host = host

    def get_host(self):
        return self.host

    def set_port(self, port):
        self.port = port

    def get_port(self):
        return  self.port

    # 设置http头
    def set_header(self, headers):
        self.headers = headers

    # 封装HTTP GET请求方法
    def get(self, url, params):
        if params=='':
            params=params
        else:
                params = urllib.parse.urlencode(eval(params))
        # params = urllib.parse.urlencode(eval(params))  # 将参数转为url编码字符串
        url = 'http://' + self.host + ':' + str(self.port)  + url + params
        request = urllib.request.Request(url, headers=self.headers)

        try:
            response = urllib.request.urlopen(request)
            response = response.read().decode('utf-8')  ## decode函数对获取的字节数据进行解码
            json_response = json.loads(response)  # 将返回数据转为json格式的数据
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装HTTP POST请求方法
    def post(self, url, data):
        # data = json.dumps(eval(data))
        # data = data.encode('utf-8')
        url = 'http://' + self.host + ':' + str(self.port) + url
        data_urlencode = urllib.parse.urlencode(eval(data)).encode('utf-8')
        try:
            request = urllib.request.Request(url,data_urlencode, headers=self.headers)
            # response = urllib.request.urlopen(request)
            response = urllib.request.urlopen(request)
            response = response.read().decode('utf-8')
            json_response = json.loads(response)
            return json_response
        except Exception as e:
            print('%s' % e)
            return {}

    # 封装HTTP xxx请求方法
    # 自由扩展