import speech_recognition as aa
import pyttsx3
import pywhatkit
import datetime
import wikipedia




listener = aa.Recognizer()


machine = pyttsx3.init()

def talk(text):
    machine.say(text)

machine.runAndWait()

def input_instruction(): 
    global instruction
    try:
        with aa.Microphone() as origin:
            print("listening")
        speech = listener.listen(origin)
        instruction = listener.recognize_google(speech)
        instruction = instruction.lower()
        if "joey" in instruction:
            instruction = instruction.replace('joey', " ")
            print(instruction)
        print(instruction)
    
    except:
        pass
    return instruction


def Joey():

    instruction = input_instruction
    print(instruction)

    if "play" in instruction:
        song = instruction.replace("play", " ")
        talk("playing" + song)
        pywhatkit.playonyt(song)

    elif 'time' in instruction:
        time = datetime.datetime.now().strftime('%I:%M%p') 
        talk('Current time' + time)

    elif 'date' in instruction:
        date = datetime.datetime.now().strftime('%d /%m /%Y')
        talk ("Today's date " + date)

    elif "How are You" in instruction:
        talk('Greetings Master Jasper, I am fine!')

    elif 'What is your Name' in instruction:
        talk('I am Joana Joey, A poweful AI created by Master Jasper')

    elif 'Who is' in instruction:
        human = instruction.replace('Who is'," ")
        info = wikipedia.summary(human, 1)
        print(info)
        talk(info)


    else:
        talk('Please repeat!')
        
Joey()


   





