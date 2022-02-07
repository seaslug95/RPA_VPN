import pyautogui as pag
import pyperclip
import time

### Parameters
path_im = './pics/'

button_pulseconnect = 'button_pulseconnect.png'
button_pulsefinalconnect = 'button_pulsefinalconnect.png'
im_pulseconnect = 'im_pulseconnect.png'

### Functions
def waitim(im: str, dl: int) -> float:
    """
    Returns time it took for image im to load.
    Returns None in case of error or if image 
    not found after deadline dl.
    """
    tic = time.time()
    toc = tic
    pos = None
    while pos == None:
        try:
            pos = pag.locateOnScreen(im, confidence=(0.95))
            toc = time.time()
            if pos != None:
                res = round(toc - tic, 2)
            if toc - tic > dl:
                print('Not found after {} sec :'.format(dl), im)
                pos = 0
                res = None
        except: # Probably related to opencv-python
            print('Error looking for :', im)
            pos = 0
            res = None
    return res

def clickim(im: str, nclick: int, dl: int) -> float:
    """
    Returns time it took to simple click or double click
    in the center of an image im.
    Returns None in case of error or if image 
    not found after deadline dl.
    """
    nclick_valid = [1, 2]
    if nclick not in nclick_valid:
        raise ValueError('Number of clicks (nclick) must be 1 or 2')
    tic = time.time()
    toc = tic
    pos = None
    while pos == None:
        try:
            pos = pag.locateOnScreen(im, confidence=(0.95))
            toc = time.time()
            if pos != None:
                pos = pag.center(pos) # Central coord of im
                pag.click(pos[0], pos[1]) if nclick == 1 else pag.doubleClick(pos[0], pos[1])
                res = round(toc - tic, 2)
            if toc - tic > dl:
                print('Could not be clicked on after {} sec :'.format(dl), im)
                pos = 0
                res = None
        except: # Probably related to opencv-python
            print('Error clicking on :', im)
            pos = 0
            res = None
    return res

def getpsw(entry: str) -> str:
    """
    Returns password of KeePass entry.
    """
    pag.press('win')
    pag.write('KeePass 2')
    pag.press('enter')
    time.sleep(2)
    pag.hotkey('ctrl', 'f')
    time.sleep(1)
    pag.write(entry)
    pag.press('enter')
    time.sleep(2)
    pag.hotkey('ctrl', 'c')
    psw = pyperclip.paste()
    return psw

### Script
pag.PAUSE = 1 # Add pause after every command

# Open Pulse
pag.press('win')
pag.write('Pulse Secure')
pag.press('enter')
clickim(im=path_im+button_pulseconnect, nclick=1, dl=5) # Click Pulse Connect button
waitim(im=path_im+im_pulseconnect, dl=30) # Wait Pulse to load

# Extract Pulse password (first part) from KeePass
getpsw(entry='Pulse Secure')

# Provide Pulse password (first part) in Pulse
pag.press('win')
pag.write('Pulse Secure')
pag.press('enter')
clickim(im=path_im+im_pulseconnect, nclick=1, dl=5) # Click Pulse Connect image to provide password
pag.hotkey('ctrl', 'v')

# Extract Entrust password from KeePass
psw_entrust = getpsw(entry='Entrust')

# Extract Pulse password (second part) from Entrust
pag.press('win')
pag.write('IdentityGuard Soft Token')
pag.press('enter')
time.sleep(1)
for n in psw_entrust:
    pag.press(n)
    # time.sleep(0.5)
time.sleep(2)
pag.hotkey('ctrl', 'c')

# Provide Pulse password (second part) in Pulse
pag.press('win')
pag.write('Pulse Secure')
pag.press('enter')
clickim(im=path_im+im_pulseconnect, nclick=1, dl=5) # Click Pulse Connect image to provide password
pag.hotkey('ctrl', 'v')
clickim(im=path_im+button_pulsefinalconnect, nclick=1, dl=5) # Click Pulse Connect button
