#!/usr/bin/python

# Check status of AP on Fortinet WLC(is AP connected to WLC)
#
# Example call:
# python check_fortiwlc_ap.py --url "https://wlc.nekaj.si" -l "admin" -p "password" --ap w1-s.nekaj.si
#

import requests
import logging
import json
from pynag.Plugins import (
    PluginHelper,
    ok,
    warning,
    critical,
    unknown,
)

logger = logging.getLogger(__name__)


class FortiWlc(object):

    HEADERS = {"Accept": "text/xml; version=1.0"}

    def __init__(
        self,
        url="http://localhost/wlc/",
        username="admin",
        password="password",
        verify=True,
    ):
        self.url = url
        self.username = username
        self.password = password
        self.verify = verify
        self._session = requests.session()
        self._cookies = None
        self._set_headers()


    def _set_headers(self):
        self._headers = self.HEADERS

    def _login(self):

        login_url = self.url + "/logincheck"
        username = self.username
        password = self.password
        params = {
            "username": username,
            "secretkey": password,
            "ajax": 1,
        }
        response = self._session.post(
            login_url, params=params
        )
        self.test_response = response.text
        if response.text[:1] == "1":
            logger.info(
                "Logged into Fortinet with username %s"
                % username
            )
            return response.cookies
        else:
            raise AttributeError(
                "Denied access: %s" % response
            )

    def _get_cookies(self, clear_cache=False):
        if clear_cache:
            self._cookies = self._login()
            return self._cookies
        else:
            if not self._cookies:
                self._cookies = self._login()
                return self._cookies

    def logout(self):
        url = self.url + "/logout"
        res = self._session.post(url)

    def get(self, resource):
        url = self.url + resource
        response = self._session.get(
            url, cookies=self._get_cookies()
        )
        if response.status_code == 401:
            raise AttributeError(
                "Denied access: %s" % response
            )
        return response

    def get_ap_info(self, ap):


        r = self.get(
            "/api/v2/monitor/wifi/managed_ap/select/"
        )
        json_data = json.loads(r.text)
        result = ""
        for data in json_data["results"]:
            if data["name"] == ap:
                result = "known AP"
                return data
        if result == "" :
             return {"status":"","state":""}




def main():
    helper = PluginHelper()
    helper.parser.add_option(
        "-H",
        help="Check if AP is connected to Fortinet WLC",
    )
    helper.parser.add_option(
        "-l", help="Username to login with", dest="username"
    )
    helper.parser.add_option(
        "-p", help="Password to login with", dest="password"
    )
    helper.parser.add_option(
        "--url", help="url address of WLC", dest="wlc"
    )
    helper.parser.add_option(
        "--ap", help="FQDN of AP", dest="ap"
    )
    helper.parse_arguments()
    username = helper.options.username
    password = helper.options.password
    wlc = helper.options.wlc
    ap = helper.options.ap
    wlc = FortiWlc(wlc, username, password, ap)
    info = wlc.get_ap_info(ap)
    wlc.logout()
    s = get_ap_status(info)
    helper.status(s["status"])
    helper.add_summary(s["add_summary"])
    helper.check_all_metrics()
    helper.exit()
    
def get_ap_status( data):
    helper = {
        "status": "unknown",
        "add_summary": "Unrecognized result from WLC",
    }
    if "disconnected" in data["status"] and (
        "authorized" in data["state"]
        or "discovered" in data["state"]
    ):
        helper["status"] = critical
        helper[
            "add_summary"
        ] = "Communication between AP and WLC does not work"

    elif (
        "authorized" in data["state"]
        and "connected" in data["status"]
    ):

        helper["status"] = ok
        helper[
            "add_summary"
        ] = "Communication between AP and WLC is OK"

    elif (
        "discovered" in data["state"]
        and "connecting" in data["status"]
    ):

        helper["status"] = warning
        helper[
            "add_summary"
        ] = "WLC does not know this AP and AP wants to communicate with WLC, and WLC ignores it"

    elif (
        "discovered" in data["state"]
        and "connected" in data["status"]
    ):
        helper["status"] = warning
        helper[
            "add_summary"
        ] = "WLC does not know this AP "

    elif (
        "connecting" in data["status"]
        and "authorized" in data["state"]
    ):
        helper["status"] = warning
        helper[
            "add_summary"
        ] = "AP wants to communicate with WLC, but WLC ignores it"

    else:
        helper["status"] = "Unkown"
        helper[
            "add_summary"
        ] = "Unrecognized result from WLC"
    return helper

if __name__ == "__main__":
    main()
