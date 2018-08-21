# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

import json
from collections import namedtuple
from fuzzywuzzy import fuzz

import requests

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

Device = namedtuple('Device', 'ref name location location2')


class HomeSeerCommandException(Exception):
    pass


class HomeSeerSkill(MycroftSkill):
    TIMEOUT = 2

    # The constructor of the skill, which calls MycroftSkill's constructor

    def __init__(self):
        super(HomeSeerSkill, self).__init__(name="HomeSeerSkill")

        self.url = self.config.get('url')
        self.device_list = []

    def initialize(self):
        supported_languages = ["en-US"]

        if self.lang not in supported_languages:
            self.log.warning("Unsupported language for {}, shutting down skill".format(self.name))
            self.shutdown()

        # Get HomeSeer devices from status query
        try:
            for d in self._get_status()["Devices"]:
                self.device_list.append(Device(d["ref"], d["name"], d["location"], d["location2"]))
        except HomeSeerCommandException:
            self.log.warning("Unable to connect to HomeSeer. Shutting down.")
            self.shutdown()

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

    def _get_status(self, ref="", location="", location2=""):
        url = self.url + "/JSON?request=getstatus"
        if len(ref) > 0:
            url += "&ref={}".format(ref)
        if len(location) > 0:
            url += "&location1={}".format(location)
        if len(location2) > 0:
            url += "&location2={}".format(location2)
        return self._send_command(url)

    def _control_by_value(self, deviceref: int, value: float):
        url = self.url + "/JSON?request=controldevicebyvalue&ref={}&value={}".format(str(deviceref), str(value))
        response = self._send_command(url)

    def _control_by_label(self, deviceref: int, label: str):
        url = self.url + "/JSON?request=controldevicebylabel&ref={}&label={}".format(str(deviceref), label)
        response = self._send_command(url)

    def _run_event_by_group(self, group_name: str, event_name: str):
        url = self.url + "/JSON?request=runevent&group={}&name={}".format(group_name, event_name)
        response = self._send_command(url)

    def _run_event_by_event_id(self, event_id):
        url = self.url + "/JSON?request=runevent&id={}".format(str(event_id))
        response = self._send_command(url)

    def get_device_by_attributes(self, name, location="", location2=""):
        best_score = 0
        score = 0
        best_device = None

        for device in self.device_list:
            score = fuzz.ratio(name, device.name) + fuzz.ratio(location, device.location) + \
                    fuzz.ratio(location2, device.location2)
            if score > best_score:
                best_score = score
                best_device = device

        return best_device

    @intent_handler(IntentBuilder("").require("GetStatus").require("Device").optionally("Location1")
                    .optionally("Location2"))
    def handle_get_status_intent(self, message):
        name = message.data["Device"]
        location = message.data["Location"]
        location2 = message.data["Location2"]

        device: Device = self.get_device_by_attributes(name, location, location2)
        status_json = self._get_status(device.ref, device.location, device.location2)
        status_string = status_json["status"]

        self.speak_dialog('DeviceStatus', {'name': device.name,
                                           'value': status_string})

    # The "stop" method defines what Mycroft does when told to stop during
    # the skill's execution. In this case, since the skill's functionality
    # is extremely simple, there is no need to override it.  If you DO
    # need to implement stop, you should return True to indicate you handled
    # it.
    #
    # def stop(self):
    #    return False


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return HomeSeerSkill()
