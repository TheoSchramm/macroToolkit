# Essentials
import threading # run multiple macros simultaneously
import os # Console UI
import pyautogui # Automation
import keyboard # Keyboard Listener


# Macros spefic
import time 
#import random


# Control variable to exit safely
running = True
def shutdown():
    global running
    running = False


# BASE CLASS, DO NOT TOUCH IT!!!
class Macro():
        def __init__(self, mode: str):
            self.mode = mode.lower()
            self.isEnabled = False
        
        # This method is going to be replaced by future classes w/ Inheritance
        def action(self):
            pass

        def run(self):
            while (running):
                if (self.isEnabled):
                    self.action()
                    if (self.mode == 'single'):
                        self.toggle()
                time.sleep(0.1)

        def toggle(self):
            self.isEnabled = not(self.isEnabled)


# CUSTOM CLASSES EXAMPLES, CREATE ANEW FOR YOUR OWNS MACROS
class exampleSingle(Macro):
    def action(self):
        keyboard.write("Hello World!")

class exampleLoop(Macro):
    def action(self):
        keyboard.write("I'm stuck into a loop!\n")

class AutoClicker(Macro):
    def action(self):
        pyautogui.click()

####################

# Insert you own macro into this list, remember to specify hotkey and mode
allMacros = {
                # YOUR MACRO GOES HERE
                "f1" : exampleSingle("single"),
                "f2" : exampleLoop("loop"),
                "f3" : AutoClicker("loop"),
            }


# Console Interface
def updateConsole():
    os.system('cls')
    print("========[ Macros ]========")
    for key in allMacros.keys():
        macro = allMacros[key]
        print(f"[{key}] {macro.__class__.__name__+':':<15} {('On' if macro.isEnabled else 'Off') if macro.mode == 'loop' else r'N/A':>5}")
    print("[Esc] Exit")
# Set console size
'''cmd = f'mode 27, {int(1.5*len(allMacros))}'
os.system(cmd)'''


# Keyboard Listener | replace this w/ keyboard.hook_key in the future
def keyPress(event):
    if (event.event_type == keyboard.KEY_DOWN):
        if (event.name == 'esc'): shutdown()
        elif (allMacros.get(event.name, False)): 
            allMacros[event.name].toggle()
            updateConsole()
keyboard.hook(keyPress)


macroThreadhs = [threading.Thread(target=i.run) for i in allMacros.values()]
for t in macroThreadhs:
    t.start()
updateConsole()
