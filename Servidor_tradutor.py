from socket import *
import requests
import uuid

key = "f4f11fcfcc2f4baaa32ca4c8f3d1287b"
endpoint = "https://api.cognitive.microsofttranslator.com"
location = "brazilsouth"
path = '/translate'
constructed_url = endpoint + path
headers = {
    'Ocp-Apim-Subscription-Key': key,
    # location required if you're using a multi-service or regional (not global) resource.
    'Ocp-Apim-Subscription-Region': location,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

servidor = "127.0.0.1"
porta = 43210

obj_socket = socket(AF_INET, SOCK_STREAM)
obj_socket.bind((servidor, porta))
obj_socket.listen(2)
print("Aguardando cliente....")
con, cliente = obj_socket.accept()
print("Conectado com: ", cliente)
while True:
    msg_recebida = str(con.recv(1024).decode('utf-8'))
    msg_recebida = msg_recebida.split(";", 2)
    lang_from = msg_recebida[0]
    lang_to = msg_recebida[1]
    params = {
        'api-version': '3.0',
        'from': lang_from,
        'to': [lang_to]
    }
    body = [{
        'text': msg_recebida[2]
    }]
    request = requests.post(
        constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    for info in response:
        for translation in info["translations"]:
            msg_enviada = translation["text"] + "\n"
            con.send(msg_enviada.encode())