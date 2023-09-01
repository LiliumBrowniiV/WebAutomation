from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from twocaptcha import TwoCaptcha
import time
import os 
import calendar
from datetime import datetime

options = Options()
service = Service( executable_path="your_path")
options.add_experimental_option("detach", True)
driver = webdriver.Chrome( 
service = service,
options = options)

def getTime():
    now        = datetime.now()
    year       = int(now.strftime("%Y"))
    month      = int(now.strftime("%m"))
    TodayDay   = now.strftime("%d")
    day        = int(now.strftime("%d"))
    monthrange = calendar.monthrange(year, month)
    if day + 8 > monthrange[1]:
        month = str(month + 1).zfill(2)
        day   = str(day + 8 - monthrange[1]).zfill(2)
    elif day + 8 > monthrange[1] and month == 12:
        year  = str(year + 1) 
        month = str(1).zfill(2)
        day   = str(day + 8 - monthrange[1]).zfill(2)
    else:
        year  = str(year).zfill(4)
        month = str(month).zfill(2)
        day   = str(day + 8).zfill(2)
    print("Today is ", year, "/", month,"/", TodayDay, 
          "\nIntend to reserve for ", year, "/", month,"/", day)
    return str(year), str(month), str(day)

def startDrive():
    driver.get("https://fe.xuanen.com.tw/fe01.aspx?Module=net_booking&files=booking_before&PT=1")
    link = driver.find_elements("xpath", "//img[contains(@onclick, 'GoToBooking();')]")
    link[0].click()
    driver.switch_to.alert.accept()
    driver.switch_to.alert.accept()

    username = ""
    password = ""
    usernameplaceholder = driver.find_elements("xpath", "//input[contains(@name, 'ctl00$ContentPlaceHolder1$loginid')]")
    passwordplaceholder = driver.find_elements("xpath", "//input[contains(@name, 'loginpw')]")

    usernameplaceholder[0].send_keys(username)
    passwordplaceholder[0].send_keys(password)


    captcha_img = driver.find_element("xpath", "/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[3]/td[2]/img")
    captcha_img.screenshot('your_path')


    api_key = os.getenv('APIKEY_2CAPTCHA', 'your_key')

    solver = TwoCaptcha(api_key)

    try:
        result = solver.normal('your_path')

    except Exception as e:
        print(e)
    else:
        code = result['code']
        return code

def process(code, year, month, day):
    driver.find_element("xpath", "/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[3]/td[2]/input").send_keys(code)
    driver.find_element("xpath", "/html/body/div[2]/div/div[3]/button[1]").click()
    driver.find_element("xpath", "/html/body/table[2]/tbody/tr/td/form/table/tbody/tr[4]/td/input").click()

    now = datetime.now()
    hour = now.strftime("%H")
    min  = now.strftime("%M")
    sec  = now.strftime("%S")
    print("Timestamp", hour, " : ", min, " : ", sec)
    time.sleep(((59 - int(min)) * 60) + (59 - int(sec)) + 1)
    DoneTime = datetime.now()
    print("Done Time", DoneTime.strftime("%H:%M:%S"))

    driver.get("https://fe.xuanen.com.tw/fe01.aspx?module=net_booking&files=booking_place&StepFlag=2&PT=1&D="+year+"/"+month+"/"+day+"&D2=1")
    driver.find_element("xpath", "/html/body/table[1]/tbody/tr[3]/td/div/form/table/tbody/tr/td/span/div/table/tbody/tr[2]/td/span/table/tbody/tr[27]/td[3]/img").click()
    driver.switch_to.alert.accept()
    time.sleep(600)

def main():
    year, month, day = getTime()
    process(startDrive(), year, month, day)

if __name__ == "__main__":
    try:
        main()
        time.sleep(600)   
    except Exception as e:
        print(e)
        print("fuck me")
        time.sleep(600)   
