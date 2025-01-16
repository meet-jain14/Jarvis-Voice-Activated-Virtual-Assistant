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
newsapi = "YOUR_API"

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
    client = OpenAI(api_key='YOUR_API',
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
        r = requests.get("https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_API")
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

# Jarvis: Voice-Activated Virtual Assistant
# Jarvis is a Python-based voice-activated virtual assistant designed to simplify daily tasks by responding to voice commands. It utilizes various libraries to perform tasks like web browsing, playing music, fetching news, and interacting with OpenAI's GPT model to answer queries or provide assistance.

# Features
# Voice Recognition:
# Uses speech_recognition for capturing and interpreting voice commands.

# Text-to-Speech Conversion:

# Primary TTS implemented with gTTS and pygame.
# Includes a fallback method using pyttsx3 for offline compatibility.
# Web Automation:
# Opens popular websites such as Google, Facebook, Netflix, Prime Video, YouTube, and custom URLs.

# Music Playback:
# Integrates with a musicLibrary dictionary to play predefined songs via web browser.

# News Updates:
# Fetches top headlines from the US using the NewsAPI (https://newsapi.org).

# AI Integration:
# Interacts with OpenAI's GPT model to process and respond to complex queries.

# Wake Word Activation:
# Responds to the wake word "Jarvis" to activate further commands.

# Error Handling:
# Gracefully handles unrecognized speech and API-related issues.

# Requirements
# Python Libraries:
# speech_recognition
# webbrowser
# pyttsx3
# requests
# gtts
# pygame
# openai (Ensure you have an OpenAI API key for GPT interaction)
# External Dependencies:
# NewsAPI: Requires an API key for fetching news articles. Replace the placeholder with your own key.
# newsapi = "YOUR_API_KEY"
# Setup and Usage
# Install Dependencies:
# Install the required Python libraries using pip:

# bash
# Copy code
# pip install speechrecognition webbrowser pyttsx3 requests gtts pygame openai
# Configure API Keys:

# Replace the newsapi variable with your NewsAPI key.
# Replace the api_key parameter in OpenAI initialization with your OpenAI key.
# Run the Script:
# Start the virtual assistant by running the script:

# bash
# Copy code
# python jarvis.py
# Usage:

# Activate Jarvis by saying "Jarvis."
# Issue commands such as:
# "Open Google"
# "Play [song name]"
# "What's the news?"
# General queries for AI processing.
# Customization
# Add Music:
# Update the musicLibrary dictionary with your song names and URLs.

# Add More Commands:
# Extend the processCommand function to include additional functionalities.

# Change Wake Word:
# Modify the word.lower() == "jarvis" condition to set a different wake word.

# Known Issues and Improvements
# Speech Recognition Accuracy:
# Limited by background noise and Google Speech API accuracy.
# TTS Playback Delay:
# May introduce a slight delay due to file saving and loading.
# Error Handling:
# Basic error handling is implemented but can be improved for specific edge cases.
