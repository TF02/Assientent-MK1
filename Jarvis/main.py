import datetime
import json
import requests
import time
import pyttsx3
import speech_recognition as sr
import face
from Features.custom_voice import speak


engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[1].id)
voicespeed = 140
engine.setProperty('rate',voicespeed)


def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('listening...')
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print('Recognising...')
        querry = r.recognize_google(audio, language='de')
    except Exception as e:
        print('--')
        return '--'
    return querry


def get_time():
    time = datetime.datetime.now().strftime('%H:%M:%S')
    speak(time)
    print(time)


def whisme():
    speak('Willkommen zurück Sir')
    hour = datetime.datetime.now().hour
    print(hour)
    if hour >= 6 and hour < 12:
        speak('Ich hoffe sie haben gut geschlafen')
    elif hour >= 12 and hour <= 18:
        print('')
    elif hour >= 18 and hour <= 24:
        speak('Ich hoffe sie haben einen schönen Abend')
    else:
        speak('Ich wünsche ihnen noch eine gute Nacht ')
    speak('Was kann ich für sie tun')


def start(recognized_person_name):
    if recognized_person_name == "titian":
        whisme()


def function1():
    speak("das ist ein Test")


def weather(query):
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    api_key = "2b4ce373e2e9bf8dedc5ea01c669e463"
    city = "Martinfeld"
    url = base_url + "appid=" + api_key + "&q=" + city
    response = requests.get(url).json()
    temp = response['main']['temp']
    temp = temp - 273,15
    temp_str = '{:.0f}'.format(temp[0])
    humi = response['main']['humidity']
    sky = response['weather'][0]['description']
    print(sky)
    if sky == 'clear sky':
        sky = 'Klarem Himmel'
    elif sky == 'overcast clouds':
        sky = 'bewölktem himmel'
    if 'grad' in query:
        speak(f"Wir haben es in Martinfeld {temp_str} grad celsius")
    elif 'wetter' in query:
        speak(f"Heute haben wir in Martinfeld {temp_str} gard celsius bei {humi} % Luftfeuchtigkeit und {sky} ")


def listen_for_hey(timeout=5):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        while True:
            print("Listening...")
            audio = r.listen(source)
            try:
                query = r.recognize_google(audio, language='de')
                if "jarvis" in query.lower():
                    print("Hey recognized!")
                    # Put your code here that should only start when "hey" is recognized
                    break  # Exit the loop once "hey" is recognized
            except sr.UnknownValueError:
                print("Could not understand audio")
            except sr.RequestError as e:
                print(f"Could not request results; {e}")
    return True


# Load the dictionary from the JSON file
with open("command_dict.json", "r") as f:
    command_dict = json.load(f)
    

if __name__ == "__main__":


    listen_for_hey() 
    recognized_person_name = face.recognize_face()
    print(recognized_person_name)
    start(recognized_person_name)
    
    while True:

        querry = takecommand().lower()
        
        for key, value in command_dict.items():
            if querry in value:
                globals()[key](querry)
            

        if "hallo" in querry:
            speak('Hallo Sir was kann ich für sie tun')

       