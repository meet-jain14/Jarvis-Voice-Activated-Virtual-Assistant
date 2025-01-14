import os

import speech_recognition as sr
import webbrowser
import pyttsx3
from pyttsx3 import engine
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "019ea5f7c30d4b6f940b34016272e822"

# response = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}")
# print(response.status_code, response.json())

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3')

    pygame.mixer.init()

    pygame.mixer.music.load('temp.mp3')

    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    pygame.mixer.music.unload()
    os.remove("temp.mp3")

def aiProcess(command):
    client = OpenAI(api_key='Osk-proj-vIPtNz0_zCBoP8_sjHFiFJQCS71J-IKCRIHhDKXtNGI0YHmrhKeGcGoQRhHrEOA4863kpwua_vT3BlbkFJ6zsRkrzuh1-QzOUbfqFHv9di6NfKKmHygEBAzSWg_dcKFM9xR_DTuU0iibRgoGGjpC5acyiVYA',
    )
    completion = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": command}
    ]
    )

    return completion.choices[0].message.content


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://www.facebook.com/")
    elif "open netflix" in c.lower():
        webbrowser.open("https://www.netflix.com/browse")
    elif "open prime" in c.lower():
        webbrowser.open("https://www.primevideo.com/region/eu/storefront")
    elif "open gnums" in c.lower():
        webbrowser.open("https://ums.paruluniversity.ac.in/Login.aspx")
    elif "open youtube" in c.lower():
        webbrowser.open("https://www.youtube.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif "news" in c.lower():
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=019ea5f7c30d4b6f940b34016272e822")
        if r.status_code == 200:
            #Parse the Json response
            data = r.json()

            #Extract the articles
            articles = data.get('articles', [])
            if not articles:
                speak("I couldn't find any news articles at the moment.")

            #Print the headlines
            for article in articles:
                speak(article['title'])

    else:
        #Let OpenAi handle the request
        output = aiProcess(c)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis.....")
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from microphone
        r = sr.Recognizer()

        print("Recognizing...")
        # recognize speech using google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            if word.lower() == "jarvis":
                speak("Yes sir")
                # Listen for Command
                with sr.Microphone() as source:
                    print("Jarvis Activated..")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except sr.UnknownValueError:
            print("Jarvis could not understand audio")
        except sr.RequestError as e:
            print("Jarvis error; {0}".format(e))
