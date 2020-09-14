# -*- coding: utf-8 -*-
"""
Created on Sun Nov 24 18:57:44 2019

@author: gupta
"""
#importing all relevant packages
import dateparser as dp
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep

#opening webpage in chrome
driver = Chrome('C:/Users/gupta/Downloads/chromedriver')
url = "https://www.espn.in/f1/schedule"
driver.get(url)

""" defining lists of data required """
dates = []
circuits = []
lenghts = []
distances = []
lap_records = []
lap_record_holder = []
qual_pos = []

cols = ["race position", "names","teams", "race times" ,"laps", "pitstops"]

wait = WDW(driver, 15)#defining the WebDriverWait to enable explicit waits

"""
explicit waits are needed to make sure that the program waits until the element required has loaded
this is to prevent errors such as NoSuchElement or ElementClickInterceptedException
""" 

count = 1

for i in range(0,21): #21 since there are 21 races in a season
    #the data with the race schedule is arranged in a table
    table = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[3]/div[1]/div/section/div/section/div/div/div[2]/table/tbody''')
    
    #gets the circuit name
    circuit = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[3]/div[1]/div/section/div/section/div/div/div[2]/table/tbody/tr[{}]/td[2]/div'''.format(i+1))
    file = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[3]/div[1]/div/section/div/section/div/div/div[2]/table/tbody/tr[{}]/td[2]/a'''.format(i+1))
    file_name = file.text
    circuits.append(circuit.text)
    
    """
    each race data is in an individual row
    the 2 lines below find each individual row and clicks on them to get further details
    """
    race = table.find_elements_by_tag_name("tr")
    race[i].find_element_by_tag_name("a").click()

    #to get the date on which the race was held and converting it to a datetime object using dateparser.parse
    date1 = dp.parse(driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/div[1]/div/div/div[1]/div/div[2]''').text.split('-')[1][1:]).date()
    dates.append(date1)
    
    driver.implicitly_wait(10)
    
    #clicks the circuits button
    WDW(driver,10).until(
                    EC.element_to_be_clickable((By.XPATH, '''//*[@id="fittPageContainer"]/div[2]/div/nav/ul/li[3]/a'''))
                    )
    driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/nav/ul/li[3]/a''').click()

    """
    the 4 wait lines below wait unitl the data has loaded to stop errors
    """
    
    wait.until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[3]/ul[1]/li[2]/span[2]'''))
            )
    wait.until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[3]/ul[1]/li[3]/span[2]'''))
            )
    wait.until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[2]/div[2]/div[2]/div[1]/span[2]'''))
            )
    wait.until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[2]/div[2]/div[2]/div[1]/span[1]'''))
            )
    """
    the 4 lines below find the element
    Note: this could have been done using
    lenght = wait.until(
            EC.presence_of_element_located((By.XPATH, '''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[3]/ul[1]/li[2]/span[2]'''))
            )
    but this was producing unexpected errors in the code such as the webpage timing out. I could not find a solution on the internet
    """
    
    lenght = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[3]/ul[1]/li[2]/span[2]''')
    distance = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[3]/ul[1]/li[3]/span[2]''')
    lap_rec = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[2]/div[2]/div[2]/div[1]/span[2]''')
    lap_rec_hold = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/section/div/div/div[2]/div[2]/div[2]/div[1]/span[1]''')
    #appends the items to the list
    lenghts.append(lenght.text)
    distances.append(distance.text)
    lap_records.append(lap_rec.text)
    lap_record_holder.append(lap_rec_hold.text)
    
    #clicks the results tab 
    driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/nav/ul/li[4]/a''').click()
    driver.implicitly_wait(10)
    
    #the results are arranged in a table with each row containing details of 1 driver
    result_table = driver.find_element_by_xpath('''//*[@id="fittPageContainer"]/div[2]/div/div[5]/div/div/div[1]/section/div/section/div/div/div[2]/table/tbody''')
    results = result_table.find_elements_by_tag_name("tr")#selects each driver
    
    dic = {x:[] for x in cols} #making dictionary with empty lists so that it can be converted to dataframe later
    for g in range(20):#20 since there are 20 drivers each race
        data = results[g].find_elements_by_tag_name("td")
        for i in range(6):
            dic[cols[i]].append(data[i].text)#this forms the dictionary
            
    #creates dataframe for each race and outputs a csv file identified by race number
    df1 = pd.DataFrame(dic)
    df1.to_csv("race_"+str(file_name)+".csv", index = False)
    driver.get(url)
    count += 1
 
#creates dataframe of circuit information 
df = pd.DataFrame(columns = ["Date Held", "Circuit"," Race Distance","Lap Record Holder",'Lap Record', 'Circuit Lenght'])
df["Date Held"] = dates
df["Circuit"] = circuits
df["Race Distance1"] = distances
df["Lap Record Holder"] = lap_record_holder
df["Lap Record"]= lap_records
df["Circuit Lenght"] = lenghts

#error where Race Distance was duplicated with one being empty so dropping empty column
df = df.drop(df.columns[2],axis = 1)#if Race Distance column does not show then delete this
#output to csv
df.to_csv("circuits.csv", index = False)

sleep(1)
driver.quit()