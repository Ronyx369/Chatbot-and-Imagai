from PyQt5 import uic

with open("chatbot.py", "w", encoding="utf-8") as fout:
    uic.compileUi("ChatBotPencere1.ui", fout)