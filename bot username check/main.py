from selenium.webdriver.common.by import By
import undetected_chromedriver.v2 as uc
import time
import random
import telebot
from selenium.webdriver.common.keys import Keys



bot = telebot.TeleBot("5972966249:AAF-CL9BpqibF37litJsoPklcBIjX43ECpM", parse_mode=None)
with open('check.txt','r') as file:
    lines = file.readlines()

driver = uc.Chrome(use_subprocess=True)
driver.get('https://web.telegram.org/k/')
input('Зашли ли в аккаунт и группу? ')

while True:
    for item in lines:
        div = driver.find_element(By.CSS_SELECTOR,'.section.no-border')
        input_e = div.find_element(By.TAG_NAME,'input')
        for i in item.strip():
            input_e.send_keys(i)
            time.sleep(0.1)
        time.sleep(random.randint(1,3))
        # while True:
        #     if input_e.get_attribute('aria-label') == 'Checking...':
        #         pass
        #     else:
        #         break
        if input_e.get_attribute('aria-label') == 'Link is available.':
            bot.send_message('-1001896143322',f'{item.strip()} - свободен!')
            lines.remove(item)
        input_e.clear()
        # for i in item.strip():
        #     input_e.send_keys(Keys.END)
        #     time.sleep(0.25)
        #     input_e.send_keys(Keys.BACKSPACE)
        #     time.sleep(0.25)
        time.sleep(random.randint(1,3))