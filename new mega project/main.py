import speech_recognition as sr
import webbrowser
import pyttsx3
import music_player
import requests
import threading
import time
import requests
import json



recognizer=sr.Recognizer()
engine=pyttsx3.init()
newsapi="b07547984e764bf4930bb81f70e69fa0"
genaikey= "AIzaSyDML29qTmylzApq1J9zkhIzg4fEebY5zEU"


speech_lock = threading.Lock()




# Function to speak text
def speak(text):
    with speech_lock:  # Acquire lock to ensure only one thread speaks at a time
        engine.say(text)
        engine.runAndWait()
def query_genai(prompt):
    # Define the endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={genaikey}"

    # Define the payload
    payload = {
        "prompt": {"text": prompt}
    }

    # Set headers
    headers = {
        "Content-Type": "application/json"
    }

    try:
        # Send the POST request
        response = requests.post(url, headers=headers, json=payload)

        # Process the response
        if response.status_code == 200:
            response_data = response.json()
            # Extract the generated content
            generated_text = response_data.get("candidates", [{}])[0].get("output", "")
            return generated_text if generated_text else "I'm sorry, I couldn't generate a response."
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"An error occurred: {str(e)}"


def speak_non_blocking(text):
    # Push speech to the queue for processing
    threading.Thread(target=speak, args=(text,)).start()

def fetch_news():
    try:
        # Request the news from the API
        response = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        
        if recognizer.status_code == 200:
            data = recognizer.json()
            articles = data.get('articles', [])
            if not articles:
                speak("No news articles found.")
                return
            
            speak("Here are the top headlines.")
            
            for i, article in enumerate(articles[:5]):  # Read top 5 headlines
                speak_non_blocking(f"Headline {i+1}: {article.get('title')}")
                time.sleep(1)
        else:
            speak("Failed to fetch news. Please check the API or your internet connection.")
    except Exception as e:
        speak("I couldn't fetch the news due to an error.")
        print(f"Error fetching news: {e}")


def process_command(command):
    if "open google" in command.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in command.lower():
        webbrowser.open("https://youtube.com")
    elif "open instagram" in command.lower():
        webbrowser.open("https://instagram.com")
    elif command.lower().startswith("play"):
        lyrics = command.lower().split(" ", 1)[1]
        link = music_player.music.get(lyrics)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, couldn't find the song.")
    elif "say news" in command.lower():
        fetch_news()
    elif "ask genai" in command.lower():
        query = command.lower().replace("ask genai", "").strip()
        if query:
            speak("Let me think...")
            response = query_genai(query)
            speak(response)
        else:
            speak("Please provide a question for me to ask GenAI.")
    else:
        speak("Sorry, I didn't understand that command.")


    

if __name__=="__main__":
    speak("Initializing friday")
    running=True
    # Start the thread to handle speech synthesis
   

    # obtain audio from the microphone
    while running:
        recognizer = sr.Recognizer()
# recognize speech using Sphinx
        speak("listening....")
        try:
            with sr.Microphone() as source:
                speak("say something")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                audio = recognizer.listen(source, timeout=10)
                word = recognizer.recognize_google(audio).lower()
            if(word.lower()=='friday'):
                speak("Yes friday here,how may i help you")
                
                
                with sr.Microphone() as source:
                        speak("friday is activated")
                        audio = recognizer.listen(source)
                        command=recognizer.recognize_google(audio)
                        print("recognized command",command)
                if "stop" in command.lower() or "stop friday" in command.lower():
                            speak("Stopping Friday. Goodbye!")
                            running = False
                            engine.stop()
                            break
                else:
                     threading.Thread(target=process_command, args=(command,)).start()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything. Please try again.")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
        except Exception as e:
            print(f"Error: {e}")
                          
                
        
        




