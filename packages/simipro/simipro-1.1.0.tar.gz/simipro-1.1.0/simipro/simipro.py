#usr/bin/pyton3
import json
reset = "\033[0m"
black = "\033[1;30m"
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
pink = "\033[1;35m"
cyan = "\033[1;36m"
white = "\033[1;37m"
success = (f"{yellow}[ {green} + {yellow} ]")
error = (f"{yellow}[ {red} - {yellow} ]")
info = (f"{yellow}[ {green} ! {yellow} ]")
errInputJson = {
  "status" : "false",
  "message" : "Parameters not found!",
  "author" : "𝙷𝙰𝚇𝙾𝚁 𝚇𝙽𝚇",
  "owner" : "https://facebook.com/AKXVAU",
  "channel" : "https://t.me/Toxinum"
}
errParameter = json.dumps(errInputJson)
try:
  import os
except Exception as err:
  print(f"{error} {err}")
try:
  import requests
  headers = {'Content-Type': 'application/json'}
except Exception as err:
  print(f"{error} {err}")
  confirm = (input("Install Requirement Auto (Y/n) : ")).lower()
  if confirm == "y":
    os.system("pip3 install requests")
    import request
    headers = {'Content-Type': 'application/json'}
  elif confirm == "n":
    print(f"{error} Cancelled by user!")
  else:
    print(f"{error} Invalid input!")
def simiTalk (ask, lc):
  if not ask:
    return (errParameter)
  elif not lc:
    return (errParameter)
  else:
    None
  json_data = {
    'ask': ask,
    'lc': lc,
  }
  try:
    response = json.loads(requests.post('https://api.toxinum.xyz/v1/simiTalk', headers=headers, json=json_data).text)
    return (response)
  except Exception as err:
    return(f"{error} {err}")
def simiTeach (ask, ans, lc, key):
  if not ask:
    return (errParameter)
  elif not key:
    return (errParameter)
  elif not lc:
    return (errParameter)
  elif not key:
    return (errParameter)
  else:
    None
  json_data = {
    'ask': ask,
    'ans' : ans,
    'lc': lc,
    'key' : key
  }
  try:
    response = json.loads(requests.post('https://api.toxinum.xyz/v1/simiTeach', headers=headers, json=json_data).text)
    return (response)
  except Exception as err:
    return (f"{error} {err}")