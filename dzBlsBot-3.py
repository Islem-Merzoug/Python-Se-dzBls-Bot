from selenium import webdriver
import time
import os

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

from pynput.keyboard import Key, Controller
import traceback

keyboard = Controller()

driver = webdriver.Chrome()

if __name__ == "__main__":
     
# reading a text file containing all the info we want to pass to the application, then passing that info
     file = open("C:/Users/zakaria/Desktop/member.txt", "r")
     lines = file.readlines()
     print(lines)
     driver.get("https://tunisia.blsspainvisa.com/book_appointment.php")
     centre=driver.find_element_by_name('centre')
     centre.send_keys('Tunis')

     email=driver.find_element_by_name('email')
     email.send_keys('5553cd4f71@emailtown.club')



     phone=driver.find_element_by_name('phone')
     phone.send_keys(lines[0])


     category=driver.find_element_by_id('category')
     category.send_keys('Normal')
           

     
            
     
    #after that, retrieving the verification code sent to that address
     current_window = driver.current_window_handle
     driver.execute_script("window.open('https://www.pushbullet.com/')")
     
     WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
     new_window = [window for window in driver.window_handles if window != current_window][0]  # Get new tab ID
     driver.switch_to.window(new_window)  # Switch to new tab
        
     
     sign=driver.find_element_by_xpath('//*[@id="sign-in-btn"]')
     sign.click()
     
     google=driver.find_element_by_xpath('//*[@id="onecup"]/div/div[2]/button[1]/img')
     google.click()

     email=driver.find_element_by_name('identifier')
     email.send_keys('zaki.kaka99@gmail.com')

     suive=driver.find_element_by_xpath('//*[@id="identifierNext"]/span/span') 
     suive.click()
     
     time.sleep(7)

     passs=driver.find_element_by_name('password')
     passs.send_keys('************')
     
     suive=driver.find_element_by_xpath('//*[@id="passwordNext"]/span/span')
     suive.click()

     time.sleep(7)

     allsms=driver.find_element_by_xpath('//*[@id="sink"]/div[3]/div/div[1]/div[5]/img')
     allsms.click()

     time.sleep(3)
     
     sms=driver.find_element_by_xpath('//*[@id="sidebar"]/div[28]/div[1]')
     sms.click()
     
     time.sleep(3)

     ver_code = driver.find_element_by_xpath('//*[@id="innerlist"]/div[2]/div[2]/div/div[2]/div').text[24:-24]
     print(ver_code)

     driver.switch_to.window(current_window)
     driver.find_element_by_id('otp').send_keys(ver_code)     
        

     save=driver.find_element_by_name('save')
     save.click()
     
     
     time.sleep(3)
     
     agree = driver.find_element_by_name("agree")
     driver.execute_script("arguments[0].click();", agree)


appointment_made = False
while(not appointment_made):
        try:
            driver.find_element_by_xpath('//*[@id="app_date"]').click()             #this makes the datepicker appear
            all_appointments = driver.find_elements_by_xpath('//*[@title="Book"]')
            #print(all_appointments)
            if len(all_appointments) != 0:
                all_appointments[0].click()
                appointment_made = True
 
            
            
            time=driver.find_element_by_xpath('//*[@id="app_time"]/option[2]')
            time.click()

            typeh=driver.find_element_by_xpath('//*[@id="VisaTypeId"]/option[2]')
            typeh.click()
            
            first_name=driver.find_element_by_name('first_name')
            first_name.send_keys('fggg')
            
            last_name=driver.find_element_by_name('last_name')
            last_name.send_keys('juytg')

            driver.execute_script("document.getElementById('dateOfBirth').value='1985-12-16'")
            
            passport_no=driver.find_element_by_name('passport_no')
            passport_no.send_keys('1471478')

            driver.execute_script("document.getElementById('pptIssueDate').value='2016-06-10'")       #sets the Passport Issue Date
            driver.execute_script("document.getElementById('pptExpiryDate').value='2026-06-10'")

            pptIssuePalace=driver.find_element_by_name('pptIssuePalace')
            pptIssuePalace.send_keys('oran')

           
            
            save = driver.find_element_by_name("save")
            driver.execute_script("arguments[0].click();", save)
          
            alert = driver.switch_to_alert()
            alert.accept()
            
            
            
           # time.sleep(120)
            
           # driver.find_element_by_xpath('/html/body/div[1]/section[1]/div/div/div[1]/div[2]/a/div').click()   
            
            
        except:
            pass
            print ("we are beeing redirectedddd -----> ip is blocked")
            print ("starting with next available IP")
            
            

            
            
