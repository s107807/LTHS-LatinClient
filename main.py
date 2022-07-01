version = 0.1


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json, time, validators, os, requests, sys

if os.name == 'nt':
    subDirectory = '\\'
else:
    subDirectory = '/'

if len(sys.argv) >= 2:
    if sys.argv[1] == '--compile':
        os.system(f"pyinstaller main.py --icon {str(json.load(open('settings.json'))['configuration']['icon'])}")
        input('[+] Compiled')
        sys.exit()

if os.path.exists('settings.json') == False:
    open('settings.json').write(requests.get('https://s107807.github.io/LTHS-LatinClient/settings.json').content)

print(f'\033[1;33;40m[+] Starting Client v{version}')

def clear_console():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def loadWait(by, type):
    try:
        WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, type)))
        return True
    except:
        print(f'unable to load element: {type}')
        return False

#! ---------->SETUP START<----------
if str(json.load(open('settings.json'))['configuration']['browser-type']) == "none":
    webbrowserTypes = ['Chrome', 'Chromium', 'Brave', 'Firefox', 'Internet Explorer', 'Edge', 'Opera']
    print('Browser Types:\n------------')
    for a in range(len(webbrowserTypes)):
        print(webbrowserTypes[a])
    print('------------')
    while True:
        webbrowserType = str(input('please enter your browser: '))
        if webbrowserType in webbrowserTypes:
            break
        else:
            print('please enter a valid browser type')
    with open('settings.json', 'r+') as f:
        data = json.load(f)
        data['configuration']['browser-type'] = webbrowserType
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

webbrowserType = str(json.load(open('settings.json'))['configuration']['browser-type'])

if str(json.load(open('settings.json'))['schoology']['latin-link']) == "none":
    print('please enter the schoology link for the latin app')
    while True:
        latinLink = str(input('link: '))
        if validators.url(latinLink) == True:
            break
        else:
            print('invalid url')
    with open('settings.json', 'r+') as f:
        data = json.load(f)
        data['schoology']['latin-link'] = latinLink
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

if str(json.load(open('settings.json'))['schoology']['username']) == "none":
    username = str(input('please enter schoology username: '))
    password = str(input('please enter schoology password: '))
    clear_console()
    with open('settings.json', 'r+') as f:
        data = json.load(f)
        data['schoology']['username'] = username
        data['schoology']['password'] = password
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

latinLink = str(json.load(open('settings.json'))['schoology']['latin-link'])
schoologyUser = str(json.load(open('settings.json'))['schoology']['username'])
schoologyPass = str(json.load(open('settings.json'))['schoology']['password'])
delay = int(json.load(open('settings.json'))['configuration']['timeout-delay'])

try:
    if webbrowserType == 'Chrome' or webbrowserType == 'Chromium' or webbrowserType == 'Brave':
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.core.utils import ChromeType
        options = Options()
        options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
        options.add_experimental_option('prefs', {"credentials_enable_service": False, "profile.password_manager_enabled": False})
        if webbrowserType == 'Chrome':
            driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        elif webbrowserType == 'Chromium':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install(), options=options)
        elif webbrowserType == 'Brave':
            driver = webdriver.Chrome(ChromeDriverManager(chrome_type=ChromeType.BRAVE).install(), options=options)

    elif webbrowserType == 'Firefox':
        from webdriver_manager.firefox import GeckoDriverManager
        driver = webdriver.Firefox(executable_path=GeckoDriverManager().install())

    elif webbrowserType == 'Internet Explorer':
        from webdriver_manager.microsoft import IEDriverManager
        driver = webdriver.Ie(IEDriverManager().install())

    elif webbrowserType == 'Edge':
        from webdriver_manager.microsoft import EdgeChromiumDriverManager
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())

    elif webbrowserType == 'Opera':
        from webdriver_manager.opera import OperaDriverManager
        driver = webdriver.Opera(executable_path=OperaDriverManager().install())
except:
    input(f'\033[1;31;40m[-] Failed to Start Client v{version}')
    sys.exit()


clear_console()
#! ---------->SETUP END<----------

try:
    driver.get(latinLink)
    print('[+] Successfully Connected to Schoology')
except:
    print('[-] Failed to Connect to Schoology')
if loadWait(By.ID, 'edit-mail'):
    driver.find_element(By.ID, 'edit-mail').send_keys(schoologyUser)
if loadWait(By.ID, 'edit-pass'):
    driver.find_element(By.ID, 'edit-pass').send_keys(schoologyPass)
if loadWait(By.ID, 'edit-submit'):
    driver.find_element(By.ID, 'edit-submit').click()
if loadWait(By.ID, 'schoology-app-container'):
    print('[+] Successfully Logged In')
    time.sleep(3)
    try:
        driver.get('https://lthslatin.org')
        print('[+] Successfully Loaded LTHS Latin')
    except:
        print('[-] Failed to load LTHS Latin')

if loadWait(By.CLASS_NAME, 'ui-title'):
    user = str(str(str(driver.find_element(By.CLASS_NAME, 'ui-title').text).split("'s")[0]).lower()).title()
    print(f'[+] Located user: {user}')
else:
    print('[+] Unable to Find User')
modes = ['synopsis', 'noun-adj', 'launchpad', '(grasp)', 'reading', 'composition', 'ciples', 'infinitive morphology']
mode = 'launchpad'
print(f'\033[1;32;40m[+] Successfully Started Client v{version}')
while True:
    try:
        for a in range(len(driver.find_elements(By.CLASS_NAME, 'ui-title'))):
            for b in range(len(modes)):
                if modes[b] in str(driver.find_elements(By.CLASS_NAME, 'ui-title')[a].text).lower():
                    mode = modes[b]
    except:
        #! must have closed webpage
        sys.exit()
    if mode == 'synopsis':
        #Finds latin conjugation type
        conjugationNames = ['first', 'second', 'third', 'thirdI', 'fourth']
        totalConjugations = [['ō', 'āre', 'vī', 'us'], ['eō', 'ēre', 'ī', 'us'], ['ō', 'ere', 'ī', 'us'], ['iō', 'ere', 'ī', 'us'], ['iō', 'īre', 'ī', 'us']]
        latinWords = []
        blocks = ['a', 'b', 'c', 'd']
        for a in range(len(blocks)):
            try:
                latinWords.append(driver.find_element(By.XPATH, f"// li[@class='ui-block-{str(blocks[a])}']").text)
            except:
                latinWords.append(f'unable to get word {a}')
        print(latinWords)
        outputChoice = []
        for a in range(len(totalConjugations)):
            for b in range(4):
                if totalConjugations[a][b] not in latinWords[b]:
                    continue
                outputChoice.append(totalConjugations[a])
        numberCount = []
        for a in range(len(outputChoice)):
            tempText = ''
            for b in range(len(outputChoice[a])):
                tempText += outputChoice[a][b]
            numberCount.append(len(tempText))
        print(conjugationNames[totalConjugations.index(outputChoice[numberCount.index(max(numberCount))])])
        print((driver.find_element(By.XPATH, f"// li[@class='ui-block-e']").text).split(' |')[0])
        print((driver.find_element(By.XPATH, f"// li[@class='ui-block-e']").text).split('| ')[1])

driver.close()