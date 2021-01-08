from datetime import timedelta, date
import requests
import pandas as pd
import pypyodbc
import matplotlib.pyplot as plt


def schedule_func():
    
    # connect to sql database
    conn = pypyodbc.connect("Driver={SQL Server};"
                        "Server=DESKTOP-KOOIS0J;"
                        "Database=Horses;"
                        "Trusted_Connection=yes;",
                        autocommit=True
                    )
    mycursor = conn.cursor()

    # the 2 endpoints we'll be hitting from the hub
    racecard_url = "https://apigateway.betfair.com.au/hub/racecard"
    event_url = "https://apigateway.betfair.com.au/hub/raceevent"

    # define start date and end date to scrape - you should make sure you check your
    # database/store for what days you have already scraped so your not hitting the 
    # hub for data you already have. Its considered a bit rude ;)
    start_date = date(2020, 11, 1)
    end_date = date(2020, 12, 27)
    inc = timedelta(days=1)

    # iterate over the days
    d = start_date
    while d < end_date:
        # turn the date into a string for our url request parameter
        date_str = d.strftime("%Y-%m-%d")

        # grab the racecard data page for the data and parse the json into a python data structure
        card_page = requests.get(f"{racecard_url}?date={date_str}")
        
        card_data = card_page.json()

        # iterate over meetings and markets 
        
        for meeting in card_data["MEETINGS"]:

            if meeting["COUNTRY"] == 'AUS' and meeting["RACE_TYPE"] == 'H':

                for market in meeting["MARKETS"]:
                # if market['error'] == None:
                    #   continue
        
        
                        # get the market id
                    
                    mid = market['MARKET_ID']
                        
                    # iterate over each market id and grab the page specific to that market id
                    event_page = requests.get(f"{event_url}/1.{mid}")
                    event = event_page.json()

                    if "error" in event:
                        continue
                    venue = event['venueName']

                    racenumber = event['raceNo']

                    weather1 = event['weather']
                    if weather1 == 'O\'CAST':
                        weather1 = 2
                    elif weather1 == 'SHOWERS':
                        weather1 = 3
                    elif weather1 == 'FAST':
                        weather1 = 1
                    elif weather1 == 'GOOD':
                        weather1 = 1
                    elif weather1 == 'FINE':
                        weather1 = 1
                    elif weather1 == 'RAIN':
                        weather1 = 4
                    else:
                        weather1 = 5

                    


                        
                    trackrating = event['trackCondition']


                    productpoolsize = event['products'][0]
                    if productpoolsize['poolSizeAmount'] == None:
                        continue
                    if productpoolsize['poolSizeAmount'] < 500:
                        continue
                    poolSizeAmount = productpoolsize['poolSizeAmount']
                        
            
                    for runners in event["runners"]:
                        if "isScratched" in runners:
                            continue
                        data = {
                            'day': [],
                            'venueName': [],
                            'raceNo': [],
                            'weather': [],
                            'trackCondition': [],
                            'runnerName': [],
                            'WIN_ODDS_BSP': [],

                            'poolSizeAmountWin': [],

                                }
                        
                        horsename = runners['runnerName']
                        priceget = runners["markets"][0]
                        if "price" in priceget:
                            BSP = priceget["price"]
                        else:
                            BSP = 0
                        
                        
                    
                    #place = runners['placedResult']
                    #print(place)
                            
                        # print(len(BSP), len(horsename), len(weather1), len())
                        data['day'].append(date_str)
                        data['venueName'].append(venue)
                        data['raceNo'].append(racenumber)
                        data['weather'].append(weather1)
                        data['trackCondition'].append(trackrating)
                        data['runnerName'].append(horsename)
                        data['WIN_ODDS_BSP'].append(BSP)

                        data['poolSizeAmountWin'].append(poolSizeAmount)
                        #data['poolSizeAmountPlace'].append(poolsizeplace)
                    
                        table = pd.DataFrame(data, columns=['day','venueName','raceNo', 'weather', 'trackCondition', 'runnerName', 'WIN_ODDS_BSP', 'poolSizeAmountWin'])
                        print(table)
                        sql = "INSERT INTO Betfairdata (day, venueName, raceNo, weather, trackCondition, runnerName, WIN_ODDS_BSP, poolSizeAmountWin) VALUES (?,?,?,?,?,?,?,?)"
                        # print("Everything: ", "DayCalender: ",enddate1, "Venue: ",tr2, "RaceNo: ",race_number, "RaceName1: ",race_name1, "RaceTitle: ",race_title1, "RaceDist: ",race_distance1, "Place: ",place, "HorseName: ", horsename, "Prizemoney: ",prizemoney, "Row: ",barrier, "Trainer: ",trainer, "Driver: ",driver, "Margin: ",margin, "StartingOdds: ",startingprice, "StewardsComment: ",stewardscomments, "Scratching: ",scratchingnumber, "TrackRating: ",trackrating, gt, mr, lt, fq, sq, tq, frq)
                        Values = [date_str, venue, racenumber, weather1, trackrating, horsename, BSP, poolSizeAmount]

                        mycursor.execute(sql, Values)
                            #except:
                        #conn.commit()
                        
                            # }
                        #print(f"scraping date:{date_str} market:1.{mid} venue:{event['venueName']} raceNo:{event['raceNo']} racetype:{meeting['RACE_TYPE']} marketname:{market['EVENT_NAME']} country:{event['country']}")
                    
            else:
                print('not harness or Aus')


