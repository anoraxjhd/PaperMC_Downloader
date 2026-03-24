# Imports
from requests import get
import customtkinter as ctk
from tkinter import messagebox as mb
from webbrowser import open

# Settings
ctk.set_appearance_mode("dark")
URL = "https://qing762.is-a.dev/api/papermc/"
allowedStatus = [
  200, 203
]

def getData():
  global data
  response = get(URL)
  status = response.status_code
  if status in allowedStatus:
    data = response.json()
  else:
    mb.showerror(f"Fehler {status}", f'Servers response is: {status}')

def send(version = "", data = ""):
  global paperURL
  if version in data['versions']:
    resultLabel.configure(text=f"Paper {version} Gefunden. \n Drücke Auf ""Download"" um Paper herunterzuladen.")
    paperURL = data['versions'][version]
  else:
    resultLabel.configure(text=f"Paper {version} nicht gefunden.")

def beforeSend(version = "", data = ""):
  if not data: mb.showerror(f"Fehler", f'Data is None are you Online?'); return 1
  if not version: resultLabel.configure(text=f"Gebe eine Version ein."); return 1
  send(version, data)

def GUI():
  global resultLabel, versionInput
  app = ctk.CTk()
  app.geometry("400x200")
  app.title("PaperMC Downloader")
  app.iconbitmap("icon.ico")

  resultLabel = ctk.CTkLabel(app, text="/")
  resultLabel.pack(padx=20, pady=10)

  download = ctk.CTkButton(app, text="Herunterladen", command=lambda: open(paperURL))
  download.pack(padx=50)

  versionInput = ctk.CTkEntry(app, placeholder_text="Version")
  versionInput.pack(padx=20, pady=20)

  submit = ctk.CTkButton(app, text="Senden", command=lambda: beforeSend(version=versionInput.get(), data=data))
  submit.pack(padx=20)

  app.mainloop()

getData()
GUI()
