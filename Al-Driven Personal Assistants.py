import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import openai

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# OpenAI API Key (replace with your own)
openai.api_key = "your-api-key-here"

def talk(text):
    engine.say(text)
    engine.runAndWait()

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print("You said:", command)
    except:
        talk("Sorry, I did not catch that.")
        return ""
    return command.lower()

def chat_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

def run_jarvis():
    talk("Hello, how can I help you today?")
    while True:
        command = take_command()

        if 'time' in command:
            time = datetime.datetime.now().strftime('%I:%M %p')
            talk(f"The current time is {time}")

        elif 'who is' in command:
            person = command.replace('who is', '')
            info = wikipedia.summary(person, sentences=2)
            talk(info)

        elif 'play' in command:
            song = command.replace('play', '')
            talk(f"Playing {song}")
            pywhatkit.playonyt(song)

        elif 'open google' in command:
            talk("Opening Google")
            pywhatkit.search("Google")

        elif 'chat' in command:
            talk("Sure, what do you want to talk about?")
            user_prompt = take_command()
            response = chat_with_openai(user_prompt)
            talk(response)

        elif 'stop' in command or 'exit' in command:
            talk("Goodbye!")
            break

        else:
            talk("I can search the web for you.")
            pywhatkit.search(command)

run_jarvis()
