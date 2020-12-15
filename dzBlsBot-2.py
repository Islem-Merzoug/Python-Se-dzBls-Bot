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

IP = ["64.225.62.241:3128","12.345.678.910:8080"]

class Bot:
    def configure_driver(self, ip):
        # options = webdriver.FirefoxOptions()
        # next_server = "--proxy-server=%s" + ip
        # options.add_argument(next_server)
        # options.add_argument("--headless")

        # driver = webdriver.Firefox(firefox_options=options)
        # driver.implicitly_wait(20)
        # driver.get('https://algeria.blsspainvisa.com/appointment.php')

        firefox_options = webdriver.FirefoxOptions()
        firefox_options.add_argument('--proxy-server=%s' % ip)
        # options.add_argument("--headless")

        driver = webdriver.Firefox(firefox_options=firefox_options)
        driver.implicitly_wait(20)
        driver.get("https://tunisia.blsspainvisa.com/appointment.php")

        pageExists = []
        pageNotExists = []

        while True:
            try:
                pageExists = driver.find_element_by_id("verification_code")
            except:
                print(pageNotExists)

            if (pageExists == pageNotExists):
                print('not exists')
                driver.refresh()
            else:
                print('exists')
                break

        # reading a text file containing all the info we want to pass to the application, then passing that info
        file = open("/home/islem/dzBlsBot-2/member.txt", "r")
        lines = file.readlines()
        print(lines)

        try:
            driver.find_element_by_xpath(
                '//*[@id="IDBodyPanelapp"]/div[1]').click()  # clicks the 'X'(close) button if it appears
        except:
            print("Exception occured, pop up didn't appear")

        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'centre')))
        select = Select(driver.find_element_by_id('centre'))
        time.sleep(2)
        select.select_by_visible_text('Tunis')

        time.sleep(6)

        WebDriverWait(driver, 50).until(EC.element_to_be_clickable((By.ID, 'category')))
        categorie = Select(driver.find_element_by_id('category'))
        time.sleep(2)
        categorie.select_by_visible_text('Normal')

        # filling phone text field
        phone_code = driver.find_element_by_id("phone_code")
        phone_code.clear()
        time.sleep(2)
        phone_code.send_keys('213')
        phone = driver.find_element_by_name("phone")
        time.sleep(2)
        phone.send_keys(lines[0])
        email = driver.find_element_by_id("email")
        time.sleep(2)
        email.send_keys(lines[8])

        # getting a spare email address using 'https://temp-mail.org/' webpage and passing it to the text field
        # current_window = driver.current_window_handle
        # driver.execute_script("window.open('https://temp-mail.org')")
        # WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        # new_window = [window for window in driver.window_handles if window != current_window][0]  # Get new tab ID
        # driver.switch_to.window(new_window)  # Switch to new tab
        # time.sleep(25)
        # spare_email = driver.find_element_by_id('mail').get_attribute('value')
        # print(spare_email)
        # driver.switch_to.window(current_window)
        # driver.find_element_by_id('email').send_keys(spare_email)

        # driver.find_element_by_xpath('//*[@id="verification_code"]').click()
        # driver.switch_to.window(new_window)  # Switch to new tab
        # # time.sleep(60)
        #
        # WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.XPATH, '//html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[3]/div[1]/a/span[1]')))
        #
        # driver.find_element_by_xpath('//html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[4]/ul/li[3]/div[1]/a/span[1]').click()
        # time.sleep(2)
        #
        # ver_code = driver.find_element_by_xpath('/html/body/main/div[1]/div/div[2]/div[2]/div/div[1]/div/div[2]/div[3]/table/tbody/tr[7]/td').text[-4:]
        # print(ver_code)

        ###############################
        current_window = driver.current_window_handle
        driver.execute_script("window.open('https://www.pushbullet.com/')")
        print('2')

        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
        new_window = [window for window in driver.window_handles if window != current_window][0]  # Get new tab ID
        driver.switch_to.window(new_window)  # Switch to new tab
        print('3')

        time.sleep(10)
        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.ID, 'sign-in-btn')))


        sign = driver.find_element_by_id('sign-in-btn')
        sign.click()
        print('4')

        time.sleep(10)

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="onecup"]/div/div[2]/button[1]/img')))

        google = driver.find_element_by_xpath('//*[@id="onecup"]/div/div[2]/button[1]/img')
        google.click()
        print('5')

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.NAME, 'identifier')))

        email = driver.find_element_by_name('identifier')
        email.send_keys('i.merzoug16@gmail.com')
        print('6')

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="identifierNext"]/span/span')))

        suive = driver.find_element_by_xpath('//*[@id="identifierNext"]/span/span')
        suive.click()
        print('7')

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.NAME, 'password')))

        passs = driver.find_element_by_name('password')
        passs.send_keys('*professional@account#')
        print('8')

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="passwordNext"]/span/span')))

        suive = driver.find_element_by_xpath('//*[@id="passwordNext"]/span/span')
        suive.click()
        print('9')

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div[3]/div/div[1]/div')))

        allsms = driver.find_element_by_xpath('/html/body/div/div/div[3]/div/div[1]/div')
        allsms.click()
        print('10')

        WebDriverWait(driver, 500).until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="sink"]/div[3]/div/div[1]/div[5]')))

        sms = driver.find_element_by_xpath('//*[@id="sink"]/div[3]/div/div[1]/div[5]')
        sms.click()
        print('11')

        WebDriverWait(driver, 180).until(EC.element_to_be_clickable(
            (By.XPATH, '/html/body/div/div/div[3]/div/div[3]/div[1]/div/div/div[2]/div/div[2]/div')))
        time.sleep(10)

        # ver_code = driver.find_element_by_xpath(
        #     '/html/body/div/div/div[3]/div/div[3]/div[1]/div/div/div[2]/div/div[2]/div').text[-4:]
        # print(ver_code)

        ver_code = driver.find_element_by_xpath('//*[@id="innerlist"]/div[last ()]/div[2]/div/div[2]/div').text[-4:]
        print(ver_code)

        ###################################################

        driver.switch_to.window(current_window)
        driver.find_element_by_id('otp').send_keys(ver_code)

        driver.find_element_by_name('save').click()

        # part 2------------------------------------------------------------------
        agree = driver.find_element_by_name('agree')
        driver.execute_script("arguments[0].scrollIntoView();", agree)
        WebDriverWait(driver, 500).until(EC.element_to_be_clickable((By.NAME, 'agree')))
        # time.sleep(5)
        agree.click()

        # part 3------------------------------------------------------------------

        appointment_made = False
        while (not appointment_made):
            try:
                driver.find_element_by_xpath('//*[@id="app_date"]').click()  # this makes the datepicker appear
                all_appointments = driver.find_elements_by_xpath('//*[@title="Book"]')
                # print(all_appointments)
                if len(all_appointments) != 0:
                    all_appointments[0].click()
                    appointment_made = True

            except:
                print("Exception occured...")

        driver.find_element_by_xpath('//*[@id="app_time"]/option[2]').click()  # sets the Appointment Time
        driver.find_element_by_xpath('//*[@id="VisaTypeId"]/option[2]').click()  # sets the Visa Type

        driver.find_element_by_id('first_name').send_keys(lines[1])  # sets the first name
        driver.find_element_by_id('last_name').send_keys(lines[2])  # sets the last name
        driver.execute_script("document.getElementById('dateOfBirth').value=" + lines[3])  # sets the Date Of Birth
        driver.find_element_by_id('passport_no').send_keys(lines[4])  # sets the Passport Number
        driver.find_element_by_id('pptIssueDate').send_keys(lines[5])  # sets the Passport Issue Date
        driver.find_element_by_id('pptExpiryDate').send_keys(lines[6])  # sets the Passport Expiry Date

        # driver.execute_script(
        #     "document.getElementById('pptIssueDate').value=" + lines[5])  # sets the Passport Issue Date
        # driver.execute_script(
        #     "document.getElementById('pptExpiryDate').value=" + lines[6])  # sets the Passport Expiry Date
        driver.find_element_by_id('pptIssuePalace').send_keys(lines[7])  # sets the passport Issue Place

bot = Bot()
for ip in IP:
    bot.configure_driver(ip)
# if __name__ == '__main__':
#     bot = Bot()
#     bot.refresh(bot.driver)
#
    # time.sleep(10)
    # driver.close()

    # file = open("/home/islem/dzBlsBot/member.txt", "r")
    # content = file.readlines()
    # print(content)