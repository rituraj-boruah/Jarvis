import pyttsx3
import speech_recognition as sr
import keyboard
import os
import threading
from datetime import datetime
from decouple import config
from conv import random_text
from online import find_my_id, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast
from display import update_display, launch_display, run_display
from file_control import open_folder, search_file, delete_file, move_file, create_folder
from ai_assistant import gpt_fallback
from system_control import advanced_system_control, open_software, close_software
import wolframalpha

# Voice Engine Init
engine = pyttsx3.init('sapi5')
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 180)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

# User Configs
USER = config('USER')
HOSTNAME = config('BOT')
WOLFRAM_APP_ID = config('WOLFRAMALPHA_APP_ID')

listening = True

def speak(text):
    max_len = 100
    if len(text) > max_len:
        text = text[:max_len].rstrip() + "..."
    print(f"{HOSTNAME}: {text}")
    engine.say(text)
    engine.runAndWait()
    update_display(f"{HOSTNAME}: {text}")

def greet_me():
    hour = datetime.now().hour
    greet = "Good Morning" if hour < 12 else ("Good Afternoon" if hour < 18 else "Good Evening")
    speak(f"{greet} {USER}. I am {HOSTNAME}. How may I help you today?")

def start_listening():
    global listening
    listening = True
    print("[INFO] Listening resumed")

def pause_listening():
    global listening
    listening = False
    print("[INFO] Listening paused")

def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        try:
            audio = r.listen(source, timeout=7, phrase_time_limit=5)
        except sr.WaitTimeoutError:
            print("[WARN] Timeout. No speech detected.")
            return "None"

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"User: {query}")
        update_display(f"User: {query}")
        return query.lower()
    except Exception as e:
        print("[ERROR] Recognition failed:", e)
        speak("Sorry, didn't catch that.")
        return "None"

def search_wolfram(query):
    client = wolframalpha.Client(WOLFRAM_APP_ID)
    try:
        res = client.query(query)
        answer = next(res.results).text
        return answer
    except:
        return None

def fallback(query):
    result = gpt_fallback(query)
    if result:
        speak(result)
    else:
        speak("Let me search it online...")
        search_on_google(query)

keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)

if __name__ == "__main__":
    launch_display()

    def main_jarvis():
        greet_me()
        try:
            while True:
                if listening:
                    query = take_command()
                    if query == "none":
                        continue

                    if "how are you" in query:
                        speak(random_text())
                    elif query.startswith("search on chrome for"):
                        term = query.replace("search on chrome for", "").strip()
                        speak(f"Searching for {term}")
                        search_on_google(term)
                    elif query.startswith("search"):
                        term = query.replace("search", "").strip()
                        speak(f"Searching for {term}")
                        search_on_google(term)
                    elif "ip address" in query:
                        ip = find_my_id()
                        speak(f"Your IP Address is {ip}")
                    elif any(x in query for x in ["wikipedia", "who is", "what is", "define"]):
                        if "wikipedia" in query:
                            query = query.replace("wikipedia", "")
                        results = search_on_wikipedia(query)
                        speak(results)
                    elif "play" in query or "youtube" in query:
                        speak("What should I play on YouTube?")
                        video = take_command()
                        youtube(video)
                    elif "send email" in query:
                        speak("Please type the recipient email address:")
                        receiver_add = input("Recipient Email: ")
                        speak("What is the subject?")
                        subject = take_command().capitalize()
                        speak("What's the message?")
                        message = take_command().capitalize()
                        if send_email(receiver_add, subject, message):
                            speak("Email sent successfully.")
                        else:
                            speak("Sorry, failed to send email.")
                    elif "news" in query:
                        speak("Please say the topic for the news.")
                        topic = take_command()
                        headlines = get_news(topic)
                        for headline in headlines:
                            speak(headline)
                    elif "weather" in query:
                        speak("Please tell your city name.")
                        city = take_command()
                        weather, temp, feels_like = weather_forecast(city)
                        if weather:
                            speak(f"Currently in {city}: {weather}, Temp: {temp}, Feels like {feels_like}")
                        else:
                            speak("Couldn't fetch the weather.")
                    elif any(x in query for x in ["calculate", "solve", "math"]):
                        result = search_wolfram(query)
                        if result:
                            speak(f"The answer is {result}")
                        else:
                            fallback(query)
                    elif "open" in query:
                        app_name = query.split("open", 1)[1].strip()
                        open_software(app_name)
                    elif "close" in query:
                        app_name = query.split("close", 1)[1].strip()
                        close_software(app_name)
                    elif any(x in query for x in ["volume", "shutdown", "restart", "sleep"]):
                        advanced_system_control(query)
                    elif "move mouse" in query or "click mouse" in query or "scroll" in query:
                        advanced_system_control(query)
                    elif "open folder" in query:
                        folder_name = query.replace("open folder", "").strip()
                        open_folder(folder_name)
                    elif "search file" in query:
                        file_name = query.replace("search file", "").strip()
                        search_file(file_name)
                    elif "delete file" in query:
                        file_name = query.replace("delete file", "").strip()
                        delete_file(file_name)
                    elif "move file" in query:
                        parts = query.split("to")
                        if len(parts) == 2:
                            file_name = parts[0].replace("move file", "").strip()
                            destination = parts[1].strip()
                            move_file(file_name, destination)
                        else:
                            speak("Sorry, I couldn't understand where to move the file.")
                    elif "create folder" in query:
                        folder_name = query.replace("create folder", "").strip()
                        create_folder(folder_name)
                    elif "exit" in query or "stop" in query:
                        speak("Goodbye Sir! Shutting down.")
                        os._exit(0)
                    else:
                        fallback(query)
        except KeyboardInterrupt:
            speak("Goodbye Sir! Exiting.")
            os._exit(0)

    threading.Thread(target=main_jarvis, daemon=True).start()
    run_display()
