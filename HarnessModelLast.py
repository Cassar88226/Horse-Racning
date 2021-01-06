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
from dateutil.relativedelta import relativedelta


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



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'}

#conn.close()
sleep(0.5)



base_url = "http://www.harness.org.au/racing/results/?firstDate="
base1_url = "http://www.harness.org.au"
try:
    page1 = requests.get('http://www.harness.org.au/racing/results/?firstDate=', headers=headers)
except requests.exceptions.ConnectionError:
    r.status_code = "Connection refused"
#webpage_response = requests.get('http://www.harness.org.au/racing/results/?firstDate=')

soup = bs(page1.content, "html.parser")

soup123 = requests.session()

format = "%d-%m-%y"
delta = timedelta(days=1)
#yesterday = datetime.today() - timedelta(days=1)

enddate = datetime(2020, 10, 31)
startdate = datetime(2020, 12, 27)
#prints header in csv
#writer.writerow(['Date1', 'Venue', 'RaceNumber', 'RaceName', 'RaceTitle', 'RaceDistance', 'Place', 'HorseName', 'Prizemoney', 'Row', 'Trainer', 'Driver', 'Margin', 'StartingOdds', 'StewardsComments', 'Scratching', 'TrackRating', 'Gross_Time', 'Mile_Rate', 'Lead_Time', 'First_Quarter', 'Second_Quarter', 'Third_Quarter', 'Fourth_Quarter'])


while enddate < startdate:
    enddate += timedelta(days=1)

    enddate1 = enddate.strftime("%d-%m-%Y")
    enddate2 = enddate.strftime("%Y-%m-%d")
    new_url = base_url + str(enddate1)
    # soup123 = requests.sessions()
    soup12 = soup123.get(new_url, headers=headers)

    soup1 = bs(soup12.content, "html.parser") 
    table1 = soup1.find('table', class_='meetingListFull')

    tr = table1.find_all('tr', {'class':['odd', 'even']})

    
   # sql1 = "SET DATEFORMAT dmy;"
   # mycursor.execute(sql1)
   # conn.commit()
    

    for tr1 in tr:
        tr2 = tr1.find('a').get_text()
        tr3 = tr1.find('a')['href']

        newurl = base1_url + tr3
        with requests.Session() as s:
            webpage_response = s.get(newurl, headers=headers)
            soup = bs(webpage_response.content, "html.parser")
            #soup1 = soup.select('.content')
            results = soup.find_all('div', {'class':'forPrint'})
            resultsv2 = soup.find_all('table', {'class':'raceFieldTable'})
            
               
            #writer.writerow(['Date1', 'Venue', 'RaceNumber', 'RaceTitle', 'RaceDistance', 'Place', 'HorseName', 'Prizemoney', 'Row1', 'HorseNumber', 'Trainer', 'Driver', 'Margin', 'StartingOdds', 'StewardsComments', 'Scratching', 'TrackRating', 'Gross_Time', 'Mile_Rate', 'Lead_Time', 'First_Quarter', 'Second_Quarter', 'Third_Quarter', 'Fourth_Quarter'])
        
            for race in results:

                race_number = race.find('td', class_='raceNumber').get_text()
            
                

                race_name1 = race.find('td', class_='raceTitle').get_text()
                
                race_title1 = race.find('td', class_='raceInformation').get_text()
                race_title1 = ' '.join(race_title1.split())
                
                race_distance1 = race.find('td', class_='distance').get_text()
                race_distance1 = race_distance1.replace('M', '')
                race_distance1 = float(race_distance1)

                tableoftimes = race.find('table', class_='raceTimes')
                tableofrunners = race.find('table', class_='raceFieldTable resultTable')
                
                trackrating = ''
                grosstime = ''
                milerate = ''
                leadtime = ''
                firstquarter = ''
                secondquarter = ''
                thirdquarter = ''
                fourthquarter = ''                
                
                if tableoftimes and tableofrunners:
                    for row in tableoftimes.select('td>strong:contains(":")'):
            #            for t in row: 
                        if "Track Rating:" in row.contents[0]:
                            trackrating = row.nextSibling.strip()     
                        elif "Gross Time:" in row.contents[0]:
                            grosstime = row.nextSibling.strip()
                        elif "Mile Rate:" in row.contents[0]:
                            milerate = row.nextSibling.strip()
                        elif "Lead Time:" in row.contents[0]:
                            leadtime = row.nextSibling.strip()
                        elif "First Quarter:" in row.contents[0] and row.nextSibling:
                            firstquarter = row.nextSibling.strip()
                        elif "Second Quarter:" in row.contents[0] and row.nextSibling:
                            secondquarter = row.nextSibling.strip()
                        elif "Third Quarter:" in row.contents[0] and row.nextSibling:
                            thirdquarter = row.nextSibling.strip()
                        elif "Fourth Quarter:" in row.contents[0] and row.nextSibling:
                            fourthquarter = row.nextSibling.strip()
                        if grosstime == '::' or grosstime == 'NTT':
                            grosstime = None
                        elif milerate == 'NTT' or milerate == '0::0' or milerate == '::':
                            milerate = None
                        elif milerate == 'NTT':
                            milerate = None
                        elif leadtime == 'NTT':
                            leadtime = None
                        elif firstquarter == 'NTT':
                            firstquarter = None
                        elif secondquarter == 'NTT':
                            secondquarter = None
                        elif thirdquarter == 'NTT':
                            thirdquarter = None
                        elif fourthquarter == 'NTT':
                            fourthquarter = None
                        
                        gt = ''
                        mr = ''
                        lt = ''
                        fq = ''
                        sq = ''
                        tq = ''
                        frq = ''

                        #print("Before: ", grosstime, milerate, leadtime, firstquarter, secondquarter, thirdquarter, fourthquarter)

                        if(grosstime == '0'):
                            gt = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:
                            if(grosstime != '' and grosstime != '0' and type(grosstime) != type(None)):
                                grosstime = grosstime.replace('.', ':')
                                # d = grosstime.split(':')
                                gt = datetime.strptime(grosstime, '%M:%S:%f').time()
                                # if(len(d) > 1):
                                #     s1 = d[0]
                                #     s2 = d[1]
                                #     sec = timedelta(seconds=int(s1))
                                #     sec = str(sec) + ":" + s2 
                                #     gt = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                # else:
                                #     s2 = d[0]
                                #     sec = timedelta(seconds=int(s2))
                                #     sec = str(sec)
                                #     gt = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                gt = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                    
                        if(milerate == '0'):
                            mr = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:
                            if(milerate != '' and milerate != '0' and type(milerate) != type(None)):
                                milerate = milerate.replace('.', ':')
                                mr = datetime.strptime(milerate, '%M:%S:%f').time()
                                # d = milerate.split(':')
                                # if(len(d) > 1):
                                #     s1 = d[0]
                                #     s2 = d[1]
                                #     sec = timedelta(seconds=int(s1))
                                #     sec = str(sec) + ":" + s2 
                                #     mr = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                # else:
                                #     s2 = d[0]
                                #     sec = timedelta(seconds=int(s2))
                                #     sec = str(sec)
                                #     mr = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                mr = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()

                        if(leadtime == '0'):
                            lt = lt.replace('-', '')
                            lt = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:

                            if(leadtime != '' and leadtime != '0' and type(leadtime) != type(None)):
                                leadtime = leadtime.replace('.', ':').replace('-', '')
                                d = leadtime.split(':')
                                if(len(d) > 1):
                                    s1 = d[0]
                                    s2 = d[1]
                                    sec = timedelta(seconds=int(s1))
                                    sec = str(sec) + ":" + s2 
                                    lt = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                else:
                                    s2 = d[0]
                                    sec = timedelta(seconds=int(s2))
                                    sec = str(sec)
                                    lt = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                lt = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()

                        if(firstquarter == '0'):
                            fq = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:
                            if(firstquarter != '' and firstquarter != '0' and type(firstquarter) != type(None)):
                                firstquarter = firstquarter.replace('.', ':')
                                d = firstquarter.split(":")
                                if(len(d) > 1):
                                    s1 = d[0]
                                    s2 = d[1]
                                    sec = timedelta(seconds=int(s1))
                                    sec = str(sec) + ":" + s2 
                                    fq = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                else:
                                    s2 = d[0]
                                    sec = timedelta(seconds=int(s2))
                                    sec = str(sec)
                                    fq = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                fq = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()

                        if(secondquarter == '0'):
                            sq = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:                    
                            if(secondquarter != '' and secondquarter != '0' and type(secondquarter) != type(None)):
                                secondquarter = secondquarter.replace('.', ':')
                                d = secondquarter.split(':')
                                if(len(d) > 1):
                                    s1 = d[0]
                                    s2 = d[1]
                                    sec = timedelta(seconds=int(s1))
                                    sec = str(sec) + ":" + s2 
                                    sq = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                else:
                                    s2 = d[0]
                                    sec = timedelta(seconds=int(s2))
                                    sec = str(sec)
                                    sq = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                sq = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                            
                        if(thirdquarter == '0'):
                            tq= datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:
                            if(thirdquarter != '' and thirdquarter != '0' and type(thirdquarter) != type(None)):
                                thirdquarter = thirdquarter.replace('.', ':')
                                d = thirdquarter.split(':')
                                if(len(d) > 1):
                                    s1 = d[0]
                                    s2 = d[1]
                                    sec = timedelta(seconds=int(s1))
                                    sec = str(sec) + ":" + s2 
                                    tq = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                else:
                                    s2 = d[0]
                                    sec = timedelta(seconds=int(s2))
                                    sec = str(sec) 
                                    tq = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                tq= datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                
                        if(fourthquarter == '0'):
                            frq = datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                        else:
                            if(fourthquarter != '' and fourthquarter != '0' and type(fourthquarter) != type(None)):
                                fourthquarter = fourthquarter.replace('.', ':')
                                d = fourthquarter.split(':')
                                if(len(d) > 1):
                                    s1 = d[0]
                                    s2 = d[1]
                                    sec = timedelta(seconds=int(s1))
                                    sec = str(sec) + ":" + s2 
                                    frq = datetime.strptime(sec, '%H:%M:%S:%f').time()
                                else:
                                    s2 = d[0]
                                    sec = timedelta(seconds=int(s2))
                                    sec = str(sec) 
                                    frq = datetime.strptime(sec, '%H:%M:%S').time()
                            else:
                                frq= datetime.strptime(str(timedelta(seconds=int("0"))), '%H:%M:%S').time()
                            
                        # print("After: ",gt, mr, lt, fq, sq, tq, frq)


                 
                    for row in tableofrunners.select("tr"):
                    
                        data = {
                            'DayCalender': [],
                            'Venue': [],
                            'RaceNumber': [],
                            'RaceName': [],
                            'RaceTitle': [],
                            'RaceDistance': [],          
                            'Place': [],
                            'HorseName': [],
                            'HorseID': [],
                            'Age': [],
                            'Colour': [],
                            'Sire': [],
                            'Sex': [],
                            'Prizemoney': [],
                            'Handicap': [],
                            'Row': [],
                            'Trainer': [],
                            'Driver': [],
                            'Margin': [],
                            'StartingOdds': [],
                            'StewardsComments': [],
                            'Scratching': [],
                            'TrackRating': [],
                            'Gross_Time': [],
                            'Mile_Rate': [],
                            'Lead_Time': [],
                            'First_Quarter': [],
                            'Second_Quarter': [],
                            'Third_Quarter': [],
                            'Fourth_Quarter': [],
                            'GateSpeed': [],
                            'Leader': [],
  
                            'Placer': [],
                            'Winner': []
                        }

                        # Skip "empty" rows
                        if row.find('td', class_='horse_number') == None:
                            continue

                        place = row.find('td', class_='horse_number').get_text()
                        place = place.replace('*', '').replace('r', '').replace('u', '').replace('f', '').replace('d', '')
                        try:
                            place = int(place, 0)
                        except:
                            place = 0

                        if place == 1:
                            winner = 1
                        else:
                            winner = 0

                        if place == 1 or place == 2 or place == 3:
                            placer = 1
                        else:
                            placer = 0

                        horsename = row.find('a', class_='horse_name_link')
                        horsename = horsename.text.replace('HorseName: ', '') if horsename else ''
                        horsename = horsename.replace(' NZ', '')



                        horse_id = row.find('a').get('href')
                        horse_id = horse_id[-6:]
             

                        horseweb = row.find('a').get('href')
                        horseurl = base1_url + horseweb
       
                        with requests.Session() as s:
                            try:
                                webpage_response = s.get(horseurl, headers=headers)
                            except requests.exceptions.ConnectionError:
                                r.status_code = "Connection refused"
                            
                            soup = bs(webpage_response.content, "html.parser")
                            horseresult = soup.find('table', {"class": ["table horseHeader"]})
                            sleep(1)

                            #table354 = horseresult
                            #foul = table354.tr.find_next_sibling()
                            #table254 = horseresult[1]
                            Age1 = horseresult.find_all('td')[1].get_text().replace('\xa0', '')
                            
                            horseage1 = datetime.strptime(Age1, '%d %B %Y')
                            horsebday = datetime(2021, 9, 1)
                            age = relativedelta(horsebday, horseage1).years
   
                            Colour = horseresult.find_all('td')[3].get_text()
                            Colour1 = Colour.split()[0]
                 
                            Sex = Colour.split()[1]
                     
                            Sire = horseresult.find_all('td')[5].get_text()
                          

                            #for tr35 in horseresult:
                                #horseage = tr35[].find_all('td')[1].get_text().replace('\xa0', '')

       
                                
                             
                                
                                #print(age)
                                #print(horseage1)
                                #Colour = tr35.find_all('td')[3].get_text()
                                #Colour1 = Colour.split()[0]
                                #Sex = Colour.split()[1]
                                #Sire = tr35.find_all('td')[5].get_text()
                                #print(Sire)

                        

                            #print(fouldate)
                            

                        prizemoney = row.find('td', class_='prizemoney')
                        prizemoney = prizemoney.text.replace('Prizemoney: ', '') if prizemoney else ''
                        prizemoney = prizemoney.replace('$', '')
                        prizemoney = prizemoney.replace(',', '')
                        if prizemoney is not '':
                            prizemoney = float(prizemoney)
                        else:
                            None

                   
                        handicap = row.find('td', class_='hcp')
                        handicap = handicap.text.replace('Handicap: ', '') if handicap else ''
                        handicap = handicap.replace('m', '')
                        handicap = handicap.replace('FT', '1').replace('\xa0', '')
                        if handicap is not '':
                            handicap = float(handicap)
                        else:
                            None

                        barrier = row.find('td', class_='barrier')
                        barrier = barrier.text.replace('Row: ', '') if barrier else ''

                        trainer = row.find('td', class_='trainer nowrap')
                        trainer = trainer.text.replace('Trainer: ', '') if trainer else ''

                        driver = row.find('td', class_='driver-short')
                        driver = driver.text.replace('Driver: ', '') if driver else ''



                        margin = row.find('td', class_='margin') 
                        margin = margin.text.replace('Margin: ', '').strip() if margin else ''
                        margin = margin.replace('SHFHD', '0.03')
                        margin = margin.replace('HFHD', '0.05')
                        margin = margin.replace('HD', '0.10')
                        margin = margin.replace('HFNK', '0.15')
                        margin = margin.replace('NK', '0.20')
                        
                        if margin is not '':
                            margin = float(margin)
                        else:
                            None
                        

                        if row.find('td', class_='starting_price') == None:
                            startingprice = 0
                        else:
                            startingprice = row.find('td', class_='starting_price')
                            startingprice = startingprice.text.replace('StartingOdds: ', '') 
                            startingprice = startingprice.replace('Â', '').replace('\xa0', '') if startingprice else '' 
                            startingprice = startingprice.replace('$', '').replace('fav', '').replace('&nbsp;&nbsp;', '')
                            try:
                                startingprice = Decimal(startingprice)
                            except:
                                startingprice = 0

                            
                
                        stewardscomments = row.find('span', class_='stewardsTooltip')
                        stewardscomments = stewardscomments.text.replace('StewardsComments: ', '') if horsename else ''
                        leader = ' L '
                        GateSpeed = 'GS'
                        if leader in stewardscomments:
                            leader = 1
                            leader = float(leader)
                        else:
                            leader = 0
                            leader = float(leader)
                        if GateSpeed in stewardscomments:
                            GateSpeed = 1
                            GateSpeed = float(GateSpeed)
                        else:
                            GateSpeed = 0
                            GateSpeed = float(GateSpeed)

                        scratchingnumber = row.find('td', class_='number')
                        scratchingnumber = scratchingnumber.text.replace('Scratching: ', '') if scratchingnumber else ''
                       

                        
                        data['DayCalender'].append(enddate2)
                        data['Venue'].append(tr2)
                        data['RaceNumber'].append(race_number)
                        data['RaceName'].append(race_name1)
                        data['RaceTitle'].append(race_title1)
                        data['RaceDistance'].append(race_distance1)
                        data['Place'].append(place)
                        data['HorseName'].append(horsename)
                        data['HorseID'].append(horse_id)
                        data['Age'].append(age)
                        data['Colour'].append(Colour1)
                        data['Sex'].append(Sex)
                        data['Sire'].append(Sire)
                        data['Prizemoney'].append(prizemoney)
                        data['Handicap'].append(handicap)
                        data['Row'].append(barrier)
                        data['Trainer'].append(trainer)
                        data['Driver'].append(driver)
                        data['Margin'].append(margin)
                        data['StartingOdds'].append(startingprice)
                        data['StewardsComments'].append(stewardscomments)
                        data['Scratching'].append(scratchingnumber)
                        data['TrackRating'].append(trackrating)
                        data['Gross_Time'].append(grosstime)
                        data['Mile_Rate'].append(milerate)
                        data['Lead_Time'].append(leadtime)
                        data['First_Quarter'].append(firstquarter)
                        data['Second_Quarter'].append(secondquarter)
                        data['Third_Quarter'].append(thirdquarter)
                        data['Fourth_Quarter'].append(fourthquarter)
                        data['GateSpeed'].append(GateSpeed)
                        data['Leader'].append(leader)
                        data['Placer'].append(placer)
                        data['Winner'].append(winner)
                        #data['jockeywin'].append(temp1_ave)
                        #data['trainerwin'].append(trainerwin)
                        #data['jockeystrikerate'].append(temp1_ave)



                        #driver1 = data['Driver'].unique()
                        #trainer1 = data['Trainer'].unique()
                        #horsed1 = data['HorseID'].unique()

                        #temp3 = data[data['HorseID'] == data['HorseID']]['DayCalender']
                        #temp3 = data['DayCalender'].values.tolist()

                        #temp1 = results[results['driver'] == results['driver']]['place']
                        #temp1 = temp1['place'].values.tolist()
                        #print(temp1)

                        #for i in range(len(horsed)):

                            #temp2 = results.loc[results.horsed == results.horsed[i]][['DayCalender']]
                            #temp2 = temp2['DayCalender'].values.tolist()
                            #print(temp2)
                            #if len(temp2) != 0:
                                #temp_int2 = map(int, temp2)
                                #days = temp_int2[-2] - temp_int2[-1]
                                #print(days)
                                #results['trainerwin'][i] = trainerwinave

 
                        #if 1 in temp1:
                            #temp += 1
                        #else:
                         #   temp2 += 1

                        #if len(temp1) != 0:
                         #   temp_int = map(int, temp1)
                         #   print(temp_int)
                         #   temp1_ave = np.mean(list(temp_int))
                         #   print(temp1_ave)

                        #for i in range(len(driver)):
                        #    temp1 = results[results.driver == results.driver[i]][['place']]
                        #    temp1 = temp1['place'].values.tolist()
                        #    print(temp1)
 
                        #    if 1 in temp1:
                        #       temp += 1
                        #    else:
                        #       temp2 += 1

                        #    if len(temp1) != 0:
                        #        temp_int = map(int, temp1)
                        #        print(temp_int)
                        #        temp1_ave = np.mean(list(temp_int))
                        #        print(temp1_ave)
                      #  for i in range(len(trainer)):

                       #     temp2 = results.loc[results.trainer == results.trainer[i]][['place']]
                       #     temp2 = temp2['place'].values.tolist()
                       #     print(temp2)
                       #     if len(temp2) != 0:
                       #         temp_int2 = map(int, temp2)
                       #         trainerwinave = np.mean(list(temp_int2))
                       #         print(trainerwinave)
                       #         results['trainerwin'][i] = trainerwinave

                      #  data['jockeywin'].append(temp1_ave)
                      #  data['trainerwin'].append(trainerwin)
                      #  data['jockeystrikerate'].append(temp1_ave)




                        #data['time'] = pd.to_datetime(data['Gross']).dt.time
                        table = pd.DataFrame(data, columns=['DayCalender','Venue','RaceNumber', 'RaceName', 'RaceTitle', 'RaceDistance', 'Place', 'HorseName', 'HorseID', 'Age', 'Colour', 'Sire', 'Sex', 'Prizemoney', 'Row', 'Trainer', 'Driver', 'Margin', 'StartingOdds', 'StewardsComments', 'Scratching','TrackRating' 'Mile_Rate', 'Lead_Time', 'First_Quarter', 'Second_Quarter', 'Third_Quarter', 'Fourth_Quarter',  'Leader', 'GateSpeed', 'Placer', 'Winner'])
                        print(table)
                        sql = "INSERT INTO horses (DayCalender, Venue, RaceNumber, RaceName, RaceTitle, RaceDistance, Place, HorseName, HorseID, Age, Colour, Sire, Sex, Prizemoney, Handicap, Row, Trainer, Driver, Margin, StartingOdds, StewardsComments, Scratching, TrackRating, Gross_Time, Mile_Rate, Lead_Time, First_Quarter, Second_Quarter, Third_Quarter, Fourth_Quarter, Leader, GateSpeed, Placer, Winner) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
                        Values = [enddate2, tr2, race_number, race_name1, race_title1, race_distance1, place, horsename, horse_id, age, Colour1, Sire, Sex, prizemoney, handicap, barrier, trainer, driver, margin, startingprice, stewardscomments, scratchingnumber, trackrating, gt, mr, lt, fq, sq, tq, frq, leader, GateSpeed, placer, winner]

                        #try:
                        mycursor.execute(sql, Values)
                        #except:
                        conn.commit()
                        print(mycursor.rowcount, "records inserted")
              



