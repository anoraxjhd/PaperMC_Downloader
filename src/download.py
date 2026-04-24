from requests import get
import src.translate as translate
from threading import Thread
import src.vars as vars

mb = None

def setupDownload(version, build, resultLabel = None):
  if build:
    url = beforeSend(version, build, resultLabel=resultLabel)
    Thread(target=download, args=(url,), daemon=True).start()
  else:
    url = beforeSend(version, resultLabel=resultLabel)
    Thread(target=download, args=(url,), daemon=True).start()

def getData(URL):
  global terminalClose
  response = get(URL)
  status = response.status_code
  if status in vars.allowedStatus:
    return response.json()
  else:
    if vars.no_gui:
      print(f"\n{translate.translate("Error")}: {translate.translate("Invalid status code")}: {status}"); vars.terminalClose = True; return
    mb.showerror(translate.translate("Error"), f"{translate.translate("Invalid status code")}: {status}"); vars.app.destroy()

def download(URL : str):
  if URL == 1: return 1
  if not URL.startswith("https://") and not URL.startswith("http://"): return 1
  if vars.no_gui:
    print(f"{translate.translate("download started")}")
  else:
    mb.showinfo(translate.translate("Download"), f"{translate.translate("download started")}")
  with open(str(URL).split("/")[-1], 'wb') as f:
    f.write(get(URL).content)
  if vars.no_gui:
    print(f"\n{translate.translate("File saved to")}: {vars.savePath}")
  else:
    mb.showinfo(translate.translate("Download"), f"{translate.translate("File saved to")}: {vars.savePath}")

def send(version, build = "latest", resultLabel = None):
  # Setup stuff
  if not version.count(".") >= 1: return False
  global paperURL, versionURL
  versionURL = f"https://fill.papermc.io/v3/projects/{vars.project}/versions/{version}/builds"
  try:
    data = get(versionURL).json()
  except:
    if not vars.no_gui:
      resultLabel.configure(text=f"Paper {version} {translate.translate("not found")}.")
      return False
    else:
      print(f"Paper {version} {translate.translate("not found")}.")
      return False
  
  # Check if data is a list (valid response)
  if not isinstance(data, list):
    if not vars.no_gui:
      resultLabel.configure(text=f"Paper {version} {translate.translate("not found")}.")
      return False
    else:
      print(f"Paper {version} {translate.translate("not found")}.")
      return False
  
  # Checking if build is supposed to be latest
  if build == "latest":
    try:
      paperURL = data[0]["downloads"]["server:default"]["url"]
      if not vars.no_gui:
        resultLabel.configure(text=f"Paper {version} {translate.translate("found")}.\n{translate.translate("Press ""Download"" to download Paper")}.")
        return paperURL
      else:
        print(f"Paper {version} {translate.translate("found")}.\n{translate.translate("Downloading")}...")
        return paperURL
    except (KeyError, IndexError):
      if not vars.no_gui:
        resultLabel.configure(text=f"Paper {version} {translate.translate("not found")}.")
        return False
      else:
        print(f"Paper {version} {translate.translate("not found")}.")
        return False
  else:
    try:
      for i in data:
        if isinstance(i, dict) and i.get("id") == int(build):
          if vars.no_gui:
            print(f"Paper {version} {translate.translate("found")}.\n{translate.translate("Downloading")}..."); return i["downloads"]["server:default"]["url"]
          resultLabel.configure(text=f"Paper {version} Build: {build} {translate.translate("found")}.\n{translate.translate("Press ""Download"" to download Paper")}.")
          return i["downloads"]["server:default"]["url"]
      else:
        if not vars.no_gui:
          resultLabel.configure(text=f"Paper {version} Build: {build} {translate.translate("not found")}.")
        else:
          print(f"Paper {version} Build: {build} {translate.translate("not found")}.")
        return False
    except (ValueError, TypeError):
      if not vars.no_gui:
        resultLabel.configure(text=f"Paper {version} Build: {build} {translate.translate("not found")}.")
      else:
        print(f"Paper {version} Build: {build} {translate.translate("not found")}.")
      return False
    
def beforeSend(version = "", build = "latest", resultLabel = None):
  global mb
  if not vars.no_gui:
    import tkinter.messagebox as mb
  if not vars.no_gui and not version:
    mb.showinfo(f"{translate.translate("Enter a version")}.", f"{translate.translate("Enter a version")}."); return 1
  if vars.no_gui and not version:
    print(f"{translate.translate("Enter a version")}."); return 1
  if not build: build = "latest"
  data = send(version=version, build=build, resultLabel=resultLabel)
  return data