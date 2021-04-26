from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os
import random
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from multiprocessing import Pool
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import re 
import os

cwd = os.getcwd()

opts = Options()
opts.headless = True
opts.add_argument('log-level=3') 
dc = DesiredCapabilities.CHROME
dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}

opts.add_argument('--disable-blink-features=AutomationControlled')
opts.add_experimental_option('excludeSwitches', ['enable-logging'])
path_browser = f"{cwd}\chromedriver.exe"
browser = webdriver.Chrome(options=opts, desired_capabilities=dc, executable_path=path_browser)
global point
global n
n = 1
global url
global email
global password

def get_voc(email, password,point,browser):
    # browser.save_screenshot("GET_VOUCHER.png")
    get_voc = wait(browser,20).until(EC.presence_of_element_located((By.XPATH,'//*[@id="root"]/div/div[2]/div[2]/div[2]/div[3]'))).text
    
    # clear = re.search("voucher (\w+)", get_voc)
    # voc = clear.group(1)
    print(f"[*] [ {email} ] Message: {get_voc}")
    with open('getVoucher.txt','a') as f:
        f.write('{0} | {1} | Point:{2} | Message : {3}\n'.format(email,password,point[0],get_voc))
     

def get_message(email, password, browser):
    sleep(3)
    # browser.save_screenshot("GET_MESSAGE.png")
    get_time =  wait(browser,20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[2]/span'))).text
    print(f"[*] [ {email} ] Waktu pada pesan: {get_time}")
    # clear_time = re.findall(r'\b\d+\b', get_time)
    # print(clear_time)
    try:
        if get_time == "0m":
            wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[3]/div[2]/div[1]/div/div[1]/div[2]/div[1]/div[1]'))).click()
        else:
            if n == 3:
                get_voc(email,password,point,browser)
            else:
                n+1
                browser.refresh()
                get_message(email, password, browser)
                pass
    except:

        if n == 3:
            get_voc(email,password,point,browser)
        else:
            n+1
            browser.refresh()
            get_message(email, password, browser)
            pass

def login_twitter(k):
    global point
    global url
    global browser
    k = k.split("|")
    email = k[0]
    password = k[1]
     
    try:
        browser.get("https://twitter.com/login")
        print(f"[*] [ {email} ] Please wait, trying to login twitter!")
        sleep(3)
        browser.save_screenshot("LOGIN_TWITTER.png")
        element = wait(browser,35).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[1]/label/div/div[2]/div/input')))
        element.send_keys(email)
        sleep(0.5)
        element = wait(browser,15).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[2]/label/div/div[2]/div/input')))
        element.send_keys(password)
        sleep(0.5)
        wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[2]/form/div/div[3]/div/div/span/span'))).click()
        
        sleep(3)
        
        if "/login" in browser.current_url:
            get_warn = wait(browser, 5).until(EC.presence_of_element_located((By.XPATH, '/html/body/div/div/div/div[2]/main/div/div/div[1]/div/span'))).text
            print(f"[*] {get_warn}")
            print(f"[*] [ {email} ] Failed Login")
            with open('failedLoginTwitter.txt','a') as f:
                f.write('{0}|{1}\n'.format(email,password))

        else:

            browser.get("https://my.telkomsel.com/")
            
            sleep(10)
            
            wait(browser,50).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/div[2]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[2]/div/button/div/div/span/span'))).click()
            sleep(5)
            # browser.save_screenshot("LOGIN_TSEL.png")
            # print(f"   \n================================\n")
            try:
                browser.switch_to_window(browser.window_handles[1])
                
                wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="allow"]'))).click()
                
                sleep(2)
                
                
            except:
                pass
            browser.switch_to_window(browser.window_handles[0])
            # print(f"   \n================================\n") 

            sleep(10)
            try: 
                get_point = wait(browser,60).until(EC.presence_of_element_located((By.CSS_SELECTOR,'.Dashboard-container__dashboardContainer___9ljIU > .DashboardMainContent-component__dashboardMainContentComponent___20Ibz > .DashboardMainContent-component__mainContent___1f1O_ > .DashboardMainContent-component__userDetail___1Kqx3 > .DashboardLoyaltyPoin-component__dashboardloyaltypoinComponent___VwkjH'))).text
                point = re.findall(r'\b\d+\b', get_point)
                print(f"[*] [ {email} ] Success Login")
                with open('successLoginTwitter.txt','a') as f:
                    f.write('{0}|{1}|{2}\n'.format(email,password,point[0]))
            
                print(f"[*] [ {email} ] Your Point: {point[0]}")
                # browser.save_screenshot("POINT.png")
                sleep(0.5)
                file_list_url = "kodevoc.txt"
                myfile_url = open(f"{cwd}/{file_list_url}","r")
                list_account_url = myfile_url.read()
                new_url = list_account_url.split("|") 
                # link_url = input("[*] Kode Voucher \n[*] Bila lebih dari 1 voucher, pisahkan dengan | tanpa spasi, contoh: KODE1|KODE2|KODE3 : ")
                # new_url = link_url.split("|")
                
                # try:
                for url in new_url:
                    
                    browser.get(f"https://my.telkomsel.com/app/loyalty-reward-details/{url}")
                    print(f"[*] [ {email} ] Go To Voucher: {browser.current_url}")
                
                    sleep(5)
                    #klik tukar
                    browser.save_screenshot(f"VOUC+{url}.png")
                    element = wait(browser,20).until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/div/button')))
                    browser.execute_script("arguments[0].scrollIntoView();", element)
                    # browser.save_screenshot("SCROLL.png")
                    sleep(3)
                    wait(browser,15).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[2]/div[2]/div[4]/div/div[2]/div/button'))).click()
                    sleep(3)
                
                    title_first = wait(browser,20).until(EC.presence_of_element_located((By.XPATH,'/html/body/div[1]/div/div[1]/div/div[1]/div/span'))).text
                    
                    # print(title_first)
                    browser.save_screenshot(f"VOUC+1+{url}.png")
                    sleep(3)
                
                    try:
                        if "Setuju" in title_first:
                            #click confirm
                            wait(browser,10).until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div[1]/div/div[3]/button[2]/span'))).click()
                            sleep(3)
                            browser.save_screenshot("SETUJU.png")
                            browser.get("https://my.telkomsel.com/app/inbox")
                            sleep(3)
                            #click messange
                            print(f"[*] [ {email} ] Trying to check new inbox")
                            get_message(email, password, browser)
                            sleep(5)
                            get_voc(email,password,point,browser)
                        elif "Info" in title_first: 
                            print(f"[*] [ {email} ] Point Tidak Cukup atau Voucher tidak dapat diredeem")
                            
                    except:
                        print(f"[*] [ {email} ] Finish")
                        browser.quit()
                        
                print(f"[*] [ {email} ] Finish!")
                browser.quit()
                    

                # except:
                #     # browser.save_screenshot("ERROR_WARN_THIRD.png")
                #     print(f"[*] [ {email} ] Finish, The Job is Done!***")
                #     browser.quit()
                #     pass
            except:
                browser.save_screenshot("ERROR_WARN_SECOND.png")
                print(f"[*] [ {email} ] Something Error at Second Step")
                browser.quit()
            
    except:
        browser.save_screenshot("ERROR_WARN_FIRST.png")
        print(f"[*] [ {email} ] Something Error at First Step")
        browser.quit()
        

if __name__ == '__main__':
    global list_accountsplit
    global k
    print("[*] Automation Get Point and Reedeem Reward Telkomsel")
    print("[*] Format: email|password")
    jumlah = int(input("[*] Jumlah Proses Data (Spek PC Tinggi, isi bebas (rekomen 3), namun perhatikan jumlah akun twitternya. Spek PC rendah, isi 1 saja) : "))
    file_list = "twitter.txt"
    
    myfile = open(f"{cwd}/{file_list}","r")
    list_account = myfile.read()
    list_accountsplit = list_account.split() 
    with Pool(jumlah) as p:  
        p.map(login_twitter, list_accountsplit)
        
