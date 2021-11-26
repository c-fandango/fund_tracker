from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import holidays
import json
from datetime import date
from pyvirtualdisplay import Display 

today=date.today()
if today in holidays.GB():
    print('holiday')
    exit()

if date.today().weekday() == 5:
    print('wekend')
    exit()
if date.today().weekday() == 6:
    print('wekend')
    exit()

display = Display(visible=0, size=(1024, 768))
display.start()
path = "/usr/lib/chromium-browser/chromedriver"
driver = webdriver.Chrome(path)
funds={"":{"code":"","shareqty":,"type":""},"":{"code":"","shareqty":,"type":""},
          "":{"code":"","":,"type":""},"":{"code":"","shareqty":,"type":""},
          "":{"code":"","shareqty":,"type":""},
          "":{"code":"","shareqty":,"type":""},
          "":{"code":"","shareqty":,"type":""},
          "":{"code":"", "shareqty":,"type":""},
           "":{"shareqty":,"type":"","shareprice": }}

with open('/home/pi/pythonbotProject1/fundinfo.txt','r') as file:
    funds= dict(json.load(file))

for fund in funds:
    if funds[fund]["type"]=="unit":
        driver.get(f"https://www.share.com/investments/shares/{funds[fund]['code']}#prices-and-trades")
        time.sleep(2)
        driver.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div/div[7]/div[1]/div/div[1]/section/div[4]/div/div/div[1]/div[1]/div/section/div/div[2]/div/div/div/table/tbody/tr[1]/td/span")))
            time.sleep(2)
        except:
            driver.quit()
        shareprice= driver.find_element_by_xpath("/html/body/div[2]/div/div[7]/div[1]/div/div[1]/section/div[4]/div/div/div[1]/div[1]/div/section/div/div[2]/div/div/div/table/tbody/tr[1]/td/span")
    if funds[fund]["type"]=="fund":
        driver.get(f"https://markets.ft.com/data/funds/tearsheet/summary?s={funds[fund]['code']}")
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[1]/span[2]")))
        except:
            driver.quit()
        shareprice=driver.find_element_by_xpath("/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[1]/span[2]")
    if funds[fund]["type"]=="etf":
        driver.get(f"https://markets.ft.com/data/etfs/tearsheet/summary?s={funds[fund]['code']}")
        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[1]/span[2]")))
        except:
            driver.quit()
        shareprice=driver.find_element_by_xpath("/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[2]/ul/li[1]/span[2]")
    if funds[fund]["type"]=="share":
        driver.get(f"https://markets.ft.com/data/equities/tearsheet/summary?s={funds[fund]['code']}")

        try:
            element = WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div[2]/section[1]/div/div/div[1]/div[3]/ul/li[1]/span[2]")))
        except:
            driver.quit()
    if funds[fund]["type"]=="cash":
        continue
    funds[fund]["shareprice"]=round(float(shareprice.text.replace(',','')),2)

total=0
for fund in funds:
    funds[fund]["fundvalue"]=round(funds[fund]["shareqty"]*funds[fund]["shareprice"],2)
    total=round(total+funds[fund]["fundvalue"],2)
    print(fund +'value',funds[fund]["fundvalue"])

for fund in funds:
    with open(f"/home/pi/pythonbotProject1/{fund}data.txt",'r') as file:
        fundset=json.load(file)

    fundset.append(funds[fund]["fundvalue"])

    with open(f"/home/pi/pythonbotProject1/{fund}data.txt", 'w') as file:
        json.dump(fundset, file)


with open("/home/pi/pythonbotProject1/datesdata.txt",'r') as file:
    dates=json.load(file)
    
todaydate=date.today()
dates.append(todaydate.strftime("%Y-%m-%d"))

with open("/home/pi/pythonbotProject1/datesdata.txt", 'w') as file:
    json.dump(dates, file)

print('no error in writing')

display.stop()


