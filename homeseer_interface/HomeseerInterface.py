import requests


class HomeSeerCommandException(Exception):
    pass


class HomeseerInterface:
    TIMEOUT = 2

    def __init__(self, url):
        self.url = url

    def _send_command(self, url: str):
        try:
            website = requests.get(url, timeout=self.TIMEOUT)
            website.close()
        except requests.exceptions.ConnectionError as detail:
            raise requests.exceptions.ConnectionError("Could not connect to HomeSeer. "
                                                      "Ensure service is running and IP address is correct.")
        if website.text == "error":
            raise HomeSeerCommandException()
        return website.json()

    def get_status(self, ref="", location="", location2=""):
        url = self.url + "/JSON?request=getstatus"
        if len(ref) > 0:
            url += "&ref={}".format(ref)
        if len(location) > 0:
            url += "&location1={}".format(location)
        if len(location2) > 0:
            url += "&location2={}".format(location2)
        return self._send_command(url)

    def control_by_value(self, deviceref: int, value: float):
        url = self.url + "/JSON?request=controldevicebyvalue&ref={}&value={}".format(str(deviceref), str(value))
        response = self._send_command(url)
        return response

    def control_by_label(self, deviceref: int, label: str):
        url = self.url + "/JSON?request=controldevicebylabel&ref={}&label={}".format(str(deviceref), label)
        response = self._send_command(url)
        return response

    def run_event_by_group(self, group_name: str, event_name: str):
        url = self.url + "/JSON?request=runevent&group={}&name={}".format(group_name, event_name)
        response = self._send_command(url)
        return response

    def run_event_by_event_id(self, event_id):
        url = self.url + "/JSON?request=runevent&id={}".format(str(event_id))
        response = self._send_command(url)
        return response
