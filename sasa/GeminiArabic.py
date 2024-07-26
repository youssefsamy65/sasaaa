import google.generativeai as genai
import speech_recognition as sr
from datetime import date
from gtts import gTTS
from io import BytesIO
from pygame import mixer
import threading
import queue
import time
import tkinter as tk
from tkinter import messagebox

mixer.init()
# os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"

# Set the Google Gemini API key as an environment variable or here
genai.configure(api_key="AIzaSyCX0MFnBRE7bRAf4dxd0ocaW45yVyyQjvw")

today = str(date.today())

# Model of Google Gemini API
model = genai.GenerativeModel(
    'gemini-pro',
    generation_config=genai.GenerationConfig(
        candidate_count=1,
        top_p=0.7,
        top_k=4,
        max_output_tokens=128,
        temperature=0.7,
    )
)

chat = model.start_chat(history=[])

def chatfun(request, text_queue, llm_finished):
    response = chat.send_message(request, stream=True)
    for chunk in response:
        if chunk.candidates[0].content.parts:
            print(chunk.candidates[0].content.parts[0].text, end='')
            text_queue.put(chunk.text.replace("*", ""))
            time.sleep(0.5)

    append2log(f"AI: {response.candidates[0].content.parts[0].text}\n")
    llm_finished.set()

def speak_text(text):
    mp3file = BytesIO()
    tts = gTTS(text, lang="ar", tld='com.eg')
    tts.write_to_fp(mp3file)
    mp3file.seek(0)
    try:
        mixer.music.load(mp3file, "mp3")
        mixer.music.play()
        while mixer.music.get_busy():
            pass
    except KeyboardInterrupt:
        mixer.music.stop()
    mp3file.close()

def text2speech(text_queue, audio_queue, stop_event, data_available, busynow):
    time.sleep(1.0)
    while not stop_event.is_set():
        try:
            text = text_queue.get(timeout=1)
            if len(text) < 2:
                text_queue.task_done()
                print("skip short string text..")
                continue
            
            mp3file = BytesIO()
            tts = gTTS(text, lang="ar", tld='com.eg')
            tts.write_to_fp(mp3file)
            audio_queue.put(mp3file)

            waiting = True
            while waiting:
                if busynow.is_set():
                    time.sleep(0.5)
                else:
                    data_available.set()
                    waiting = False

            text_queue.task_done()
        except queue.Empty:
            pass

def play_audio(audio_queue, stop_event, data_available, busynow):
    while not stop_event.is_set():
        data_available.wait()
        data_available.clear()
        try:
            busynow.set()
            mp3file = audio_queue.get()
            mp3file.seek(0)
            mixer.music.load(mp3file, "mp3")
            mixer.music.play()
            while mixer.music.get_busy():
                pass
            busynow.clear()
            audio_queue.task_done()
            if audio_queue.empty():
                break
        except queue.Empty:
            continue

def append2log(text):
    global today
    fname = 'chatlog-' + today + '.txt'
    with open(fname, "a", encoding='utf-8') as f:
        f.write(text + "\n")

slang = "ar-EG"

def main(stop_event):
    global today, chat, model, slang
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.dynamic_energy_threshold = False
    rec.energy_threshold = 400

    while not stop_event.is_set():
        with mic as source:
            rec.adjust_for_ambient_noise(source, duration=0.5)
            print("Listening ...")
            try:
                audio = rec.listen(source, timeout=20, phrase_time_limit=30)
                text = rec.recognize_google(audio, language=slang)
                request = text.lower()

                if "اسمك ايه" in text or "ما هو اسمك" in text:
                    response_text = "اسمي صوفيا، خولقت من عقول مبدعة في الأكاديمية العربية للعلوم والتكنولوجيا والنقل البحري. تم تصميمي للمساعدة والإفادة، وأنا أمثل بكل فخر روح الابتكار التي تعززت في جامعتنا الموقرة. كيف يمكنني مساعدتك بمزيد من التفاصيل؟"
                    speak_text(response_text)
                    append2log(f"You: {text}\n AI: {response_text}\n")
                    continue

                if "ازيك عامله ايه" in text:
                    response_text = "أنا الحمدو لله كويسه انت اخبارك ايه."
                    speak_text(response_text)
                    append2log(f"You: {text}\n AI: {response_text}\n")
                    continue

                if "كفايه كده" in request:
                    append2log(f"You: {request}\n")
                    speak_text("مع السلامة")
                    append2log(f"AI: مع السلامة.\n")
                    print('مع السلامة')
                    break

                append2log(f"You: {request}\n")
                print(f"You: {request}\n AI: ", end='')

                text_queue = queue.Queue()
                audio_queue = queue.Queue()
                data_available = threading.Event()
                llm_finished = threading.Event()
                busynow = threading.Event()

                llm_thread = threading.Thread(target=chatfun, args=(request, text_queue, llm_finished,))
                tts_thread = threading.Thread(target=text2speech, args=(text_queue, audio_queue, stop_event, data_available, busynow,))
                play_thread = threading.Thread(target=play_audio, args=(audio_queue, stop_event, data_available, busynow,))

                llm_thread.start()
                tts_thread.start()
                play_thread.start()

                time.sleep(1.0)
                text_queue.join()
                llm_finished.wait()
                llm_thread.join()
                time.sleep(0.5)
                audio_queue.join()

                print('\n')

            except Exception as e:
                print(f"Error: {e}")
                continue

def run_main(stop_event):
    threading.Thread(target=main, args=(stop_event,)).start()

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("AI Assistant")
        self.geometry("250x100")
        self.configure(background='#f0f0f0')

         # Calculate center position based on screen size
        screen_width = 1024  # cm
        screen_height = 600  # cm
        window_width = 250   # cm
        window_height = 100  # cm
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        
        self.stop_event = threading.Event()

        self.start_button = tk.Button(self, text="Start", command=self.start, bg='#4CAF50', fg='white', font=('Arial', 12))
        self.start_button.pack(padx=100, pady=10)

        self.stop_button = tk.Button(self, text="Stop", command=self.stop, bg='#F44336', fg='white', font=('Arial', 12))
        self.stop_button.pack(padx=100, pady=10)

    def start(self):
        self.stop_event.clear()
        run_main(self.stop_event)

    def stop(self):
        self.stop_event.set()
        messagebox.showinfo("AI Assistant", "Stopped")

if __name__ == "__main__":
    app = Application()
    app.mainloop()
