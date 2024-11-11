from flask import Flask, render_template, request
import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage
import speech_recognition as sr
import time

# Initialize Firebase
cred = credentials.Certificate('Jarvis.json')
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://jarvis-6370e-default-rtdb.firebaseio.com/'
})

# Initialize Cloud Storage
bucket = storage.bucket()

app = Flask(__name__)

def start_listening():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("Listening... Say something:")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        recognized_text = recognizer.recognize_google(audio)
        print("You said:", recognized_text)

        # Save the recognized text to a file
        with open('searches.txt', 'a') as f:
            f.write(recognized_text + '\n')

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
    except sr.RequestError as e:
        print("Error with the voice recognition service; {0}".format(e))

def upload_file_to_cloud_storage():
    # Upload the 'searches.txt' file to Cloud Storage
    blob = bucket.blob('searches.txt')
    blob.upload_from_filename('searches.txt')
    print('File uploaded to Cloud Storage.')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        command = request.form.get('command')
        if command.lower() == "jarvis":
            start_listening()
            time.sleep(1)  # Wait for the file to be saved
            upload_file_to_cloud_storage()
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)