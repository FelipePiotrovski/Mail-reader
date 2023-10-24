import imaplib
import re
import os
from dotenv import load_dotenv
import quopri
import pyttsx3

load_dotenv()

host = 'imap.gmail.com'
port = 993
user = os.getenv("user")
password = os.getenv("password")

server = imaplib.IMAP4_SSL(host,port)
server.login(user,password)
server.select("INBOX")
status, data = server.search(None,("UNSEEN"))

if data[0]:
    d = data[0].split()
    ind = d[-1]
    btext = server.fetch(ind, "(BODY[1] BODY[HEADER.FIELDS (SUBJECT FROM)])")
    email_msg = btext[1][1][1]

    utf = quopri.decodestring(email_msg)
    text = utf.decode('utf-8')
    text = re.sub(r'^https?:\/\/.*[\r\n]*', '', text, flags=re.MULTILINE)
    text = text.replace('\r\n\r\n', '###').replace('\r\n', ' ').replace('###', '\r\n\r\n') #pode melhorar
    print(text)

    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if u'PT-BR' in voice.id:
            engine.setProperty('voice', voice.id)
            break
    engine.setProperty("rate", 250)
    engine.say(text)
    engine.runAndWait()
   