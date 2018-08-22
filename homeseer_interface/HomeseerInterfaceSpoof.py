from .HomeseerInterface import HomeseerInterface, HomeSeerCommandException
from mycroft.util.log import LOG

class HomeseerInterfaceSpoof(HomeseerInterface):
    def __init__(self, *args):
        super().__init__(*args)
        self._status = {
            "Name": "HomeSeer Devices",
            "Version": "1.0",
            "Devices": [
                {
                    "ref": 3398,
                    "name": "Temperature",
                    "location": "Z-Wave",
                    "location2": "Node 122",
                    "value": 82,
                    "status": "82 F",
                    "device_type_string": "Z-Wave Temperature",
                    "last_change": "\/Date(1410193983884)\/",
                    "relationship": 4,
                    "hide_from_view": False,
                    "associated_devices": [
                        3397
                    ],
                    "device_type": {
                        "Device_API": 16,
                        "Device_API_Description": "Thermostat API",
                        "Device_Type": 2,
                        "Device_Type_Description": "Thermostat Temperature",
                        "Device_SubType": 1,
                        "Device_SubType_Description": "Temperature"
                    },
                    "device_image": ""
                },
                {
                    "ref": 3570,
                    "name": "Switch Binary",
                    "location": "Z-Wave",
                    "location2": "Node 124",
                    "value": 255,
                    "status": "On",
                    "device_type_string": "Z-Wave Switch Binary",
                    "last_change": "\/Date(1410196540597)\/",
                    "relationship": 4,
                    "hide_from_view": False,
                    "associated_devices": [
                        3566
                    ],
                    "device_type": {
                        "Device_API": 4,
                        "Device_API_Description": "Plug-In API",
                        "Device_Type": 0,
                        "Device_Type_Description": "Plug-In Type 0",
                        "Device_SubType": 37,
                        "Device_SubType_Description": ""
                    },
                    "device_image": ""
                }
            ]
        }

    def _send_command(self, url: str):
        LOG.info("Calling {}".format(url))

    def get_status(self, ref="", location="", location2=""):
        if len(ref):
            for d in self._status["Devices"]:
                if d["ref"] == int(ref):
                    return d
            raise HomeSeerCommandException("Device with ref {} not found in status".format(ref))
        else:
            return self._status

    def control_by_value(self, deviceref: int, value: float):
        pass

    def control_by_label(self, deviceref: int, label: str):
        pass

    def run_event_by_group(self, group_name: str, event_name: str):
        pass

    def run_event_by_event_id(self, event_id):
        pass
