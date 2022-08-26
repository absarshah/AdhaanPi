# AdhaanPi

This script (designed basically for the Raspberry Pi, but can run on most platforms) checks prayer times once a day using the Al-Adhan API with user-selectable settings. It then plays the Adhan of choice at each of the prayer times through the speakers. In addition, users can opt-in for a once-a-day notification regarding the current Hijri date, as well as the last update of prayer times.

The script includes the possibility to manually or automatically trigger the daily announcement besides the fixed (user-selectable) daily time.
The announcement can be triggered by creating a blank "trigger.txt" file in the same path as the script. The script will delete the trigger file after executing it once. 
Personally I use a software switch in my HomeKit environment to create the trigger.txt file on the raspberry pi (via homebridge), which triggers the announcement.

#Installation

There is no installation process for the script. Simply place the Adhan.py file on your device in a separate folder (recommended simply for good housekeeping). Required dependencies must be installed on your system in order to run the script, which include sox and gtts.

Before first use, please update the settings in the .py file. Particularly important is to update the path to wherever on your device you place the script - this is used for the creation and playback of the text-to-speech daily notifications as well as the Adhaan audio. Please note that this is a "bring your own Adhaan" project - Adhaan audio file is not included :)

It is also recommended to run the script in the background, either using "nohup" or by running the script as a service. Easy instructions for running a script as a service can be found here:
https://www.nerdynat.com/programming/2019/run-python-on-your-raspberry-pi-as-background-service/
