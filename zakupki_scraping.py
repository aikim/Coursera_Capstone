
"""
Закупки ДЗО ПАО "Россети"

Data Source: http://www.zakupki.gov.ru/epz/main/public/home.html
Terms and short list:
    customer_id - регистрационный номер заказчика;
    customer_name - полное наименование заказчика;
    contract_id - номер договора 223ФЗ;
    subject - предмет договора;
    contract_value - стоимость контракта;
    currency - валюта;
    start - дата начала проекта;
    end - дата окончания проекта.    
    
@author: Anastasiia Kim

"""

#%% Setting the environment

import pandas as pd
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from bs4 import BeautifulSoup
import time


#%% 

def reading(spisok, contract, subject):    
    try:
        if len(contract) == 0:
            pass
        elif len(contract[-2]) == 8:
            d = {'customer_id': contract[-2].loc[0,1], 'customer_name': contract[-2].loc[1,1], 'contract_id': contract[1].loc[0,1], \
     'subject': contract[1].loc[3,1], 'contract_value': subject[1].loc[0,1], \
     'currency': subject[1].loc[1,1], 'start': subject[1].loc[2,1], 'end': subject[1].loc[4,1]} #Create a dictionary with values
            spisok.append(d)
        elif len(contract[-2]) != 8 and len(contract[-3]) == 8:
            d = {'customer_id': contract[-3].loc[0,1], 'customer_name': contract[-3].loc[1,1], 'contract_id': contract[1].loc[0,1], \
     'subject': contract[1].loc[3,1], 'contract_value': subject[1].loc[0,1], \
     'currency': subject[1].loc[1,1], 'start': subject[1].loc[2,1], 'end': subject[1].loc[4,1]}
            spisok.append(d)
    except IndexError:
       pass
       
#%% 
        
def structuring(href):
    try:
        href.click()
        driver.switch_to_window(driver.window_handles[1]) #Focus on the second tab
        soup = BeautifulSoup(driver.page_source, 'lxml')
        time.sleep(1)
        try:
            time.sleep(1)
            table = soup.find_all('table')         
        except NoSuchElementException:
            pass
        contract = pd.read_html(str(table))
        driver.find_element_by_xpath("//span[text()='Информация о предмете договора']").click() #Shift to the Second Tab
        driver.implicitly_wait(1) 
        driver.switch_to_window(driver.window_handles[1])
        soup = BeautifulSoup(driver.page_source, 'lxml')
        time.sleep(1)
        try:
            time.sleep(1)
            table = soup.find_all('table')
        except NoSuchElementException:
            pass
        subject = pd.read_html(str(table))
        reading(spisok, contract, subject)
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
    except NoSuchElementException:
        pass
    
#%%    
def scraping(id, companies):
    search = driver.find_element_by_xpath('//*[@id="searchString"]')
    search.send_keys(id)
    search.submit()
    driver.implicitly_wait(1)
    find = driver.find_element_by_xpath('//*[@id="quickSearchForm_header"]/div[1]/div/div/input[2]')
    find.click()
    driver.implicitly_wait(1)
    i = 1
    while True:
        i = i + 1
        for href in driver.find_elements_by_partial_link_text(str(5) + id):
            structuring(href) 
    
        try:
            driver.find_element_by_link_text(str(i)).click() #next page
            driver.implicitly_wait(1)
        except NoSuchElementException:
            break
    clear = driver.find_element_by_xpath('//*[@id="quickSearchForm_header"]/div[1]/div/div/div')
    clear.click()
    driver.implicitly_wait(1)
    
    
#%% Open the driver

driver = webdriver.Chrome(executable_path = 'C:/Users/akim/Downloads/chromedriver.exe')
driver.get('http://www.zakupki.gov.ru/epz/main/public/home.html')
driver.maximize_window()
driver.implicitly_wait(5)
wait = WebDriverWait(driver, 10)

#%% Выбрать "Контракты и договоры"
contracts_and_agreements = wait.until(ec.element_to_be_clickable((By.XPATH, "//a[text()='Контракты и договоры']")))
contracts_and_agreements.click()

#%% Выбрать "Реестр договоров"

reestr = wait.until(ec.element_to_be_clickable((By.XPATH, "//span[text()='Реестр договоров']")))
reestr.click()

#%% Уточнить параметры поиска
parameters = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="setParametersLink"]/a')))
parameters.click()

#%% Выбрать "Статус договора"

status = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="statusesTag"]/div/div[1]/span[1]')))
status.click()

#%% Выбрать "Исполнение завершено"

finished = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="statusesTag"]/div/div[2]/div[1]/ul/li[2]/span/label')))
finished.click()

#%% Кнопка "Выбрать"
press = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="statusesSelectBtn"]/span')))
press.click()

#%% Ввести начальную точку диапазона дат размещения контракта
datefrom = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="contract223DateFrom"]')))
datefrom.clear()
datefrom.send_keys("01-09-2018")

#%% Ввести конечную точку диапазона дат размещения контракта
todate = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="contract223DateTo"]')))
todate.clear()
todate.send_keys("30-09-2018")

#%% Кнопка "Уточнить поиск"

specify_search = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="searchButtonsBlock"]/div/span[2]')))
specify_search.click()

#%% Кнопка "Показывать по"
show = wait.until(ec.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div[1]/ul[1]/li[2]/span')))
show.click()

#%% Вывести по 50 договоров на страницу
fifty = wait.until(ec.element_to_be_clickable((By.XPATH, '//*[@id="_50"]')))
fifty.click()

#%% 

companies = ['3903007130', '0541031172', '0711008455', '0814166090', \
             '1701040660', '2016081143', '2309001660', '2460069527', \
             '2632082033', '5036065113', '5260200603', '6164266561', \
             '6450925977', '6671163413', '7017114672', '7802312751', \
             '7803002209', '8602060185']

spisok = []

#%% 

for id in companies:
    scraping(id, companies)
    
#%% Close driver
    
driver.quit()

#%% Delete dublicates

zakupki = pd.DataFrame(spisok)
  
#%% Save

writer = pd.ExcelWriter(r'C:/Users/akim/Downloads/ZAKUPKI/zakupki_092018.xlsx')
zakupki.to_excel(writer,'052017')
writer.save()

#%% 

folder = r'Z:\Электроэнергетика\РОССЕТИ\ПОЛИГОНЫ\working\zakupki.gov'
files = os.listdir(folder)

#%% 


t = []     
   xls = pd.ExcelFile(folder + '/' + f)
    df = xls.parse(i)
    df.drop([0, 1], inplace = True)
    df['date'] = [f[:8]]*len(df.index)
    df['hour'] = i
    df['datetime'] = pd.to_datetime(df.date) + df.hour.astype('timedelta64[h]')
    df.drop(df.columns[[1, 3, 5, 6, 7]], axis = 1, inplace = True)
    df.columns = ['node_id', 'unom', 'price', 'datetime']
    t.append(df)