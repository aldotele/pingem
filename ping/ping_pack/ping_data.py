import requests
from ping.models import Url
import re


class Ping:
    def __init__(self, url):
        self.resp = Ping.connect_attempt(url)
        self.status = self.resp.status_code
        self.response_time = str(round(self.resp.elapsed.total_seconds(), 2))
        self.content = self.resp.text

    def get_ping_data(self):
        return self.status, self.response_time, self.content

    @staticmethod
    def connect_attempt(url):
        try:
            response = requests.get(url, timeout=6)
            # r.raise_for_status()  # this would not allow to save other status codes
            return response
        except:
            raise ConnectionError("unable to connect")  # unsuccessful connection attempts will raise the same error

    @staticmethod
    def is_regexp_matching(regular_expression, content):
        try:
            out = re.match(regular_expression, content)
        except:
            return "", ""  # case of not valid regex
        if out and regular_expression != '':  # case of matching pattern found
            return True, out.group()  # the second return is the matching string
        elif regular_expression == '':  # case of regex not provided
            return None, None
        else:
            return False, ""  # case of not matching pattern

    @staticmethod
    def save_ping_data(url, status_code, response_time, regexp, is_regexp_matching, matching_details):
        url_ping = Url.objects.create(link=url,
                                      status=status_code,
                                      response_time=response_time,
                                      regexp=regexp,
                                      regexp_match=is_regexp_matching,
                                      match_details=matching_details)
        url_ping.save()
