from datetime import datetime, date, timedelta
import calendar
import requests
import re
import csv
import os
import numpy
import pandas as pd
from bs4 import BeautifulSoup as bs
import pypyodbc
from time import sleep
import time
import schedule
from decimal import Decimal 

def schedule_func():
    
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

    soup123 = requests.session()

    # get tomorrow field
    tomorrow = datetime.today() + timedelta(days=1)

    raceday = tomorrow.strftime("%Y-%m-%d")
    nextdate = tomorrow + timedelta(days=1)
    
    day = tomorrow.day
    month_name = calendar.month_name[tomorrow.month]
    week_name = calendar.day_name[tomorrow.weekday()]

    full_date = " ".join([week_name, str(day), month_name])

    nextday = nextdate.day
    next_month_name = calendar.month_name[nextdate.month]
    next_week_name = calendar.day_name[nextdate.weekday()]

    next_full_date = " ".join([next_week_name, str(nextday), next_month_name])

    print(full_date)

    soup12 = soup123.get(base_url, headers=headers)
    soup1 = bs(soup12.text, "html.parser") 
    table1 = soup1.find('table', class_='meetingList')
    tr = table1.find_all('tr')
    sleep(1)

    flag = False
    for tr1 in tr:
        try:
            tr_header = tr1.find('h4').get_text()
            if tr_header == full_date:
                flag = True
                continue
            if tr_header == next_full_date:
                flag = False
                break
        except:
            pass
        if not flag:
            continue
        tr5 = tr1.find('a').get_text()
        tr2 = tr1.find('a')['href']
        print(tr5)
        print(tr1)
        print(tr2)

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

                        date['DayCalender'].append(raceday)
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




                        table = pd.DataFrame(data, columns=['DayCalender', 'Venue', 'RaceNumber', 'RaceName', 'RaceName', 'RaceDistance', 'HorseNumber', 'HorseName', 'Handicap', 'Row', 'Trainer', 'Driver', 'StartingOdds', 'HorseClass', 'spelllastfive', 'firstup', 'HorseID', 'Form', 'Firststarter'])
                        print(table)
                        sql = "INSERT INTO Field (DayCalender, Venue, RaceNumber, RaceName, RaceTitle, RaceDistance, HorseNumber, HorseName, Handicap, Row, Trainer, Driver, StartingOdds, HorseClass, HorseID, Form, spelllastfive, firstup, Firststarter) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"

                        Values = [raceday, tr5, race_number, race_name1, race_title1, race_distance1, horse_number, horsename, handicap, barrier, trainer, driver, startingprice, class1, horse_id, form, spelllastfive, firstup, firststarter]
                        
                        mycursor.execute(sql, Values)
                        conn.commit()

                        print(mycursor.rowcount, "records inserted")

schedule.schedule.every().day.at("02:00").do(schedule_func)
while True:
    schedule.run_pending()
    sleep(10)
