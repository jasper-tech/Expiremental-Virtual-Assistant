import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import requests
import random
import os
import webbrowser
import time
import math

# Initialize Speech Recognizer & Text-to-Speech Engine
listener = aa.Recognizer()
machine = pyttsx3.init()

# AI Voice Properties
voices = machine.getProperty("voices")
machine.setProperty("voice", voices[1].id)  
machine.setProperty("rate", 175)  
machine.setProperty("volume", 1.0)  

def talk(text):
    """Function to make Joey speak"""
    machine.say(text)
    machine.runAndWait()

def input_instruction(): 
    """Function to listen for user instructions"""
    try:
        with aa.Microphone() as origin:
            print("Listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "joey" in instruction:
                instruction = instruction.replace('joey', "").strip()
            print(f"User said: {instruction}")
            return instruction
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_weather(city="Accra"):
    """Fetch weather data for a given city"""
    try:
        api_key = "YOUR_OPENWEATHER_API_KEY"  # Replace with your API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response["cod"] == 200:
            temp = response["main"]["temp"]
            weather_desc = response["weather"][0]["description"]
            talk(f"The temperature in {city} is {temp}°C with {weather_desc}.")
        else:
            talk("Sorry, I couldn't fetch the weather details.")
    except:
        talk("I'm unable to fetch the weather right now. Try again later.")

def tell_joke():
    """Tell a random joke"""
    jokes = [
        "Why don't programmers like nature? Because it has too many bugs.",
        "What did the JavaScript developer say? I'll 'callback' later!",
        "Why did the computer go to therapy? It had too many tabs open!"
    ]
    talk(random.choice(jokes))

def calculate(expression):
    """Perform basic calculations"""
    try:
        result = eval(expression)
        talk(f"The answer is {result}")
    except:
        talk("Sorry, I couldn't calculate that.")

def set_reminder(reminder):
    """Store a reminder in a text file"""
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder}\n")
    talk(f"Reminder saved: {reminder}")

def get_news():
    """Fetch top news headlines"""
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_NEWSAPI_KEY"  
        response = requests.get(url).json()

        if response["status"] == "ok":
            articles = response["articles"][:3]
            for article in articles:
                talk(article["title"])
        else:
            talk("Couldn't fetch the news.")
    except:
        talk("I can't fetch the news right now. Try again later.")

def open_application(app_name):
    """Open common applications"""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "C:/Program Files/Google/Chrome/Application/chrome.exe"
    }
    if app_name in apps:
        os.system(apps[app_name])
        talk(f"Opening {app_name}")
    else:
        talk("I can't open that application.")

def Joey():
    """Main function to control Joey's actions based on user input"""
    talk("Hello Jasper! How can I assist you today?")
    
    while True:
        instruction = input_instruction()
        
        if instruction is None:
            talk("Sorry, I didn't catch that. Please try again.")
            continue

        if "what can you do" in instruction:
            abilities = """
            I can do the following:
            1. Play music on YouTube - say 'Play' followed by a song name.
            2. Tell the time - say 'What time is it?'.
            3. Tell today's date - say 'What is today's date?'.
            4. Check the weather - say 'Weather in [city]'.
            5. Tell a joke - say 'Tell me a joke'.
            6. Perform calculations - say 'Calculate' followed by a math expression.
            7. Set reminders - say 'Set reminder' followed by your reminder.
            8. Fetch the latest news - say 'Tell me the news'.
            9. Open applications - say 'Open' followed by the app name.
            10. Search the web - say 'Search' followed by your query.
            11. Provide Wikipedia information - say 'Who is' followed by a person's name.
            12. Respond to greetings and questions about itself.
            13. Exit the assistant - say 'Exit', 'Stop', or 'That's all'.
            """
            print(abilities)
            talk(abilities)

        elif "play" in instruction:
            song = instruction.replace("play", "").strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif "time" in instruction:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The time is {time_now}")

        elif "date" in instruction:
            date_now = datetime.datetime.now().strftime('%d/%m/%Y')
            talk(f"Today's date is {date_now}")

        elif "how are you" in instruction:
            talk("Greetings, Jas! I am at your service.")

        elif "joey you there" in instruction:
            talk("At your service, sir!")

        elif "what is your name" in instruction:
            talk("I am Joana, your personal assistant.")

        elif "who is" in instruction:
            person = instruction.replace("who is", "").strip()
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            except:
                talk("I couldn't find information on that.")

        elif "weather" in instruction:
            city = instruction.replace("weather in", "").strip() or "Accra"
            get_weather(city)

        elif "joke" in instruction:
            tell_joke()

        elif "calculate" in instruction:
            expression = instruction.replace("calculate", "").strip()
            calculate(expression)

        elif "set reminder" in instruction:
            reminder = instruction.replace("set reminder", "").strip()
            set_reminder(reminder)

        elif "news" in instruction:
            get_news()

        elif "open" in instruction:
            app = instruction.replace("open", "").strip()
            open_application(app)

        elif "search" in instruction:
            query = instruction.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            talk(f"Searching for {query}")

        elif instruction in ["exit", "stop", "that's all"]:
            talk("Goodbye Jay! Have a great day.")
            break

        else:
            talk("I didn't understand that. Please repeat.")

    """Main function to control Joey's actions based on user input"""
    talk("Hello Jasper! How can I assist you today?")
    
    while True:
        instruction = input_instruction()
        
        if instruction is None:
            talk("Sorry, I didn't catch that. Please try again.")
            continue

        if "play" in instruction:
            song = instruction.replace("play", "").strip()
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif "time" in instruction:
            time_now = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The time is {time_now}")

        elif "date" in instruction:
            date_now = datetime.datetime.now().strftime('%d/%m/%Y')
            talk(f"Today's date is {date_now}")

        elif "how are you" in instruction:
            talk("Greetings, Master Jasper! I am at your service.")

        elif "joey you there" in instruction:
            talk("At your service, sir!")

        elif "what is your name" in instruction:
            talk("I am Joana, your AI assistant.")

        elif "who is" in instruction:
            person = instruction.replace("who is", "").strip()
            try:
                info = wikipedia.summary(person, 1)
                print(info)
                talk(info)
            except:
                talk("I couldn't find information on that.")

        elif "weather" in instruction:
            city = instruction.replace("weather in", "").strip() or "Accra"
            get_weather(city)

        elif "joke" in instruction:
            tell_joke()

        elif "calculate" in instruction:
            expression = instruction.replace("calculate", "").strip()
            calculate(expression)

        elif "set reminder" in instruction:
            reminder = instruction.replace("set reminder", "").strip()
            set_reminder(reminder)

        elif "news" in instruction:
            get_news()

        elif "open" in instruction:
            app = instruction.replace("open", "").strip()
            open_application(app)

        elif "search" in instruction:
            query = instruction.replace("search", "").strip()
            webbrowser.open(f"https://www.google.com/search?q={query}")
            talk(f"Searching for {query}")

        elif instruction in ["exit", "stop", "that's all"]:
            talk("Goodbye Jasper! Have a great day.")
            break

        else:
            talk("I didn't understand that. Please repeat.")

# Start Joey
Joey()
