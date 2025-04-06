from PyQt5 import uic

with open("chatbot_anamenu.py", "w", encoding="utf-8") as fout:
    uic.compileUi("AnaMenu.ui", fout)