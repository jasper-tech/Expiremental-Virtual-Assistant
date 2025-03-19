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
import tkinter as tk
from tkinter import scrolledtext
import threading

# Initialize Speech Recognizer & Text-to-Speech Engine
listener = aa.Recognizer()
machine = pyttsx3.init()

# AI Voice Properties
voices = machine.getProperty("voices")
machine.setProperty("voice", voices[0].id)  
machine.setProperty("rate", 175)  
machine.setProperty("volume", 1.0)  

def talk(text):
    """Function to make Joey speak"""
    machine.say(text)
    machine.runAndWait()

def input_instruction(text_box): 
    """Function to listen for user instructions"""
    while True:
        try:
            with aa.Microphone() as origin:
                print("Listening...")
                speech = listener.listen(origin, timeout=10, phrase_time_limit=10)  
                instruction = listener.recognize_google(speech)
                instruction = instruction.lower()
                if "joey" in instruction:
                    instruction = instruction.replace('joey', "").strip()
                print(f"User said: {instruction}")
                process_instruction(instruction, text_box)  # Process instruction for GUI
        except aa.WaitTimeoutError:
            continue  # No speech detected, just keep listening
        except Exception as e:
            print(f"Error: {e}")
            continue

def get_weather(city="Accra"):
    """Fetch weather data for a given city"""
    try:
        api_key = "_OPENWEATHER_API_KEY"  # Replace with your actual API key
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        response = requests.get(url).json()

        if response["cod"] == 200:
            temp = response["main"]["temp"]
            weather_desc = response["weather"][0]["description"]
            talk(f"The temperature in {city} is {temp}°C with {weather_desc}.")
            return f"The temperature in {city} is {temp}°C with {weather_desc}."
        else:
            talk("Sorry, I couldn't fetch the weather details.")
            return "Sorry, I couldn't fetch the weather details."
    except:
        talk("I'm unable to fetch the weather right now. Try again later.")
        return "I'm unable to fetch the weather right now. Try again later."

def tell_joke():
    """Tell a random joke"""
    jokes = [
        "Why don't programmers like nature? Because it has too many bugs.",
        "What did the JavaScript developer say? I'll 'callback' later!",
        "Why did the computer go to therapy? It had too many tabs open!"
    ]
    joke = random.choice(jokes)
    talk(joke)
    return joke

def calculate(expression):
    """Perform basic calculations"""
    try:
        result = eval(expression)
        talk(f"The answer is {result}")
        return f"The answer is {result}"
    except:
        talk("Sorry, I couldn't calculate that.")
        return "Sorry, I couldn't calculate that."

def set_reminder(reminder):
    """Store a reminder in a text file"""
    with open("reminders.txt", "a") as file:
        file.write(f"{reminder}\n")
    talk(f"Reminder saved: {reminder}")
    return f"Reminder saved: {reminder}"

def get_news():
    """Fetch top news headlines"""
    try:
        url = "https://newsapi.org/v2/top-headlines?country=us&apiKey=YOUR_NEWSAPI_KEY"  
        response = requests.get(url).json()

        if response["status"] == "ok":
            articles = response["articles"][:3]
            headlines = []
            for article in articles:
                headlines.append(article["title"])
                talk(article["title"])
            return headlines
        else:
            talk("Couldn't fetch the news.")
            return "Couldn't fetch the news."
    except:
        talk("I can't fetch the news right now. Try again later.")
        return "I can't fetch the news right now. Try again later."

def open_application(app_name):
    """Open common applications"""
    apps = {
        "notepad": "notepad.exe",
        "calculator": "calc.exe",
        "chrome": "chrome.exe"
    }
    if app_name in apps:
        os.system(apps[app_name])
        talk(f"Opening {app_name}")
        return f"Opening {app_name}"
    else:
        talk("I can't open that application.")
        return "I can't open that application."

def process_instruction(instruction, text_box):
    """Process instruction either from voice or text input"""
    # Show user instruction in the chat
    text_box.insert(tk.END, f"You: {instruction}\n")
    text_box.yview(tk.END)  

    response = ""

    # Process the instruction
    if "what can you do" in instruction or "what are your features" in instruction:
        response = (
            "Here are some things I can do:\n"
            "1. Play songs on YouTube\n"
            "2. Tell the current time\n"
            "3. Tell the current date\n"
            "4. Tell jokes\n"
            "5. Perform basic calculations\n"
            "6. Set reminders\n"
            "7. Get the latest news\n"
            "8. Open applications like Notepad, Calculator, and Chrome\n"
            "9. Look up information about a person on Wikipedia\n"
            "10. Search the web for you\n"
            "11. Tell the weather forecast for a city\n"
            "12. Respond to greetings like 'How are you?' or 'What's your name?'\n"
            "13. Exit the program"
        )
        talk(response)

    elif "play" in instruction:
        song = instruction.replace("play", "").strip()
        talk(f"Playing {song}")
        response = f"Playing {song}"
        pywhatkit.playonyt(song)

    elif "time" in instruction:
        time_now = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The time is {time_now}")
        response = f"The time is {time_now}"

    elif "date" in instruction:
        date_now = datetime.datetime.now().strftime('%d/%m/%Y')
        talk(f"Today's date is {date_now}")
        response = f"Today's date is {date_now}"

    elif "how are you" in instruction:
        talk("Greetings! I am at your service.")
        response = "Greetings! I am at your service."
    
    elif "what is your name" in instruction:
        talk("I am Joey, your AI assistant created by Jasper. I am not yet fully functional, so enjoy the few features I have to offer. Thank you.")
        response = "I am Joey, your AI assistant created by Jasper. I am not yet fully functional, so enjoy the few features I have to offer. Thank you."

    elif "hey" in instruction or "hello" in instruction or " hey buddy" in instruction:
        talk("Hi, how can I help you?")
        response = "Hi, how can I help you?"
    elif "who is" in instruction:
        person = instruction.replace("who is", "").strip()
        try:
            info = wikipedia.summary(person, 1)
            text_box.insert(tk.END, f"Joey: {info}\n")
            text_box.yview(tk.END)
            talk(info)
            response = info
        except:
            talk("I couldn't find information on that.")
            response = "I couldn't find information on that."

    elif "weather" in instruction:
        city = instruction.replace("weather in", "").strip() or "Accra"
        response = get_weather(city)

    elif "joke" in instruction:
        response = tell_joke()

    elif "calculate" in instruction:
        expression = instruction.replace("calculate", "").strip()
        if "square root" in expression: 
            number = float(expression.replace("square root of", "").strip())
            result = math.sqrt(number)
            talk(f"The square root of {number} is {result}.")
            response = f"The square root of {number} is {result}."
        else:
            response = calculate(expression)

    elif "set reminder" in instruction:
        reminder = instruction.replace("set reminder", "").strip()
        response = set_reminder(reminder)

    elif "news" in instruction:
        response = get_news()

    elif "open" in instruction:
        app = instruction.replace("open", "").strip()
        response = open_application(app)

    elif "search" in instruction:
        query = instruction.replace("search", "").strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        talk(f"Searching for {query}")
        response = f"Searching for {query}"

    elif instruction in ["exit", "stop", "that's all"]:
        talk("Goodbye! Have a great day.")
        text_box.insert(tk.END, f"Joey: Goodbye! Have a great day.\n")
        text_box.yview(tk.END)
        root.quit()
        return

    else:
        talk("I didn't understand that. Please repeat.")
        response = "I didn't understand that. Please repeat."    
    text_box.insert(tk.END, f"Joey: {response}\n")
    text_box.yview(tk.END)

def on_submit(text_box, input_entry):
    """Submit the text input when the button is pressed"""
    instruction = input_entry.get()
    if instruction.strip() != "":
        process_instruction(instruction, text_box)
    input_entry.delete(0, tk.END)  

def Joey_GUI():
    """Create the GUI for Joey assistant"""
    global root
    root = tk.Tk()
    root.title("Joey - JC's Assistant")

    # Set background color for the window
    root.config(bg="#2C3E50")

    # Create a frame to hold the text box and entry field (for better layout control)
    frame = tk.Frame(root, bg="#2C3E50")
    frame.pack(padx=20, pady=20)

    # Create a scrollable text box for the conversation
    text_box = scrolledtext.ScrolledText(frame, wrap=tk.WORD, width=60, height=20, font=("Arial", 12), bd=5, relief="solid", bg="#34495E", fg="white")
    text_box.grid(row=0, column=0, padx=10, pady=10)
    text_box.insert(tk.END, "Joey: Hello! How can I assist you today?\n")
    text_box.yview(tk.END)

    # Create an entry field for text input
    input_entry = tk.Entry(frame, width=40, font=("Arial", 12), bd=5, relief="solid", bg="#BDC3C7", fg="black")
    input_entry.grid(row=1, column=0, pady=10, padx=10)

    # Create a submit button to process the input
    def on_button_hover(event):
        submit_button.config(bg="#1ABC9C")

    def on_button_leave(event):
        submit_button.config(bg="#16A085")

    submit_button = tk.Button(frame, text="Submit", width=20, font=("Arial", 12, "bold"), bg="#16A085", fg="white", activebackground="#1ABC9C", command=lambda: on_submit(text_box, input_entry))
    submit_button.grid(row=2, column=0, pady=5)
    submit_button.bind("<Enter>", on_button_hover)
    submit_button.bind("<Leave>", on_button_leave)
    
    threading.Thread(target=input_instruction, args=(text_box,), daemon=True).start()


    # Start the GUI loop
    root.mainloop()

# Start Joey with GUI
Joey_GUI()
