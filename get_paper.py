import requests
import customtkinter as ctk
from tkinter import messagebox as mb

extra_help = True
debug = False
console = False
ErrorTesting = False
if debug == True:
    if ErrorTesting == True:
        URL = "https://google.com/DEBUG/api"
else:
    URL = "https://qing762.is-a.dev/api/papermc"
       

response = requests.get(URL)
response.encoding = "utf-8"

if response.status_code == 200:
    if debug == True:
        if console == True:
            print("Erfolgreich Verbunden.")
    data = response.json()
    if console == True:
        print(response.text)
else:
    ConnectionErrorOnRequest1 = 'Fehler beim Verbinden mit dem Server. Status Code: '
    ConnectionErrorOnRequest2 = response.status_code
    ConnectionErrorOnRequest = ConnectionErrorOnRequest1 + str(ConnectionErrorOnRequest2)
    mb.showerror("Fehler beim Verbinden mit dem Server.", ConnectionErrorOnRequest)
    if console == True:
         print("Error While Connecting: ",ConnectionErrorOnRequest)
    if response.status_code == 404:
            mb.showerror("Fehler 404", "Die angeforderte Ressource wurde nicht gefunden.")
    exit()

app = ctk.CTk()

app.geometry("400x200")
app.title("PaperMC Downloader")
app.iconbitmap("C:\\users\\felix\\Downloads\\official-minecraft-style-icons-removebg-preview.ico")

result_label = ctk.CTkLabel(app, text="/")
result_label.pack(padx=20, pady=10)


def copy_callback():
    text_to_copy = copy_label.cget("text")  # holt den Text aus dem Label
    app.clipboard_clear()
    app.clipboard_append(text_to_copy)

copy_button = ctk.CTkButton(app, text="Copy", command=copy_callback)
copy_button.pack(padx=50)

input_version = ctk.CTkEntry(app, placeholder_text="Version")
input_version.pack(padx=20, pady=20)

def button_callback():
      eingabe = input_version.get()
      target_version = eingabe

      if target_version in data['versions']:
            if console == True:
                print(f"Version {target_version} -> URL: {data['versions'][target_version]}")
            result_label.configure(text="/")
            result_label.configure(text=f"Version {eingabe}: {data['versions'][target_version]}")
            copy_label.configure(text=f"{data['versions'][target_version]}")
      else:
            if console == True:
                  print(f"Version {target_version} nicht gefunden.")
            result_label.configure(text="Version nicht gefunden")

submit = ctk.CTkButton(app, text="Senden", command=button_callback)
submit.pack(padx=20, pady=8)

copy_label = ctk.CTkLabel(app, text="NAN")
copy_label.pack(padx=28830, pady=14550)

app.mainloop()
