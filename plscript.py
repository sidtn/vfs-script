import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime
from bot_data import ids, bot
from dotenv import load_dotenv

load_dotenv()
URL_LOGIN = 'https://visa.vfsglobal.com/blr/ru/pol/login'
login = os.getenv('LOGIN')
password = os.getenv('PASSWORD')

data = {
    'center_name': 'Poland Visa Application Center-Minsk',
    'category_name': 'D-visa Karta Polaka',
    'subcategory_name': 'D-Karta Polaka',
    # 'delay_min': 5
}


async def login_pl(delay_sec):
    center = data.get('center_name')
    category = data.get('category_name')
    subcategory = data.get('subcategory_name')
    delay = delay_sec
    driver = webdriver.Chrome()
    try:
        driver.get(URL_LOGIN)
        time.sleep(4)
        try:
            driver.find_element(By.XPATH, '//*[@id="onetrust-accept-btn-handler"]').click()
        except Exception:
            pass
        email_field = driver.find_element(By.XPATH, '//*[@id="mat-input-0"]')
        password_field = driver.find_element(By.XPATH, '//*[@id="mat-input-1"]')
        email_field.send_keys(login)
        password_field.send_keys(password)
        login_button = driver.find_element(By.XPATH, '/html/body/app-root/div/app-login/'
                                                           'section/div/div/mat-card/form/button')
        login_button.click()
        time.sleep(5)
        driver.find_element(By.XPATH, '/html/body/app-root/div/app-dashboard/section/div/div[1]/div[2]/button').click()
        time.sleep(4)
        center_dropdown = driver.find_element(By.XPATH, '//*[@id="mat-select-value-1"]')
        center_dropdown.click()
        center_sel = driver.find_element(By.XPATH,
                                            f"//*[@class='mat-option-text' and contains(text(), '{center}')]")
        driver.execute_script("arguments[0].scrollIntoView();", center_sel)
        center_sel.click()
        time.sleep(3)
        category_dropdown = driver.find_element(By.XPATH, '//*[@id="mat-select-value-3"]')
        category_dropdown.click()
        category_sel = driver.find_element(By.XPATH,
                                               f"//*[@class='mat-option-text' and contains(text(), '{category}')]")
        category_sel.click()
        time.sleep(3)
        subcategory_dropdown = driver.find_element(By.XPATH, '//*[@id="mat-select-value-5"]')
        subcategory_dropdown.click()
        subcategory_sel = driver.find_element(By.XPATH,
                                               f"//*[@class='mat-option-text' and contains(text(), '{subcategory}')]")
        subcategory_sel.click()
        time.sleep(10)
        button = driver.find_element(By.XPATH, '/html/body/app-root/div/app-eligibility-criteria/section'
                                                     '/form/mat-card[2]/button')
        driver.execute_script("arguments[0].scrollIntoView();", button)
        if button.get_attribute('disabled') == 'true':
            mess = f'[PL] Дат нету, следующая попытка через {delay} секунд - {datetime.now().strftime("%H:%M:%S")}'
            print(mess)
            for id in ids:
                await bot.send_message(id, mess)
            driver.quit()
            time.sleep(delay)
            await login_pl(delay)
        else:
            button.click()
            mess = '[PL] ЕСТЬ ДАТА, БЕГОМ К КОМПУ!!!'
            for id in ids:
                await bot.send_message(id, mess)

    except Exception:
        mess = '[PL] IP забанен, перезагрузи модем'
        print(mess)
        for id in ids:
            await bot.send_message(id, mess)
        driver.quit()


