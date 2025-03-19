import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia

# Initialize speech recognizer and text-to-speech engine
listener = aa.Recognizer()

machine = pyttsx3.init()

def talk(text):
    """Function to make Joana speak"""
    machine.say(text)
    machine.runAndWait()

def input_instruction(): 
    """Function to listen for user instructions"""
    global instruction
    try:
        with aa.Microphone() as origin:
            print("Listening...")
            speech = listener.listen(origin)
            instruction = listener.recognize_google(speech)
            instruction = instruction.lower()
            if "joey" in instruction:  # Detect 'joey' in the instruction
                instruction = instruction.replace('joey', "")  # Remove the name for further processing
            print(instruction)
    
    except Exception as e:
        print(f"Error: {e}")
        return None
    return instruction

def Joey():
    """Main function to control Joana's actions based on user input"""
    instruction = input_instruction()  # Call the input_instruction function properly
    if instruction is None:
        talk("Sorry, I didn't catch that. Please try again.")
        return

    print(instruction)

    if "play" in instruction:
        song = instruction.replace("play", "").strip()
        talk(f"Playing {song}")
        pywhatkit.playonyt(song)

    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M%p')
        talk(f"Current time is {time}")

    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d/%m/%Y')
        talk(f"Today's date is {date}")

    elif "how are you" in instruction:
        talk("Greetings, Master Jasper! I am doing well.")

    elif 'what is your name' in instruction:
        talk("I am Joana Joey, a powerful AI created by Master Jasper.")

    elif 'who is' in instruction:
        human = instruction.replace('who is', "").strip()
        try:
            info = wikipedia.summary(human, 1)
            print(info)
            talk(info)
        except wikipedia.exceptions.DisambiguationError as e:
            talk(f"There are multiple people with that name. Could you be more specific?")
        except wikipedia.exceptions.HTTPTimeoutError:
            talk("I'm having trouble connecting to Wikipedia right now. Please try again later.")

    else:
        talk("I didn't understand that. Please repeat.")

# Call Joey function to start the assistant
Joey()
