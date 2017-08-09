from urllib.request import build_opener, HTTPCookieProcessor, Request
from urllib.parse import urlencode
from http.cookiejar import CookieJar
import ast
import re
import json
import six
import sys
from .help import byte_adaptor
from .help import js_adaptor
from .base import AbstractBaseExchange
class Nse(AbstractBaseExchange):
    
    __CODECACHE__ = None

    def __init__(self):
        self.opener = self.nse_opener()
        self.headers = self.nse_headers()
        self.get_quote_url = 'https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?'
        self.stocks_csv_url = 'http://www.nseindia.com/content/equities/EQUITY_L.csv'
        self.top_gainer_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/niftyGainers1.json'
        self.top_loser_url = 'http://www.nseindia.com/live_market/dynaContent/live_analysis/losers/niftyLosers1.json'
        self.nexttop_gainer_url ='http://www.nseindia.com/live_market/dynaContent/live_analysis/gainers/jrNiftyGainers1.json'

    def get_stock_codes(self, cached=True, as_json=False):
   
        url = self.stocks_csv_url
        req = Request(url, None, self.headers)
        res_dict = {}
        if cached is not True or self.__CODECACHE__ is None:
            # raises HTTPError and URLError
            res = self.opener.open(req)
            if res is not None:
                # for py3 compat covert byte file like object to
                # string file like object
                res = byte_adaptor(res)
                for line in res.read().split('\n'):
                    if line != '' and re.search(',', line):
                        (code, name) = line.split(',')[0:2]
                        res_dict[code] = name
                    # else just skip the evaluation, line may not be a valid csv
            else:
                raise Exception('no response received')
            self.__CODECACHE__ = res_dict
        return self.render_response(self.__CODECACHE__, as_json)


    def get_quote(self, code, as_json=False):
        """
        gets the quote for a given stock code
        :param code:
        :return: dict or None
        :raises: HTTPError, URLError
        """
        code = code.upper()
        if self.is_valid_code(code):
            url = self.build_url_for_quote(code)
            req = Request(url, None, self.headers)
            # this can raise HTTPError and URLError, but we are not handling it
            # north bound APIs should use it for exception handling
            res = self.opener.open(req)

            # for py3 compat covert byte file like object to
            # string file like object
            res = byte_adaptor(res)

            # Now parse the response to get the relevant data
            match = re.search(\
                        r'\{<div\s+id="responseDiv"\s+style="display:none">\s+(\{.*?\{.*?\}.*?\})',
                        res.read(), re.S
                    )
            # ast can raise SyntaxError, let's catch only this error
            try:
                buffer = match.group(1)
                buffer = js_adaptor(buffer)
                response = self.clean_server_response(ast.literal_eval(buffer)['data'][0])
            except SyntaxError as err:
                raise Exception('ill formatted response')
            else:
                return self.render_response(response, as_json)
        else:
            return None

    def get_top_gainers(self, as_json=False):
        """
        :return: a list of dictionaries containing top gainers of the day
        """
        url = self.top_gainer_url
        req = Request(url, None, self.headers)
        # this can raise HTTPError and URLError
        res = self.opener.open(req)
        res = byte_adaptor(res)
        res_dict = json.load(res)
        # clean the output and make appropriate type conversions
        res_list = [self.clean_server_response(item) for item in res_dict['data']]
        return self.render_response(res_list, as_json)

    def get_top_losers(self, as_json=False):
        """
        :return: a list of dictionaries containing top losers of the day
        """
        url = self.top_loser_url
        req = Request(url, None, self.headers)
        # this can raise HTTPError and URLError
        res = self.opener.open(req)
        res = byte_adaptor(res)
        res_dict = json.load(res)
        # clean the output and make appropriate type conversions
        res_list = [self.clean_server_response(item)
                    for item in res_dict['data']]
        return self.render_response(res_list, as_json)

    def getnext_top_gainers(self, as_json=False):
        """
        :return: a list of dictionaries containing top gainers of the day
        """
        url =self.nexttop_gainer_url
        req = Request(url, None, self.headers)
        # this can raise HTTPError and URLError
        res = self.opener.open(req)
        res = byte_adaptor(res)
        res_dict = json.load(res)
        # clean the output and make appropriate type conversions
        res_list = [self.clean_server_response(item) for item in res_dict['data']]
        return self.render_response(res_list, as_json)
    

    def is_valid_code(self, code):
        """
        :param code: a string stock code
        :return: Boolean
        """
        if code:
            stock_codes = self.get_stock_codes()
            if code.upper() in stock_codes.keys():
                return True
            else:
                return False    

    

    def nse_headers(self):
        """
        Builds right set of headers for requesting http://nseindia.com
        :return: a dict with http headers
        """
        return {'Accept' : '*/*',
                'Accept-Language' : 'en-US,en;q=0.5',
                'Host': 'nseindia.com',
                'Referer': "https://www.nseindia.com/live_market/dynaContent/live_watch/get_quote/GetQuote.jsp?symbol=INFY&illiquid=0&smeFlag=0&itpFlag=0",
                'User-Agent' : 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'X-Requested-With': 'XMLHttpRequest'
            }

    def nse_opener(self):
        """
        builds opener for urllib2
        :return: opener object
        """
        cj = CookieJar()
        return build_opener(HTTPCookieProcessor(cj))

    def build_url_for_quote(self, code):
        """
        builds a url which can be requested for a given stock code
        :param code: string containing stock code.
        :return: a url object
        """
        if code is not None and type(code) is str:
            encoded_args = urlencode([('symbol', code), ('illiquid', '0'), ('smeFlag', '0'), ('itpFlag', '0')])
            return self.get_quote_url + encoded_args
        else:
            raise Exception('code must be string')

    def clean_server_response(self, resp_dict):
        """cleans the server reponse by replacing:
            '-'     -> None
            '1,000' -> 1000
        :param resp_dict:
        :return: dict with all above substitution
        """

        # change all the keys from unicode to string
        d = {}
        for key, value in resp_dict.items():
            d[str(key)] = value
        resp_dict = d
        for key, value in resp_dict.items():
            if type(value) is str or isinstance(value, six.string_types):
                if re.match('-', value):
                    resp_dict[key] = None
                elif re.search(r'^[0-9,.]+$', value):
                    # replace , to '', and type cast to int
                    resp_dict[key] = float(re.sub(',', '', value))
                else:
                    resp_dict[key] = str(value)
        return resp_dict

    def render_response(self, data, as_json=False):
        if as_json is True:
            return json.dumps(data)
        else:
            return data

    def __str__(self):
        """
        string representation of object
        :return: string
        """
        return 'All classes for scrapping nse'
