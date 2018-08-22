# Below is the list of outside modules you'll be using in your skill.
# They might be built-in to Python, from mycroft-core or from external
# libraries.  If you use an external library, be sure to include it
# in the requirements.txt file so the library is installed properly
# when the skill gets installed later by a user.

from collections import namedtuple
from fuzzywuzzy import fuzz

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.util.log import LOG

# from homeseer_interface.HomeseerInterface import HomeseerInterface, HomeSeerCommandException
from .homeseer_interface.HomeseerInterfaceSpoof import HomeseerInterfaceSpoof as HomeseerInterface, HomeSeerCommandException

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

Device = namedtuple('Device', 'ref name location location2')


class HomeSeerSkill(MycroftSkill):
    TIMEOUT = 2

    # The constructor of the skill, which calls MycroftSkill's constructor

    def __init__(self):
        super(HomeSeerSkill, self).__init__(name="HomeSeerSkill")

        self.hs = HomeseerInterface(self.config.get('url'))
        self.device_list = []

    def initialize(self):
        supported_languages = ["en-us"]

        if self.lang not in supported_languages:
            self.log.warning("Unsupported language ({}) for {}, shutting down skill".format(self.lang, self.name))
            self.shutdown()

        # Get HomeSeer devices from status query
        try:
            for d in self.hs.get_status()["Devices"]:
                self.device_list.append(Device(d["ref"], d["name"], d["location"], d["location2"]))
        except HomeSeerCommandException:
            self.log.warning("Unable to connect to HomeSeer. Shutting down.")
            self.shutdown()

    def get_device_by_attributes(self, detail: str):
        best_score = 0
        score = 0
        best_device = None

        for device in self.device_list:
            device_detail = " ".join(device)
            score = fuzz.ratio(detail, device_detail)
            if score > best_score:
                best_score = score
                best_device = device

        return best_device

    @intent_handler(IntentBuilder("").require("Detail"))
    def handle_get_status_intent(self, message):
        detail = message.data["Detail"]
        self.log.info("Getting status for {}...".format(detail))
        device: Device = self.get_device_by_attributes(detail)
        self.log.info("Device found: {}".format(device))
        status_json = self.hs.get_status(device.ref, device.location, device.location2)
        self.log.info("Device status: {}".format(status_json))
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
