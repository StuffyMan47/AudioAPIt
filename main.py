import wave
import shutil
from vosk import Model, KaldiRecognizer
import os, json
from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
#Также нужно сделать следующие действия:
# pip install fastapi
# pip install "uvicorn[standard]"

#в терминал нужно написать: uvicorn main:app --reload

#Далее перейти по этому адресу: http://127.0.0.1:8000/

#Далее нужно зайти на сайт: http://127.0.0.1:8000/docs#/default/save_file_file_upload_file_post

#Чтобы загрузить аудиозапись в формате .wav

app = FastAPI()

@app.post("/file/upload-file")
def save_file(file: UploadFile = File(...)):
    with open('output.wav', "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"file_name": file.filename}

def listen():
    model = Model("Smodel")
    rec = KaldiRecognizer(model, 44100)
    wf = wave.open(r'output.wav', "rb")
    last_n = False
    result = ''
    while True:
        data = wf.readframes(44100)
        if len(data) == 0:
            break

        if rec.AcceptWaveform(data):
            x = json.loads(rec.Result())
            result = x["text"]
        else:
            pass
    return(result)


@app.get("/")
def read_root():
    res = listen()
    html_content = f"<h2>Speech to text: {listen()}</h2>"
    return HTMLResponse(content=html_content)

