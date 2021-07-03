import datetime
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
            #r.raise_for_status()  # it won't allow to save other status codes
            return response
        except:
            raise ConnectionError("unable to connect")

    @staticmethod
    def is_regexp_matching(regular_expression, content):
        #print(regular_expression)
        try:
            out = re.match(regular_expression, content)  # check this !!! previously: re.search
            #print(out)
        except:
            return "", ""
        if out and regular_expression != '':
            return True, out.group()  # the second return is the matching string
        elif regular_expression == '':
            return None, None
        else:
            return False, ""

    @staticmethod
    def save_ping_data(url, status_code, response_time, regexp, is_regexp_matching, matching_details):
        url_ping = Url.objects.create(link=url, status=status_code, response_time=response_time,
                                      regexp=regexp, regexp_match=is_regexp_matching, match_details=matching_details)
        url_ping.save()


if __name__ == '__main__':
    url = 'http://google.com/'
    try:
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        respTime = str(round(r.elapsed.total_seconds(), 2))
        currDate = datetime.datetime.now()
        currDate = str(currDate.strftime("%d-%m-%Y %H:%M:%S"))
        print(currDate + " " + respTime)
    except requests.exceptions.HTTPError as err01:
        print("HTTP error: ", err01)
    except requests.exceptions.ConnectionError as err02:
        print("Error connecting: ", err02)
    except requests.exceptions.Timeout as err03:
        print("Timeout error:", err03)
    except requests.exceptions.RequestException as err04:
        print("Error: ", err04)

    print(r.status_code)