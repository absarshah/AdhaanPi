# AdhaanPi
This script (designed basically for the Raspberry Pi, but can run on most platforms) checks prayer times once a day using the Al-Adhan API with user-selectable settings. It then plays the Adhan of choice at each of the prayer times through the speakers. In addition, users can opt-in for a once-a-day notification regarding the current Hijri date, as well as the last update of prayer times.

Please update the settings in the .py file before first use. Particularly important is to update the path to wherever on your device you place the script - this is used for the creation and playback of the text-to-speech daily notifications as well as the Adhaan audio. Please note that this is a "bring your own Adhaan" project - Adhaan audio file is not included :)

It is also recommended to run the script in the background, either using "nohup" or by running the script as a service. Easy instructions for running a script as a service can be found here:
https://www.nerdynat.com/programming/2019/run-python-on-your-raspberry-pi-as-background-service/
