"""
Simple HTTP Connection Library
"""

import uuid
import urllib
import urllib2
import hashlib
import urlparse
import cookielib
import mimetypes


class MyHTTPErrorProcessor(urllib2.HTTPErrorProcessor):

    def http_response(self, request, response):
        code, msg, headers = response.code, response.msg, response.info()
        
        if code == 302: return response

        if not (200 <= code < 300):
            response = self.parent.error('http', request, response, code, msg, headers)
        return response

    https_response = http_response


class HTTPConnect:

    def __init__(self, url, redirect = True, debug = False, verbose = False):
        
        self.url = url
        self.redirect = redirect
        self.debug = debug
        self.verbose = verbose
        self.headers = dict()

        self.__debug_print('[*] URL: ' + url)
        self.__connect()
        

    def __connect(self):
        """Init Connection"""
        
        self.__debug_print('[*] Initialize Connection')
        
        self.cj = cookielib.CookieJar()
        http_handler = urllib2.HTTPHandler(debuglevel=1)
        https_handler = urllib2.HTTPSHandler(debuglevel=1)
        cookie_handler = urllib2.HTTPCookieProcessor(self.cj)

        if self.redirect == False and self.verbose:
            self.opener = urllib2.build_opener(http_handler, https_handler, MyHTTPErrorProcessor, cookie_handler)
        elif self.verbose:
            self.opener = urllib2.build_opener(http_handler, https_handler, MyHTTPErrorProcessor, cookie_handler)
        elif self.redirect == False:
            self.opener = urllib2.build_opener(MyHTTPErrorProcessor, cookie_handler)
        else:
            self.opener = urllib2.build_opener(cookie_handler)
    

    def add_header(self, key, value):
        """Add a HTTP Header"""
        
        self.__debug_print('[*] Add Header: ' + key + ': ' + value)

        self.headers[key] = value


    def add_cookie(self, name, value):
        """Add a Cookie"""

        self.__debug_print('[*] Add Cookie: ' + name + '=' + value)

        url_parse = urlparse.urlparse(self.url)
        
        cookie = cookielib.Cookie(version=0, name=name, value=value,
                                  expires=None, port=None, port_specified=False,
                                  domain=url_parse.hostname, domain_specified=True, domain_initial_dot=False,
                                  path='/', path_specified=True, secure=False,
                                  discard=False, comment=None, comment_url=None,
                                  rest={'HttpOnly': False}, rfc2109=False)
        self.cj.set_cookie(cookie)


    def add_handler(self, handler):
        """Add a Handler"""

        self.__debug_print('[*] Add Handler: ' + str(handler))
        self.opener.add_handler(handler)


    def read_cookies(self):
        """Read Cookies"""

        cookies = dict()
        for cookie in self.cj:
            cookies[cookie.name] = cookie.value

        return cookies
    

    def get(self, param = None):
        """HTTP Get Request"""

        if param:
            url = self.url + '?' + urllib.urlencode(param)
        else:
            url = self.url

        self.__debug_print('[*] Get: ' + url)

        tries = 3

        while tries:
            try:
                request = urllib2.Request(url, headers = self.headers)
                response = self.opener.open(request)
                return response.read()
            except Exception as e:
                self.__debug_print('[*] Get Error: ' + str(e))
                tries -= 1
        
        return None
    

    def post(self, data, param = None, multiform = False):
        """HTTP Post Request"""

        self.__debug_print('[*] Post: ' + self.url)
        self.__debug_print('[*] Data: ' + str(data))

        if param:
            url = self.url + '?' + urllib.urlencode(param)
        else:
            url = self.url

        if multiform:
            post_data = self.__multiform_encode(data)
        else:
            post_data = urllib.urlencode(data)

        tries = 3

        while tries:
            try:
                request = urllib2.Request(url, post_data, headers = self.headers)
                response = self.opener.open(request)
                return response.read()
            except Exception as e:
                self.__debug_print('[*] Get Error: ' + str(e))
                tries -= 1
        
        return None


    def __multiform_encode(self, data):
        """Generate multipart/form-data Data"""

        boundary = '-'*25 + hashlib.md5(str(uuid.uuid4())).hexdigest()
        content_type = 'multipart/form-data; boundary=' + boundary
        self.add_header('Content-Type', content_type)

        form_data = '--' + boundary + '\r\n'

        for key, value in data.items():
            if key != 'file':
                form_data += 'Content-Disposition: form-data; ' + 'name="' + key + '"' + '\r\n\r\n'
                form_data += value + '\r\n'
                form_data += '--' + boundary + '\r\n'
                
        for key, value in data.items():
            if key == 'file':
                form_data += 'Content-Disposition: form-data; ' + 'name="' + value['name'] + '"; filename="' + value['filename'] + '"\r\n'
                form_data += 'Content-Type: ' + (mimetypes.guess_type(value['filename'])[0] or 'application/octet-stream') + '\r\n\r\n'
                form_data += value['data'] + '\r\n'
                form_data += '--' + boundary + '--\r\n'

        self.__debug_print('[*] Multi Form:' + form_data)
        
        return form_data
    

    def __debug_print(self, message):
        """Print Debug Info"""

        if self.debug:
            print message


if __name__ == '__main__':

    pass