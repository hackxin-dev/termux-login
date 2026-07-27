import os 
import time
import signal
import readline

from pwinput import pwinput
from hashlib import sha256

home = "/data/data/com.termux/files/home"

array = []
class auto(object):
	def __init__(self, options):
		self.options = sorted(options)
		
	def complete(self, text, state):
		if state == 0:
			if text:
				self.matches = [s for s in self.options if s and s.startswith(text)]
			else :
				self.matches = self.options[:]
		try:
			return self.matches[state]
		except IndexError:
			return None
def complete(array):
	completer = auto(array)
	readline.set_completer(completer.complete)
	readline.parse_and_bind("tab:complete")

def getPID():
  os.system("ps | grep zsh > ~/.security/PID")
  fp = open(f"{home}/.security/PID", "r").readlines()[0]
  PID = fp.strip().split(" ")[0]
  return PID
    
def checkAgent():
  if os.path.exists(f"{home}/.security/.user"):
    return True
  else:
    return False
    
def getDataAgent():
  if os.path.exists(f"{home}/.security/.user"):
    return open(f"{home}/.security/.user", "r").read()
  else:
    return "None"
    
def handler(signum, frame):
  PID = getPID()
  print()
  print("[!] Access Denied")
  os.system(f"kill -9 {PID}")
    
def main():
  PID = getPID()
  attempt = 3
  if checkAgent():
    while True:
      try:
        if attempt == 0:
          os.system(f"kill -9 {PID}")
        signal.signal(signal.SIGTSTP, handler)
        print("System".center(80))
        print("---------------".center(80))
        print("Welcome back, Agent. Please log in to continue.")
        print()
        username = str(input("[?] Username: "))
        password = pwinput(prompt="[?] Password: ", mask="*")
        attempt -= 1
        if getDataAgent() == sha256(str(f"{username}:{password}").encode()).hexdigest():
          print()
          print("[*] Access Granted")
          time.sleep(2)
          os.system("clear")
          break
        else:
          print(f"[!] Access Denied, Wrong Password, remaining {attempt} attempts")
          time.sleep(2)
          os.system("clear")
      except KeyboardInterrupt:
        print()
        print("[!] Access Denied")
        os.system(f"kill -9 {PID}")
      except EOFError:
        print()
        print("[!] Access Denied")
        os.system(f"kill -9 {PID}")
  else:
    print("System".center(80))
    print("---------------".center(80))
    print("Welcome, agent. Please register to continue.")
    print()
    newUsername = str(input("[?] New Username: "))
    newPassword = pwinput(prompt="[?] New Password: ", mask="*")
    with open(f"{home}/.security/.user", "w") as fu:
      fu.write(sha256(str(f"{newUsername}:{newPassword}").encode()).hexdigest())
      fu.close()
      print()
      print("[*] Successful registration.")
      time.sleep(2)
      os.system("clear")
      
if __name__ == "__main__":
  main()