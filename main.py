from riotwatcher import LolWatcher
import pandas as pd
import matplotlib.pyplot as plt
from requests.exceptions import HTTPError
apiKey = 'RGAPI-4e3ccff0-0013-4c96-bea0-22c5fabc9e75'
watcher = LolWatcher(apiKey)
myRegion = 'na1'
username = ('Quantum')
#username = input("Input your Summoner username:")
userInfo = watcher.summoner.by_name(myRegion, username)
#myRankedStats = watcher.league.by_summoner(myRegion, userInfo['id'])
#myMatches = watcher.match.matchlist_by_puuid(myRegion, userInfo['puuid'],0,10,420)
def jungleTracker():
    try:
        liveGame = watcher.spectator.by_summoner(myRegion, userInfo['id'])
        for i in range(10):
            if liveGame['participants'][i]['summonerName']==username:
                teamCode = liveGame['participants'][i]['teamId']
                break
        for i in range(10):
            if liveGame['participants'][i]['teamId']!= teamCode and (liveGame['participants'][i]['spell1Id']==11 or liveGame['participants'][i]['spell2Id']==11):
                enemyJungler = liveGame['participants'][i]['summonerName']
                print (enemyJungler,"is the enemy jungler.")
                break
        enemyJunglerInfo = watcher.summoner.by_name(myRegion, enemyJungler)
        enemyJunglerMatches = watcher.match.matchlist_by_puuid(myRegion, enemyJunglerInfo['puuid'],0,10,420)
        xCoords, yCoords = [], []
        for i in range (len(enemyJunglerMatches)):
            print (i)
            lastMatch = enemyJunglerMatches[i]
            matchTimeline = watcher.match.timeline_by_match(myRegion, lastMatch)
            matchDetail = watcher.match.by_id(myRegion,lastMatch)
            enemyJunglerId = 0
            for j in range (10):
                if matchTimeline['metadata']['participants'][j]==enemyJunglerInfo['puuid'] and (matchDetail['info']['participants'][j]['summoner1Id']==11 or matchDetail['info']['participants'][j]['summoner2Id']==11):
                    enemyJunglerId=j+1
                    break
            if enemyJunglerId==0:
                continue
            for j in range (2,4):
                xCoords.append([matchTimeline][0]['info']['frames'][j]['participantFrames'][str(enemyJunglerId)]['position']['x'])
                yCoords.append([matchTimeline][0]['info']['frames'][j]['participantFrames'][str(enemyJunglerId)]['position']['y'])
        df = pd.DataFrame({'X Coords':xCoords,'Y Coords':yCoords})
        fig = plt.figure()
        ax1 = fig.add_subplot(111)
        ax1.scatter(df['X Coords'][::2],df['Y Coords'][::2],label="Starting Buff (2:00)")
        ax1.scatter(df['X Coords'][1::2], df['Y Coords'][1::2],label="Scuttle (3:00)")
        for i in range(0,len(xCoords),2):
            plt.arrow(df['X Coords'][i],df['Y Coords'][i],df['X Coords'][i+1]-df['X Coords'][i],df['Y Coords'][i+1]-df['Y Coords'][i],length_includes_head=True,width=75,color='white')
        plt.legend(loc='upper left')
        img = plt.imread('SRMAP.webp')
        plt.imshow(img, extent=[0, 16000, 0, 16000])
        plt.show()
    except HTTPError:
        print("This summoner is not in a live game. Sorry!")
jungleTracker()
"""
def deathInfo():
    totalDeaths, deathTime, gameTime = 0,0,0
    for i in range (len(myMatches)):
        lastMatch = myMatches[i]
        matchDetail = watcher.match.by_id(myRegion, lastMatch)
        for j in range(10):
            if matchDetail['info']['participants'][j]['summonerName']==username:
                gameTime+=matchDetail['info']['participants'][j]['timePlayed']
                totalDeaths+=matchDetail['info']['participants'][j]['deaths']
                deathTime+=matchDetail['info']['participants'][j]['totalTimeSpentDead']
    print ("You have died",totalDeaths,"times, giving you an average of",1/(totalDeaths/(gameTime/60)),"minutes per death.")
    print ("You have spent", deathTime//60, "minutes and", deathTime%60, "seconds dead.")
    print ("You have spent a total of", gameTime//3600, "hours,",(gameTime%3600)//60,"minutes and", gameTime%60,"seconds in game.")
deathInfo()
"""