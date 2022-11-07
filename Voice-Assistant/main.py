from email import message
import pyjokes
from pywhatkit.main import search
import speech_recognition as sr
import pyttsx3
from neuralintents import GenericAssistant
import sys
import datetime
from email.message import EmailMessage
import smtplib
import webbrowser as we
from time import sleep, time
import requests
from bs4 import BeautifulSoup
import pywhatkit
import pyjokes
import wolframalpha
import wikipedia
from bs4 import BeautifulSoup

#Initialising the text-to-speech engine
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty("rate", 150) #configuring the engine
user = "Charles"

#function to run the engine
def say(audiostring):
    print(audiostring)
    engine.say(audiostring)
    engine.runAndWait()

#function to record the users's speech and converting it to text
def record():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
            print('I am listening!....')
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            try:
                data = r.recognize_google(audio, language="en-IN")
                print(data)
            except sr.UnknownValueError:
                print('sorry, i didnt understand')
            if 'what' in data or 'which' in data or 'who' in data or 'when' in data or 'explain' in data or 'describe' in data or 'define' in data:
                  try:#reply the 'wh' questions
                    app_id = '7JKRXQ-AQW9YQJQJT'
                    client = wolframalpha.Client(app_id)
                    res1 = client.query(data)
                    answer = next(res1.results).text
                    say(answer)
                    if answer == "None":
                        say(wikipedia.summary(data, sentences=2))
                  except StopIteration:
                        say(wikipedia.summary(data, sentences=2))
                  except AssertionError:
                        say(data)
            else:
                message = data.lower()
                assistant.request(message)
    return data

    
#function to stop the program and provide specific results
def stop():
  time = datetime.datetime.now().hour
  if(time >= 21) and (time < 6):
    say(f"Good Night {user}! Have a nice sleep")
  else:
    say(f"Bye {user}")
  sys.exit(0)

#greeting
hour = datetime.datetime.now().hour
if(hour >= 6) and (hour < 12):
    say(f"Good Morning {user}")
elif(hour >= 12) and (hour < 18):
    say(f"Good afternoon {user}")
elif(hour >= 18) and (hour < 21):
    say(f"Good Evening {user}")
say("how may i assist you")


#to send email
def sendemail():
    email_list = {
        "tom": "vyinghope90@gmail.com"
    }
    try:
        email = EmailMessage()
        say("To whom you want to send the e-mail")
        name = record().lower()
        email["To"] = email_list[name]
        say("What is the subject of your e-mail")
        email["Subject"] = record()
        email["From"] = "Email address"
        say("What should i Say?")
        email.set_content(record())
        s = smtplib.SMTP("smtp.gmail.com", 587)
        s.starttls()
        s.login('email address', 'password')
        s.send_message(email)
        s.close()
        say("Email has Sent")
    except Exception as e:
        print(e)
        say("Unable to send the Email")

#to find the weather condition
def weather():
    city = "thrissur"
    city = city + " weather"
    city = city.replace(" ", "+")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

    res = requests.get(f'https://www.google.com/search?q={city}&oq={city}'
                       f'&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    print("Searching...\n")
    soup = BeautifulSoup(res.text, 'html.parser')
    location = soup.select('#wob_loc')[0].getText().strip()
    info = soup.select('#wob_dc')[0].getText().strip()
    weather1 = soup.select('#wob_tm')[0].getText().strip()
    say(f"location is {location}")
    say(f"climate is {info}")
    say(f"temperature is {weather1}"+"°C")


#to find todays news
def today_news():
    url = 'https://newsapi.org/v2/everything?'
    parameters = {
        'q': 'big data', # query phrase
        'pageSize': 5,  # maximum is 100
        'apiKey': "703dbdd8d4bb422690dc7e350af54da6" # your own API key
    }
    response = requests.get(url, params=parameters)
    response_json = response.json()
    for i in response_json['articles']:
       say(i['title'])


def time1():
    say("Current time is " + datetime.datetime.now().strftime("%I:%M"))


def date():
      say("Current date is " + str(datetime.datetime.now().day) + " " +
               str(datetime.datetime.now().month) + " " + str(datetime.datetime.now().year))


def search():
       say("What you want to search")
       we.open("https://www.google.com/search?q="+ record())



def covid():
    r = requests.get("https://coronavirus-19-api.herokuapp.com/all").json()
    say(f'Confirmed cases: {r["cases"]} \nDeaths: {r["deaths"]} \nRecovered: {r["recovered"]}')

def joke():
    say(pyjokes.get_joke())


    
def friday(data):
    if 'define' in data or 'explain' in data or 'describe' in data:
        say(wikipedia.summary(data,sentences=2))


#mappings made for specific querys to the corresponding functions.If a query, in patterns of the  intents.json file is identified,we perform thesexcorresponding fuctions
mappings = {
    "exit": stop,
    "email": sendemail,
    "climate": weather,
    "news": today_news,
    "now": time1,
    "today": date,
    "google": search,
    "corona": covid,
    "comedy": joke,
    }

#training the model with data
assistant = GenericAssistant('intents.json', intent_methods=mappings)
assistant.train_model()
assistant.save_model()
assistant.load_model()


#function that provide the input for querys the model asks
def record1():
    r = sr.Recognizer()
    with sr.Microphone(device_index=0) as source:
            print('I am listening!....')
            r.adjust_for_ambient_noise(source, duration=1)
            audio = r.listen(source)
            try:
                audio_string = r.recognize_google(audio, language="en-IN")
                print(audio_string)
            except sr.UnknownValueError:
                print('sorry, i didnt understand')
            print("what you want to search on YouTube?")
            pywhatkit.playonyt(audio_string)
            sys.exit(0)
while True:
    data1=record()
    if 'search on YouTube' in data1 or 'YouTube' in data1:
        record1()
   
