# Imports
from requests import get
import customtkinter as ctk
from tkinter import messagebox as mb
from webbrowser import open as wbopen
from json import load


# VARS
paperURL = ""

# Settings

customLang = True
lang = "de"
ctk.set_appearance_mode("dark")
URL = "https://qing762.is-a.dev/api/papermc/"
allowedStatus = [200, 203]
if customLang:
  with open("translations.json", "r", encoding="UTF-8") as f:
    translations = load(f)

def translate(text, lang="en"):
  try:
    return translations.get(lang, {}).get(text, text)
  except:
    return text

def getData():
  global data, status
  response = get(URL)
  status = response.status_code
  if status in allowedStatus:
    data = response.json()
  else:
    mb.showerror(str(translate("Error", lang=lang)) + " " + str(status), f'{translate("Servers response is", lang=lang)}: {status}')

def send(version = "", data = ""):
  global paperURL
  if version in data['versions']:
    resultLabel.configure(text=f"Paper {version} {translate("found", lang=lang)}. \n {translate("Press ""Download"" to download Paper", lang=lang)}.")
    paperURL = data['versions'][version]
  else:
    resultLabel.configure(text=f"Paper {version} {translate("not found", lang=lang)}.")

def beforeSend(version = "", data = ""):
  if not data: mb.showerror(translate("Error", lang=lang), f'{translate("Data is None are you Online", lang=lang)}?'); return 1
  if not version: resultLabel.configure(text=f"{translate("Enter a version", lang=lang)}."); return 1
  send(version, data)

def openBrowser(URL):
  if not URL: resultLabel.configure(text=f"{translate("Enter a Version and Click Send", lang=lang)}."); return 1
  wbopen(URL)

def GUI():
  global resultLabel, versionInput
  app = ctk.CTk()
  app.geometry("400x200")
  app.title("PaperMC Downloader")
  app.iconbitmap("icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  download = ctk.CTkButton(app, text=translate("Download", lang=lang), command=lambda: openBrowser(paperURL))
  download.pack(padx=50)

  versionInput = ctk.CTkEntry(app, placeholder_text=translate("Version", lang=lang))
  versionInput.pack(padx=20, pady=20)

  submit = ctk.CTkButton(app, text=translate("Send", lang=lang), command=lambda: beforeSend(version=versionInput.get(), data=data))
  submit.pack(padx=20)

  app.mainloop()

getData()
if status in allowedStatus: GUI()
