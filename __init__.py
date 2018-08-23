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

from .homeseer_interface.HomeseerInterface import HomeseerInterface, HomeSeerCommandException
# from .homeseer_interface.HomeseerInterfaceSpoof import HomeseerInterfaceSpoof as HomeseerInterface, \
#     HomeSeerCommandException

# Each skill is contained within its own class, which inherits base methods
# from the MycroftSkill class.  You extend this class as shown below.

Device = namedtuple('Device', 'ref name location location2')


class HomeSeerSkill(MycroftSkill):
    TIMEOUT = 2

    # The constructor of the skill, which calls MycroftSkill's constructor

    def __init__(self):
        super(HomeSeerSkill, self).__init__(name="HomeSeerSkill")

        self.hs = HomeseerInterface(self.config.get('url'), "demo@homeseer.com", "demo100")
        self.device_list = []

    def initialize(self):
        supported_languages = ["en-us"]

        if self.lang not in supported_languages:
            self.log.warning("Unsupported language ({}) for {}, shutting down skill".format(self.lang, self.name))
            self.shutdown()

        # Get HomeSeer devices from status query
        try:
            for d in self.hs.get_status()["Devices"]:
                self.device_list.append(Device(str(d["ref"]), d["name"], d["location"], d["location2"]))
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

    def get_devices_by_attribute(self, root_device: Device, attribute: str):
        root_attr = getattr(root_device, attribute)
        return [d for d in self.device_list if getattr(d, attribute) == root_attr]

    @intent_handler(IntentBuilder("").require("StatusDetail"))
    def handle_get_status_intent(self, message):
        detail = message.data["StatusDetail"]
        device: Device = self.get_device_by_attributes(detail)
        try:
            status_json = self.hs.get_status(device.ref, device.location, device.location2)
            status_string = status_json["status"]

            self.speak_dialog('DeviceStatus', {'name': device.name,
                                               'value': status_string})
        except HomeSeerCommandException as e:
            self.speak_dialog('Error', {'exception': str(e)})

    @intent_handler(IntentBuilder("").require("ToggleSetting").require("ToggleSingleDetail"))
    def handle_turn_setting_intent(self, message):
        detail = message.data["ToggleSingleDetail"]
        setting = message.data["ToggleSetting"]
        self.log.info("Setting details {} to {}".format(detail, setting))
        device: Device = self.get_device_by_attributes(detail)
        self.speak_dialog('ToggleSingle', {'setting': setting,
                                           'name': device.name})
        try:
            self.hs.control_by_label(device.ref, setting)
        except HomeSeerCommandException as e:
            self.speak_dialog('Error', {'exception': str(e)})

    @intent_handler(IntentBuilder("").require("AllKeyword").require("ToggleSetting").require("ToggleSingleDetail"))
    def handle_turn_setting_all_intent(self, message):
        detail = message.data["ToggleSingleDetail"]
        setting = message.data["ToggleSetting"]
        self.log.info("Setting ALL details {} to {}".format(detail, setting))
        root_device: Device = self.get_device_by_attributes(detail)
        self.speak_dialog('ToggleAll', {'setting': setting,
                                        'name': root_device.name})
        devices = self.get_devices_by_attribute(root_device, 'name')
        for d in devices:
            try:
                self.hs.control_by_label(d.ref, setting)
            except HomeSeerCommandException as e:
                self.speak_dialog('Error', {'exception': str(e)})

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
