import pyttsx3 #text to speech library
import datetime #date and time library
import speech_recognition as sr #speech recognition library
import wikipedia #for accessing information from wikipedia
import webbrowser #for opening websites usingt the browser
import os #for using system commands to open applications

from config import apikey
chatStr = ""

def chat(query):
    global chatStr
    print(chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\n Luna: "
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt= chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    speak(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    print(response["choices"][0]["text"])
    text+=response["choices"][0]["text"]
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:

        f.write(text)
import openai
engine=pyttsx3.init('sapi5') #sapi5 is a Windows voice API
voices=engine.getProperty('voices')

engine.setProperty('voice',voices[1].id) #use voices[0] for male and voices[1] for female
def speak(audio):
    #takes string parameter and gives voice output
    engine.say(audio)
    engine.runAndWait()
def wishMe():
    #wish the user and introduction
    hour=int(datetime.datetime.now().hour)


    if (hour>=0 and hour<12):
        speak("Good morning")
    elif(hour>=12 and hour<=18):
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Luna. How may I help you?")
def takeCommand():
    #takes microphone input from user and gives string output
    r=sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold=1
        audio=r.listen(source)
    try:
        print("Recognizing...")
        query=r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        print("Say that again please...")
        return "None"
    return query


if __name__=="__main__":
    flag=0
    wishMe()
    while(True):
        query=takeCommand().lower()
        if "stop" in query:
            exit()
        #logic for executing tasks based on query

        sites=[["youtube","youtube.com"],["google","google.com"],["prime","primevideo.com"],["whatsapp","web.whatsapp.com"],["reddit","reddit.com"],["wikipedia","wikipedia.com"],["instagram","instagram.com"],["insta","instagram.com"]]
        for site in sites:
            if f"open {site[0]}" in query:
                speak(f"Opening {site[0]}")
                webbrowser.open(site[1])
                flag=1


        apps=[["spotify","C:\\Program Files\\WindowsApps\\SpotifyAB.SpotifyMusic_1.208.923.0_x86__zpdnekdrzrea0\\Spotify.exe"],["word","C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"],["excel","C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"],["powerpoint","C:\\Program Files\\Microsoft Office\\root\\Office16\\POWERPNT.EXE"],["onenote","C:\\Program Files\\Microsoft Office\\root\\Office16\\ONENOTE.EXE"],["chrome","C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"],["google chrome","C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"]]
        for app in apps:
            if f"open {app[0]}" in query:
                os.startfile(app[1])
                speak(f"Opening {app[0]}")
                flag=1
        if (flag==0):
            if "using artificial intelligence" in query:
                ai(prompt=query)
            elif 'wikipedia' in query:
                speak("Searching Wikipedia...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2)
                speak(f"According to Wikipedia, {results}.")
            elif "date" in query:
                today = datetime.date.today()
                speak(f"Today's date is {today}")
            elif "the time" in query:
                # strTime=datetime.datetime.now().strftime("%H:%M:%S")
                # speak(strTime)
                speak(f"The time is {datetime.datetime.now().hour} {datetime.datetime.now().minute}")


            elif "reset chat" in query:
                chatStr = ""
            else:
                print("Chatting...")
                chat(query)