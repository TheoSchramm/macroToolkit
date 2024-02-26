# Essencials
import threading # responsivity, i guess
import os # console UI
import pyautogui # mouse  
import keyboard # keyboard, duhn

# Macros spefic
import time 
import random
import pydirectinput

# Control variable to exit safely
running = True

# BASE CLASS, DO NOT TOUCH IT!!!
class Macro():
        def __init__(self, key: str, mode: str):
            self.key = key.lower()
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
allMacros = [
            # YOUR MACRO GOES HERE,
            exampleSingle("F1", "single"),
            exampleLoop("F2", "loop"),
            AutoClicker("F3", "loop"), 
        ]

# Console Interface
def updateConsole(needUpdate: bool):
    if (needUpdate):
        os.system('cls')
        print("========[ Macros ]========")
        for macro in allMacros:
            print(f"[{macro.key.upper()}] {macro.__class__.__name__+':':<15} {('On' if macro.isEnabled else 'Off') if macro.mode == 'loop' else r'N/A':>5}")
# Set console size
cmd = f'mode 27, {int(1.5*len(allMacros))}'
os.system(cmd)

# Keyboard Listener
def keyPress(event):
    needUpdate = False
    for macro in allMacros:
            # Debug Key Listener
            #print(event.name)

            # Exit
            if (event.event_type == keyboard.KEY_DOWN) and (event.name.lower() == "z"):
                global running
                running = False
                for t in macroThreadhs:
                    t.join()

            # Toggle Macro
            if (event.event_type == keyboard.KEY_DOWN) and (event.name.lower() == macro.key):
                macro.toggle()
                needUpdate = True
    updateConsole(needUpdate)
keyboard.hook(keyPress)

macroThreadhs = [threading.Thread(target=macro.run) for macro in allMacros]
for t in macroThreadhs:
    t.start()
updateConsole(True)
