################################################################################################################
#
# AdhaanPi
# Prayer time alarms for RaspberryPi
# Written by Absar Shah
# version August 2022
#
# This script checks prayer times once a day using the Al-Adhan API (user-selectable settings possible below).
# It then plays the Adhan of choice at each of the prayer times through the speakers. In addition, users can
# opt-in for a once-a-day notification regarding the current Hijri date, as well as the last update of
# prayer times.
#
# Libraries sox, gtts must be installed on your device. 
#
# The script should either be run using "nohup" to keep it running in the background, or alternativela as 
# a background service using systemctl.
#
# This scrpt would not have been possible without the use of the Al-Adhan API below (www.aladhan.com), 
# as well as the inspiration from the work by Abdulrahman Sahloul on instructables. Jazak Allah. 
#
# Please feel free to modify and use for your own purposes. In case of an improvement to the script 
# that helps the community, please share onwards
#
################################################################################################################



# Import libraries

import urllib.request
import requests
import os, sys
import gtts
import time
import ast

from datetime import date
from playsound import playsound
from datetime import datetime


###################################################
############## USER DEFINED SETTINGS ##############
###################################################

# Define locale (Düsseldorf, Germany), Calculation method (UOIF) and Asr calculation method (Hanafi)
City = "Dusseldorf"
Country = "Germany"
Method = "12" # See list at bottom of script
School = "1" # "0" for Safa'i and "1" for Hanafi
checkInterval = 1 # Time in seconds between checking for current prayer time

# Define for which prayers you need Azaan playback
azaanFajr = 0
azaanDhuhr = 1
azaanAsr = 1
azaanMaghrib = 1
azaanIsha = 1

# Azaan file details
azaanFile = 'tunis.mp3'

# Audio playback details for Azaan
aTempo = "1.1"
aGain = "-4"


# Define if you want a daily announcement 
announcement = 1		# Do a daily announcement? 1 = yes, 0 = no
announcementTime = "07:45" 	# when should the announcement happen in 24h format HH:MM

# Audio playback details for daily announcement
dTempo = "1.1"
dGain = "-3"

# !!!! IMPORTANT !!!!
# Please enter the path to the location of the script on your device
# This is especially important in case you run this script as a service
scriptPath = "/var/lib/homebridge/Adhan/"

# Housekeeping
URL = "http://api.aladhan.com/v1/timingsByCity?city=" + City + "&country=" + Country + "&method=" + Method + "&school=" + School
today = date.today()
runToday = 0
announced = 0


###################################################
############### MAIN PROGRAM STARTS ###############
###################################################

while (1):
	# Fetch prayer times once a day, in addition to todays Hijra date
	nToday = date.today()
	if (today != nToday) or (runToday == 0):
		# Use aladhan API to get prayer times
		x = requests.get(URL)
		prayerTimesGet = x.text

		# Convert string to dictionary
		prayerTimesRaw = ast.literal_eval(prayerTimesGet)

		# Get to the dictionary elements defining prayer times
		prayerTimesData = prayerTimesRaw['data']
		prayerTimes = prayerTimesData['timings']

		# Get to the dictionary elements defining Hijra date
		prayerTimesDate = prayerTimesData['date']
		prayerTimesForDate = prayerTimesDate['readable'] # Used in announcement
		todayHijri = prayerTimesDate['hijri']
		todayHijriM = todayHijri['month'] 
		todayHijriMonth = todayHijriM['en'] # Used in announcement
		todayHijriDay = todayHijri['day'] # Used in announcement

		# Set new date flag
		today = nToday
		runToday = 1
		announced = 0

	# Get current time
	cTime = time.localtime()
	currTime = time.strftime("%H:%M", cTime)

	# Check if current time matches with a prayer time, and if user has opted to play the Azaan during this time
	if ((currTime ==  prayerTimes['Fajr']) and (azaanFajr == 1)):
		os.system("play " + scriptPath + azaanFile + " tempo " + aTempo + " gain " + aGain)

	if ((currTime ==  prayerTimes['Dhuhr']) and (azaanDhuhr == 1)):
		os.system("play " + scriptPath + azaanFile + " tempo " + aTempo + " gain " + aGain)

	if ((currTime ==  prayerTimes['Asr']) and (azaanAsr == 1)):
		os.system("play " + scriptPath + azaanFile + " tempo " + aTempo + " gain " + aGain)

	if ((currTime ==  prayerTimes['Maghrib']) and (azaanMaghrib == 1)):
		os.system("play " + scriptPath + azaanFile + " tempo " + aTempo + " gain " + aGain)

	if ((currTime ==  prayerTimes['Isha']) and (azaanIsha == 1)):
		os.system("play " + scriptPath + azaanFile + " tempo " + aTempo + " gain " + aGain)

	# DAILY ANNOUNCEMENT 
	# Announce todays date and last date of times fetched at a fixed time exery day

	if (((currTime == announcementTime) and (announcement == 1) and (announced == 0)) or os.path.isfile(scriptPath + "trigger.txt")):
		tts = gtts.gTTS("Assalam-o-alaikum!", lang = "ar", slow = False)
		tts2 = gtts.gTTS("Today is "+ str(todayHijriDay) + " " + str (todayHijriMonth), lang = "en", slow = False)
		tts3 = gtts.gTTS("Prayer times have been updated for " + str(prayerTimesForDate), lang = "en", slow = False)
		tts.save(scriptPath + "hello.mp3")
		tts2.save(scriptPath + "hello2.mp3")
		tts3.save(scriptPath + "hello3.mp3")
		os.system("play " + scriptPath + "hello.mp3 tempo " + dTempo + " gain " + dGain)
		os.system("play " + scriptPath + "hello2.mp3 tempo " + dTempo + " gain " + dGain)
		os.system("play " + scriptPath + "hello3.mp3 tempo " + dTempo + " gain " + dGain)
		if os.path.isfile(scriptPath + "trigger.txt"):
  			os.remove(scriptPath + "trigger.txt")

		announced = 1

	# Pause interval before next iteration
	time.sleep(checkInterval)



#####################
#      Methods      #
#####################

# 1 - University of Islamic Sciences, Karachi
# 2 - Islamic Society of North America
# 3 - Muslim World League
# 4 - Umm Al-Qura University, Makkah
# 5 - Egyptian General Authority of Survey
# 7 - Institute of Geophysics, University of Tehran
# 8 - Gulf Region
# 9 - Kuwait
# 10 - Qatar
# 11 - Majlis Ugama Islam Singapura, Singapore
# 12 - Union Organization islamic de France
# 13 - Diyanet İşleri Başkanlığı, Turkey
# 14 - Spiritual Administration of Muslims of Russia
# 15 - Moonsighting Committee Worldwide (also requires shafaq paramteer)
# 99 - Custom. See https://aladhan.com/calculation-methods
