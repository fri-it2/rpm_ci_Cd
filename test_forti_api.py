import responses
import unittest
import json
from pynag.Plugins import (
    PluginHelper,
    ok,
    warning,
    critical,
    unknown,
)
from check_fortiwlc_ap import FortiWlc
from check_fortiwlc_ap import get_ap_status


class TestFortiWlclogin(unittest.TestCase):
    @responses.activate
    def test_login_in(self):
        """ Test succesfull login with username and password """
        url = "https://wlc.local.si/logincheck?username=admin&secretkey=geslo&ajax=1"

        responses.add(
            responses.POST,
            url,
            body='1document.location="/ng/prompt?viewOnly&redir=%2Fng%2F";',
            status=200,
            adding_headers={
                "set-cookie": "foo=bar; "
            },
        )

        wlc = FortiWlc(
            url="https://wlc.local.si",
            username="admin",
            password="geslo",
        )
        jar = ['foo', ]
        wlc_data = wlc._login()
        self.assertEqual(len(responses.calls), 1)
        self.assertEqual(wlc_data.keys(), jar)

    @responses.activate
    def test_get_ap_info(self):
        """ Test succesfull API call for AP """

        url = "https://wlc.localhost.si/api/v2/monitor/wifi/managed_ap/select/"
        response_data = json.load(
            open("nekaj.json")
        )
        data = json.load(open("w1-nekaj.json"))
        responses.add(
            responses.GET,
            url,
            json=response_data,
            status=200,
        )

        url_login = "https://wlc.localhost.si/logincheck?username=admin&secretkey=geslo&ajax=1"

        responses.add(
            responses.POST,
            url_login,
            body='1document.location="/ng/prompt?viewOnly&redir=%2Fng%2F";',
            status=200,
        )
        url_logout = "https://wlc.localhost.si/logout"
        responses.add(
            responses.POST, url_logout, status=200
        )

        wlc = FortiWlc(
            url="https://wlc.localhost.si",
            username="admin",
            password="geslo",
        )

        wlc_data = wlc.get_ap_info(
            "w1.nekaj.si"
        )

        self.assertEqual(len(responses.calls), 2)
        self.assertEqual(wlc_data, data)


class TestCheckFortiWlcAp(unittest.TestCase):
    def test_get_ap_info(self):
        """ Test status of AP"""

        data = json.load(open("wnekaj.json"))
        response_helper = {
            "status": ok,
            "add_summary": "Communication between AP and WLC is OK",
        }
        wlc_data = get_ap_status(data)
        self.assertEqual(wlc_data, response_helper)


if __name__ == "__main__":
    unittest.main()
