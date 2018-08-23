To submit your skill, replace this file with text from 
https://rawgit.com/MycroftAI/mycroft-skills/master/meta_editor.html


## HomeSeer-Mycroft
HomeSeer hub integration for Mycroft Voice Assistant

## Configuration
Add the block below to your `mycroft.conf` file:

```json
  "HomeSeerSkill" : {
	"url": "HomeSeer server local IP",
	"username" : "Your HomeSeer account username. Put 'null' if local.",
	"password": "Your HomeSeer account password. Put 'null' if local."
  }
```

Remember to put `null` for username and password if your Homeseer is on the same LAN as your Mycroft.
Restart Mycroft for the changes to take effect.

## Description 
A port of the HomeSeer functionality from Alexa to Mycroft. Allows the user to interact with smart-objects using voice 
control. 

## Examples 
Use the syntax and examples below to construct phrases that will control and obtain status from HomeSeer
devices.
* “{Attention Phrase} {Command} {Location 2} {Location 1} {Device Name}“

###### Controlling HomeSeer Devices
* “{Mycroft} {Turn on the} {Light}“
* “{Mycroft} {Turn on the} {Bathroom} {Light}“
* “{Mycroft} {Turn on the} {First Floor} {Bathroom} {Light}“
* “{Mycroft} {Unlock the} {Door Lock}“
* “{Mycroft} {Unlock the} {Kitchen} {Door Lock}“
* “{Mycroft} {Unlock the} {First Floor} {Kitchen} {Door Lock}“
* “{Mycroft} {Set the} {Outside Lights} {to 50%}“
* “{Mycroft} {Set the} {Kitchen} {Outside Lights} {to 50%}“
* “{Mycroft} {Set the} {First Floor} {Kitchen} {Outside Lights} {to 50%}“
###### Controlling “All” HomeSeer Devices
* “{Mycroft} {Turn on all the} {Lights}“
* “{Mycroft} {Turn on all the} {Living Room} {Lights}“
* “{Mycroft} {Set all} {Living Room} {Lights} {to 50%}“
* “{Mycroft} {Turn off all the} {First Floor} {Lights}“
###### Obtaining Status From HomeSeer Devices
* “{Mycroft} {Get the status of the} {Door Lock}“
* “{Mycroft} {Get the status of the} {Kitchen} {Door Lock}“
* “{Mycroft} {Get the status of the} {First Floor} {Kitchen} {Door Lock}“
###### Working with Events
Syntax and examples below are example phrases that will launch HomeSeer events.
* “{Attention Phrase} {Command} {Event Name} {Command}“
###### Launching HomeSeer Events
* “{Mycroft} {Run the Event} {Turn all lights off}“
* “{Mycroft} {Run the} {Turn all lights off} {Event}“
## Credits 
Sawyer McLane
