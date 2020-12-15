from selenium import webdriver
import time
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pynput.keyboard import Key, Controller
import traceback
keyboard = Controller()

options = webdriver.FirefoxOptions()

#options.add_argument("--headless")
#options.add_argument('--window-size=1920,1080')
#options.add_argument('--no-sandbox')
#options.add_argument('--start-maximized')
#options.add_argument('--disable-setuid-sandbox')
#options.add_argument('--disable-gpu')
 
driver = webdriver.Firefox(firefox_options=options)
# part 1------------------------------------------------------------------------------------------------------------------------------------------------
driver.get('https://onlinena.vfsglobal.com/Appointment/')


      
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#EmailId"))).send_keys("")

driver.find_element_by_css_selector("#Password").send_keys("")

WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='https://www.google.com/recaptcha/api2/anchor?']")))

WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span.recaptcha-checkbox.goog-inline-block.recaptcha-checkbox-unchecked.rc-anchor-checkbox"))).click()


time.sleep(120)

driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[4]/div/form/div[4]/input').click()
# part 1------------------------------------------------------------------------------------------------------------------------------------------------                                              
                              
Appointment=driver.find_element_by_xpath('//*[@id="Accordion1"]/div/div[2]/div/ul/li[1]/a')#حجز موعد 
driver.execute_script("arguments[0].click();", Appointment)
    
                               
LocationId=driver.find_element_by_id('LocationId')#تحديد مركز الطلبات 
LocationId.send_keys('Nagoya')

VisaCategoryId=driver.find_element_by_id('VisaCategoryId')#تحديد مركز الطلبات 
VisaCategoryId.send_keys('All ')




btnContinue=driver.find_element_by_id('btnContinue')#btnContinue
btnContinue.send_keys('All ')

       
# part 1------------------------------------------------------------------------------------------------------------------------------------------------



AddCOSTM=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[2]/a')#AddCOSTM
driver.execute_script("arguments[0].click();", AddCOSTM)


PassportNumber=driver.find_element_by_id('PassportNumber')#PassportNumber
PassportNumber.send_keys('02566668 ')


DateOfBirth=driver.find_element_by_id('DateOfBirth')#DateOfBirth 
DateOfBirth.send_keys('22/10/1989 ')


PassportExpiryDate=driver.find_element_by_id('PassportExpiryDate')#تحديد مركز الطلبات 
PassportExpiryDate.send_keys('22/11/2020 ')

NationalityId=driver.find_element_by_id('NationalityId')#تحديد مركز الطلبات 
NationalityId.send_keys('ALGERIA ')


GenderId=driver.find_element_by_id('GenderId')#تحديد مركز الطلبات 
GenderId.send_keys('Male ')

driver.find_element_by_id("submitbuttonId").click()

alert = driver.switch_to_alert()# accept la Appointment  
alert.accept()

# part 1------------------------------------------------------------------------------------------------------------------------------------------------


 
Continue=driver.find_element_by_xpath('/html/body/div[2]/div[1]/div[3]/div[3]/form/div[2]/input')#AddCOSTM
driver.execute_script("arguments[0].click();", Continue)

# part 1------------------------------------------------------------------------------------------------------------------------------------------------
appointment_made = False
while (not appointment_made):
    try:
        driver.find_element_by_xpath('//*[@id="app_date"]').click()  # this makes the datepicker appear
        all_appointments = driver.find_elements_by_xpath('/html/body/div[2]/div[1]/div[3]/div[3]/form/table/tbody/tr/td[1]/div/div/div/table/tbody/tr[2]/td[5]/div/div[1]')
        # print(all_appointments)
        if len(all_appointments) != 0:
            all_appointments[0].click()
            appointment_made = True

    except:
        print("Exception occured...")


selectedTimeBand=driver.find_element_by_id('selectedTimeBand')
selectedTimeBand.send_keys('9:30-10:00 ')


driver.find_element_by_id("btnConfirm").click()


alert = driver.switch_to_alert()# accept la Appointment  
alert.accept()
