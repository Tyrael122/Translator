import os, requests, uuid
from socket import *
from tkinter import Tk
import tkinter

servidor = "127.0.0.1"
porta = 43210
obj_socket = socket(AF_INET, SOCK_STREAM)
obj_socket.connect((servidor, porta))

endpoint_var_name = 'TRANSLATOR_TEXT_ENDPOINT'
if not endpoint_var_name in os.environ:
    raise Exception('Please set/export the environment variable: {}'.format(endpoint_var_name))
endpoint = os.environ[endpoint_var_name]

path = '/languages?api-version=3.0'
constructed_url = endpoint + path

headers = {
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

request = requests.get(constructed_url, headers=headers)
response = request.json()
lang_list = {}
for language in response["translation"]:
    lang_list[language] = response["translation"][language]["name"]
lang_names = []
for code in lang_list:
    lang_names.append(lang_list[code])

def translate():
    for key, value in lang_list.items():
        if value == option_lang_from.get():
            lang_from = key
        if value == option_lang_to.get():
            lang_to = key
    msg_enviada = lang_from + ";" + lang_to + ";" + text.get()
    obj_socket.send(msg_enviada.encode())
    msg_recebida = obj_socket.recv(1024).decode('utf-8')
    output_text.config(text=msg_recebida)


window = Tk()
window.title("Start screen")
window.geometry('400x400')

option_lang_from = tkinter.StringVar(window)
option_lang_to = tkinter.StringVar(window)

label_from = tkinter.Label(window, text="Lingua origem")
lang_from = tkinter.OptionMenu(window, option_lang_from, *lang_names)
label_to= tkinter.Label(window, text="Lingua destino")
lang_to = tkinter.OptionMenu(window, option_lang_to, *lang_names)
label_text = tkinter.Label(window, text="Texto para traduzir")
text = tkinter.Entry(window)
btn_translate = tkinter.Button(window, text="Traduzir", command=translate)
output_text = tkinter.Label(window, text="", font="Arial 16", wraplength=1000)

label_from.pack()
lang_from.pack()
label_to.pack()
lang_to.pack()
label_text.pack()
text.pack()
btn_translate.pack()
output_text.pack()

window.attributes('-fullscreen', True)
window.mainloop()