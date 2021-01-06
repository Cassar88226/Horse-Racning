from datetime import datetime, date, timedelta
import requests
import re
import csv
import os
import numpy
import pandas as pd
from bs4 import BeautifulSoup as bs
from simplified_scrapy import SimplifiedDoc,req,utils
import pypyodbc
from time import sleep
import time
import schedule
from decimal import Decimal 
import tensorflow as tf
from tensorflow import keras

#Write to CSV File
#file = open('harnessresults.csv', 'w', newline='', encoding='utf8')
#writer = csv.writer(file)

#Connect to SQL database
conn = pypyodbc.connect("Driver={SQL Server};"
                     "Server=DESKTOP-KOOIS0J;"
                     "Database=Horses;"
                     "Trusted_Connection=yes;",
                     autocommit=True
                )


mycursor = conn.cursor()



headers = {'User-Agent': 'Mozilla/5.0'}

#conn.close()
sleep(1)



base_url = "http://www.harness.org.au/racing/fields"
base1_url = "http://www.harness.org.au/"
try:
    page1 = requests.get('http://www.harness.org.au/racing/fields', headers=headers)
except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"
#webpage_response = requests.get('http://www.harness.org.au/racing/fields')

soup = bs(page1.content, "html.parser")
soup123 = requests.session()
format = "%d-%m-%y"
delta = timedelta(days=1)
tomorrow = datetime.today() + timedelta(days=1)
tomorrow1 = tomorrow.strftime("%d%m%y")
print(tomorrow1)
enddate = date.today()

future = date.today() + timedelta(days=3)
#startdate = datetime(2017, 1, 1)
#prints header in csv
#writer.writerow(['Date1', 'Venue', 'RaceNumber', 'RaceName', 'RaceTitle', 'RaceDistance', 'Place', 'HorseName', 'Prizemoney', 'Row', 'Trainer', 'Driver', 'Margin', 'StartingOdds', 'StewardsComments', 'Scratching', 'TrackRating', 'Gross_Time', 'Mile_Rate', 'Lead_Time', 'First_Quarter', 'Second_Quarter', 'Third_Quarter', 'Fourth_Quarter'])
n = 1

while n > 0:
    enddate += timedelta(days=1)
    enddate1 = enddate.strftime("%d-%m-%Y")
    #enddate2 = enddate.strftime("%Y-%m-%d")
    #new_url = base_url
    # soup123 = requests.sessions()
    soup12 = soup123.get(base_url, headers=headers)
    print(soup12)
    soup1 = bs(soup12.text, "html.parser") 
    table1 = soup1.find('table', class_='meetingList')
    print(table1)
    tr = table1.find_all('tr', {'class':['odd', 'even']})
    print(tr)
    sleep(1)
    
   # sql1 = "SET DATEFORMAT dmy;"
   # mycursor.execute(sql1)
   # conn.commit()
    

    for tr1 in tr:
        tr5 = tr1.find('a').get_text()
        tr2 = tr1.find('a')['href']
        print(tr5)
        print(tr1)
        print(tr2)
        tr3 = tr2[-6:]
        #tr3 = tr3 + "20"
        #tr4 = datetime.strptime(tr3, '%d%m%y')
        #print(tr4)
        #tr2 = tr1.find('a')['href']
        #print(tr2)
        newurl = base1_url + tr2
        print(newurl)
        with requests.Session() as s:
            webpage_response = s.get(newurl, headers=headers)
            soup = bs(webpage_response.content, "html.parser")
            #soup1 = soup.select('.content')
            results = soup.find_all('div', {'class':'forPrint'})
            resultsv2 = soup.find_all('table', {'class':'raceFieldTable'})

            for race in results:

                race_number = race.find('td', class_='raceNumber').get_text()
            
                

                race_name1 = race.find('td', class_='raceTitle').get_text()
                
                race_title1 = race.find('td', class_='raceInformation').get_text()
                race_title1 = ' '.join(race_title1.split())
                
                race_distance1 = race.find('td', class_='distance').get_text()
                race_distance1 = race_distance1.replace('M', '')
                race_distance1 = float(race_distance1)

                #tableoftimes = race.find('table', class_='raceTimes')
                tableofrunners = race.find('table', class_='raceFieldTable')


                #if tableofrunners:
                #if 'Pl' not in tableofrunners.find('th', class_='horse_number'):
                   # continue
                
                if tableofrunners is not None:
      
                    for row in tableofrunners.select("tr"):
                    
                        data = {

                            'Venue': [],
                            'RaceNumber': [],
                            'RaceName': [],
                            'RaceTitle': [],
                            'RaceDistance': [],          
                            'HorseNumber': [],
                            'HorseName': [],
                            'Handicap': [],
                            'Row': [],
                            'Trainer': [],
                            'Driver': [],
                            'StartingOdds': [],
                            'HorseClass': [],
                            'HorseID': [],
                            'Form': [],
                            'spelllastfive': [],
                            'firstup': [],
                            'Firststarter': []
                        }

                        # Skip "empty" rows
                        if row.find('td', class_='horse_number') == None:
                            continue
                        result = tableofrunners.find('th', class_='horse_number')
                        result = result.text.replace('horse_number: ', '').replace('\xa0', '')
                        if 'Pl' in result:
                            continue
                      
                        trainer = row.find('td', class_='trainer')
                        print(trainer)
                        trainer = trainer.text.replace('Trainer: ', '') if trainer else ''

                        driver = row.find('td', class_='driver-short')
                        driver = driver.text.replace('Driver: ', '') if driver else ''

                     

                        if "SCRATCHED" in driver:
                            continue

                        horse_number = row.find('td', class_='horse_number')
                        
                        horse_number = horse_number.text.replace('Form: ', '') if horse_number else ''

                       
                       
                        form = row.find('td', class_='form')
                        form = form.text.replace('Form: ', '') 


                        if 's' in form:
                            spelllastfive = 1
                        else:
                            spelllastfive = 0

                        if form.endswith('s'):
                            firstup = 1
                        else:
                            firstup = 0

                        if form == '':
                            form = 0
                        else:
                            form = form.replace('*', '').replace('r', '0').replace('u', '0').replace('f', '0').replace('d', '0').replace('s', '').replace('n', '').replace('b', '')

                        if form == 0:
                            firststarter = 1
                        else:
                            firststarter = 0


                        #if form[:] == 's':
                         #   spelllastfive = 1
                        #elif form[:] == 'b':
                         #   spelllastfive = 1
                        #else:
                           # spelllastfive = 0

                        #if form[-1] == 's':
                         #   firstup = 1
                        #elif form[:] == 'b':
                         #   firstup = 1
                        #else:
                         #   firstup = 0
                        #else:
                         #   firststarter = 0
                        
                        
                        
                        #form = form.replace('*', '').replace('r', '0').replace('u', '0').replace('f', '0').replace('d', '0').replace('s', '').replace('n', '').replace('b', '')




                        horsename = row.find('a', class_='horse_name_link')
                        horsename = horsename.text.replace('HorseName: ', '') if horsename else ''
                        horsename = horsename.replace(' NZ', '')

                        horse_id = row.find('a').get('href')
                        horse_id = horse_id[-6:]
                        print(horse_id)
                        
                        class1 = row.find('td', class_='horse_class')
                        class1 = class1.text.replace('HorseClass: ', '') 
                        class1 = class1.replace('\xa0', '') if class1 else ''
                   
                        handicap = row.find('td', class_='hcp')
                        handicap = handicap.text.replace('Handicap: ', '') if handicap else ''
                        handicap = handicap.replace('m', '')
                        handicap = handicap.replace('FT', '0').replace('\xa0', '')
                        

                        barrier = row.find('td', class_='barrier')
                        barrier = barrier.text.replace('Row: ', '') if barrier else ''

                        
                      

                        #driver = row.find('td', class_='driver-short')
                        #driver = driver.text.replace('Driver: ', '') if driver else ''

                        if row.find('td', class_='market') == None:
                            startingprice = 0
                        else:
                            startingprice = row.find('td', class_='market')
                            startingprice = startingprice.text.replace('Market: ', '') 
                            startingprice = startingprice.replace('Â', '').replace('\xa0', '') if startingprice else '' 
                            startingprice = startingprice.replace('$', '').replace('fav', '').replace('&nbsp;&nbsp;', '')
                            try:
                                startingprice = Decimal(startingprice)
                            except:
                                startingprice = 0
                        #scratchingnumber = row.find('td', class_='number')
                        #scratchingnumber = scratchingnumber.text.replace('Scratching: ', '') if scratchingnumber else ''

                        data['Venue'].append(tr5)
                        data['RaceNumber'].append(race_number)
                        data['RaceName'].append(race_name1)
                        data['RaceTitle'].append(race_title1)
                        data['RaceDistance'].append(race_distance1)
                        data['HorseName'].append(horsename)
                        data['HorseNumber'].append(horse_number)
                        #data['Prizemoney'].append(prizemoney)
                        data['Handicap'].append(handicap)
                        data['Row'].append(barrier)
                        data['Trainer'].append(trainer)
                        data['Driver'].append(driver)
                        data['StartingOdds'].append(startingprice)
                        data['HorseClass'].append(class1)
                        data['HorseID'].append(horse_id)
                        data['Form'].append(form)
                        data['spelllastfive'].append(spelllastfive)
                        data['firstup'].append(firstup)
                        data['Firststarter'].append(firststarter)

   
 

                        table = pd.DataFrame(data, columns=['Venue', 'RaceNumber', 'RaceName', 'RaceName', 'RaceDistance', 'HorseNumber', 'HorseName', 'Handicap', 'Row', 'Trainer', 'Driver', 'StartingOdds', 'HorseClass', 'spelllastfive', 'firstup', 'HorseID', 'Form', 'Firststarter'])
                        print(table)
                        sql = "INSERT INTO Field (Venue, RaceNumber, RaceName, RaceTitle, RaceDistance, HorseNumber, HorseName, Handicap, Row, Trainer, Driver, StartingOdds, HorseClass, HorseID, Form, spelllastfive, firstup, Firststarter) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

                        Values = [tr5, race_number, race_name1, race_title1, race_distance1, horse_number, horsename, handicap, barrier, trainer, driver, startingprice, class1, horse_id, form, spelllastfive, firstup, firststarter]
                        
                        mycursor.execute(sql, Values)
                        #except:
                        conn.commit()

                        print(mycursor.rowcount, "records inserted")

                        n -= 1