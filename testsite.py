from bs4 import BeautifulSoup
import pprint
import requests
import datetime


timezone = {'Premier League':7,'Spanish La Liga':8,'Italian Serie A':7,'The FA Cup':7,'German Bundesliga':7}

gTeams = ['Real Madrid','Liverpool','Manchester City','AC Milan','Barcelona','Juventus','Bayern Munich','Borussia Dortmund','Chelsea','Arsenal' ]

print('TODAYS DATE: '+datetime.date.today().strftime("%d-%B-%Y %A"))

def convertTimezone(ur_timezone,given_timezone):
    timeobj = datetime.datetime.strptime(given_timezone,'%d-%B-%Y %H:%M')
    timeobj += datetime.timedelta(hours=ur_timezone)
    return timeobj


for _day in range(0,7):
    local = datetime.date.today() + datetime.timedelta(days=_day)
    weekday = local.strftime("%A")
    local = local.strftime("%d-%B-%Y")

#https://www.skysports.com/football/fixtures-results/21-June-2020
    newwebsite = 'https://www.skysports.com/football/fixtures-results/'+local
    newsource= requests.get(newwebsite).text
    newsoup= BeautifulSoup(newsource,'lxml')

    find_team = []
#<span class="swap-text__target">Newcastle United</span>
    for n in newsoup.find_all('span',{'class':"swap-text__target"}):
        if '\n' not in n:
            find_team.append(n)

    '''
    #filter out /n 
    for team in find_team:
        if '\n' in team:
            find_team.remove(team)
    '''
    fixture=[]
    time = []
    for i in range(1,len(find_team)-1,2):
        if find_team[i].text.strip() in gTeams or find_team[i+1].text.strip() in gTeams:
            fixture.append(find_team[i])
            fixture.append(find_team[i+1])

    for t in fixture[::2]:
        time.append(t.parent.parent.parent.find('span',{'class':'matches__date'}))


    if(time):
        print('\n ---------------------------------------------- \n')
        x=0
        leag = fixture[0].findPrevious('h5')
        for i in range(len(time)):
            timez = local+' '+time[i].text.strip()
            newtime = convertTimezone(timezone[leag.text],timez)
            print(fixture[x].text.strip()+' vs '+fixture[x+1].text.strip()+' on '+str(newtime.strftime('%d-%B %H:%M%p %a ')))
            x+=2

