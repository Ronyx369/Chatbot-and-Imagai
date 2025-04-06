from PyQt5 import uic

with open("chatbot_info.py", "w", encoding="utf-8") as fout:
    uic.compileUi("info.ui", fout)