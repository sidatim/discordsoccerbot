import discord as d
from discord.ext import commands as c
from dotenv import load_dotenv
import os 
import requests  
import datetime
import json
from dateutil.relativedelta import relativedelta
load_dotenv()
botToken=os.getenv('token')
compsDict={ ##stores the key value pairing for the league/match
    "PremierLeague": 2021,
    "UCL": 2001,
    "LaLiga": 2014,
    "Bundesliga": 2002, 
    "SerieA": 2019,
    "Ligue1": 2015

}
leagueList=[]   
for i in compsDict.keys():
     with open('teams/'+i+'.json') as league:
          data=json.load(league)
          leagueList.append(data)
          
today=datetime.date.today()
todayString=today.strftime("%Y-%m-%d")
nextWeek=today+datetime.timedelta(days=7)
nextweekString=nextWeek.strftime("%Y-%m-%d")
nextMonth=today +relativedelta(months=1)

apiToken=os.getenv('soccerToken')

intent=d.Intents.default()
intent.typing=False
intent.message_content=True

bot=c.Bot('#',intents=intent)
client=d.client.Client(intents=intent)

@bot.command() 
async def competitions(message):
    if message.author==client.user: 
        return

    channel=message.channel
    user=message.author
    def checkMessage(message):
        if user==message.author and channel==message.channel:
            return message.author,message.channel

    competitions="Which competitions out of the top 5 leagues or Champions League do you want to see within the next week of?"
    
    await channel.send(competitions)
    userMessage=await bot.wait_for("message", timeout=30.0, check=checkMessage)
    league=None
    response=str(userMessage.content)
    
    if response.casefold() in ['premier league', 'pl', 'premierleague', 'epl', 'english premier league', 'prem']:
            league=getLeagues(str(compsDict.get("PremierLeague")))   
            if league['resultSet']['count'] != 0 and league!="Error":
                embedMatches= await createEmbedforMatches(league)
                await channel.send(embed=embedMatches)     
            elif league['resultSet']['count']==0:
                await channel.send("There are no matches scheduled within the next week for the Uefa Champions League")
            elif league=="Error":
                await channel.send("Error getting the matches, please try again later.")
            else:
                await channel.send("Unknown error, please try again later.")
    elif response.casefold() in ['uefachampionsleague','ucl','uefa champions league', 'cl', 'champions league']:
            league=getLeagues(str(compsDict.get("UCL")))
            if league['resultSet']['count'] !=0 and league!="Error":
                embedMatches= await createEmbedforMatches(league)
                await channel.send(embed=embedMatches)
            elif league['resultSet']['count']==0:
                await channel.send("There are no matches scheduled within the next week for the Uefa Champions League")
            elif league=="Error":
                await channel.send("Error getting the matches, please try again later.")     
            else:
                await channel.send("Unknown error, please try again later.")
    elif response.casefold() in ['bundesliga', '1.bundesliga']:
          league=getLeagues(str(compsDict.get("Bundesliga")))   
          if league['resultSet']['count'] !=0 and league!="Error":
                embedMatches= await createEmbedforMatches(league)
                await channel.send(embed=embedMatches)
          elif league['resultSet']['count']==0:
                await channel.send("There are no matches scheduled within the next week for the Bundesliga.")
          elif league=="Error":
                await channel.send("Error getting the matches, please try again later.")     
          else:
                await channel.send("Unknown error, please try again later.") 
          
    elif response.casefold() in ['la liga', 'laliga', 'primera division']:
            league=getLeagues(str(compsDict.get("LaLiga")))   
            if league['resultSet']['count'] !=0 and league!="Error":
                embedMatches= await createEmbedforMatches(league)
                await channel.send(embed=embedMatches)
            elif league['resultSet']['count']==0:
                await channel.send("There are no matches scheduled within the next week for La Liga.")
            elif league=="Error":
                await channel.send("Error getting the matches, please try again later.")     
            else:
                await channel.send("Unknown error, please try again later.") 
           
    elif response.casefold() in ['serie a', 'seriea']:
            league=getLeagues(str(compsDict.get("SerieA")))
            if league['resultSet']['count'] !=0 and league!="Error":
                embedMatches= await createEmbedforMatches(league)
                await channel.send(embed=embedMatches)
            elif league['resultSet']['count']==0:
                await channel.send("There are no matches scheduled within the next week for Serie A.")
            elif league=="Error":
                await channel.send("Error getting the matches, please try again later.")     
            else:
                await channel.send("Unknown error, please try again later.")    
    elif response.casefold() in ['ligue1', 'ligue 1', "ligue 1 mcdonald's", 'uber eats']:
            league=getLeagues(str(compsDict.get("Ligue1")))   
            if league['resultSet']['count'] !=0 and league!="Error":
                embedMatches= await createEmbedforMatches(league)
                await channel.send(embed=embedMatches)
            elif league['resultSet']['count']==0:
                await channel.send("There are no matches scheduled within the next week for Ligue 1.")
            elif league=="Error":
                await channel.send("Error getting the matches, please try again later.")     
            else:
                await channel.send("Unknown error, please try again later.")    
    
    else:
         await channel.send("Not a valid league response")

        


@bot.command()
async def teams(message):
    if message.author==client.user:
        return
    teams="Which team do you want to search the previous 5 and next 5 matches of?"
    channel=message.channel
    await channel.send(teams)
    user=message.author
    def checkMessage(message):
         if user==message.author and channel== message.channel:
              return message.author, message.channel
    
    userMessage=await bot.wait_for("message", timeout=30.0, check=checkMessage)
    teamName=str(userMessage.content)
    t=teamName.casefold()
    team=getTeam(t)
    if team !="Error":
        completed, uncompleted=getTeamResults(team)
        teamEmbed= await createEmbedforteamMatches(completed,uncompleted,teamName)
        await channel.send(embed=teamEmbed)
    else: 
         await channel.send("Not a valid team name or the team is not in the Top 5 leagues or Champions League")
@bot.command()
async def standings(message):
     if message.author==bot.user:
          return
     channel=message.channel
     user=message.author
     standings="Which of the top 5 leagues or Champions League do you want to see the current standings of?"
     await channel.send(standings)
     def checkMessage(message):
          if user==message.author and channel==message.channel:
            return user, channel
     response=await bot.wait_for("message",timeout=30.0, check=checkMessage)
     responseText=str(response.content)
     if responseText.casefold() in ['premier league', 'english premier league', 'premierleague', 'pl', 'epl']:
            standings=getStandings(str(compsDict.get("PremierLeague")))
            standingEmbed=await createEmbedforStandings(standings)
            await channel.send(embed=standingEmbed)
     elif responseText.casefold() in ['la liga', 'primera division' ,'laliga']:
          standings=getStandings(str(compsDict.get("LaLiga")))
          standingEmbed=await createEmbedforStandings(standings)
          await channel.send(embed=standingEmbed)
     elif responseText.casefold() in ['ucl', 'cl', 'champions league', 'uefa champions league']:
          standings=getStandings(str(compsDict.get("UCL")))
          standingEmbed=await createEmbedforStandings(standings)
          for result in standingEmbed:
           await channel.send(embed=result)        
     elif responseText.casefold() == "bundesliga":
          standings=getStandings(str(compsDict.get("Bundesliga")))
          standingEmbed=await createEmbedforStandings(standings)
          await channel.send(embed=standingEmbed)
     elif responseText.casefold() in ['seriea', 'serie a']:
          standings=getStandings(str(compsDict.get("SerieA")))
          standingEmbed=await createEmbedforStandings(standings)
          await channel.send(embed=standingEmbed)
     elif responseText.casefold() in ['ligue1', "ligue 1 mcdonald's", 'uber eats', 'ligue 1']:
          standings=getStandings(str(compsDict.get("Ligue1")))
          standingEmbed=await createEmbedforStandings(standings)
          await channel.send(embed=standingEmbed)
     else:
        await channel.send("Entry is not of the top 5 leagues or Champions League")                    
       
def getLeagues(dictValue): ##get league matches 
    link='http://api.football-data.org/v4/competitions/'+dictValue +'/matches?dateFrom='+todayString +'&dateTo='+nextweekString 
    header={'X-Auth-Token': apiToken }
    response=requests.get(link, headers=header)
    if response.status_code==200:
        matches=response.json()
        return matches
    else:
        print("Failed to get Matches:", response.status_code)
        return "Error"


#USED to get the teams id and official name from the api (should use this to update teams ID and names at the start of every season)
"""
def fetchTeam(dictValue):
    link="http://api.football-data.org/v4/competitions/"+str(dictValue)+ '/teams'
    header={'X-Auth-Token':apiToken}
    response=requests.get(link,headers=header)
    teamlist=[]
    if response.status_code==200:
        teams=response.json()     
        for team in teams['teams']:
              comp={
                'name': team['name'],
                'id': team['id'],
                'alias':[team['shortName'], team['tla']]   
        }
              teamlist.append(comp)
            
        
    else:
        print("Error getting teams", response.status_code)
        return "Error getting teams. Please try again later."
    return teamlist
for key, value in compsDict.items():

    response=fetchTeam(value)
    data={
        'league': key,
        'teams': response
    }
    with open(key+'.json', mode='w') as write_file:
        json.dump(data, write_file, indent=4)
  """ 
  



async def createEmbedforMatches(leagueMatches):
    titleName=str(leagueMatches['competition']['name'])
    embed=d.Embed(title=titleName, description="Displays the next week of matches within the selected competition")
    count=1
    for match in leagueMatches['matches']:
        if match['status']=="FINISHED":
            homeName=str(match['homeTeam']['name'])
            homeScore=str(match['score']['fullTime']['home'])
            awayName=str(match['awayTeam']['name'])
            awayScore=(match['score']['fullTime']['away'])
            embed.add_field(name="Match " + str(count), value=f"{homeName} {homeScore} - {awayScore} {awayName}", inline=False)
        else:
              awayName=str(match['awayTeam']['name'])              
              homeName=str(match['homeTeam']['name'])
              embed.add_field(name="Match " + str(count), value=f"{homeName} - {awayName}", inline=False)
        count=count+1

    return embed


def getTeamResults(teamID):
    link="http://api.football-data.org/v4/teams/"+str(teamID)+"/matches?dateFrom=2025-08-14&dateTo="+str(nextMonth)
    header={'X-Auth-Token': apiToken}
    response=requests.get(link,headers=header)
    if response.status_code==200:
        matches=response.json()['matches']
        completed=[match for match in matches if match['status']=="FINISHED"]
        uncompleted=[match for match in matches if match['status']=="TIMED" or match['status']=="SCHEDULED"]
        sortedCompleted=sorted(completed, key=lambda x:x['utcDate'], reverse=True) 
        sortedunCompleted=sorted(uncompleted, key=lambda x:x['utcDate'])
        result1=sortedCompleted[:5]
        result2=sortedunCompleted[:5]
        return result1, result2
        
    else:
         print("Error getting response", response.status_code)

"""
searchDict={}
for league in leagueList:
     for key,value in league.items():
          for teamName in key:
            x=teamName.casefold()
            searchDict[x]=value
"""
def getTeam(response):
    for league in leagueList:
        for team in league['teams']:
            if response==team['name'].casefold():
                return team['id']
            for alias in team.get('alias', []):
                 if response==alias.casefold():
                      return team['id']
    return "Error"

async def createEmbedforteamMatches(r1,r2,name): 
    embed=d.Embed(title=f"{name.capitalize()}" " matches", description="Displays the last 5 results and up to 5 matches scheduled in the league or Champions League within the next month for " f"{name.capitalize()}")
    counter1=1
    for x in r1:
        embed.add_field(name="Completed Match " +str(counter1), value=f"{x['homeTeam']['name']} {x['score']['fullTime']['home']} - {x['score']['fullTime']['away']} {x['awayTeam']['name']}, Competition: {x['competition']['name']}", inline=False)
        counter1+=1
    counter2=1
    for x in r2:
         embed.add_field(name="Scheduled Match "+  str(counter2), value=f"{x['homeTeam']['name']} - {x['awayTeam']['name']}, Competition: {x['competition']['name']}", inline=False)
         counter2+=1
    return embed

def getStandings(leagueID):
     link="http://api.football-data.org/v4/competitions/" +leagueID+ "/standings"
     header={'X-Auth-Token' : apiToken}
     response=requests.get(link, headers=header)
     if response.status_code==200:
          currentStandings=response.json()
          return currentStandings
     else:
          return "Error"
     

async def createEmbedforStandings(currentStandings):
     titleName=str(currentStandings['competition']['name'])
     embed=d.Embed(title=titleName, description=f"Current Standings of {titleName}")
     newEmbed=d.Embed(title="", description="")
     
     counter=0
     for x in currentStandings['standings']:
          for y in x['table']:
            if counter < 25:
                embed.add_field(name=f"{y['position']}", value=f"{y['team']['name']}   Points: {y['points'] } MP: {y['playedGames']} \n W: {y['won']} D: {y['draw']} L: {y['lost']} GF: {y['goalsFor']} GA: {y['goalsAgainst']} GD: {y['goalDifference']}", inline=False)
                counter+=1
            else:
                newEmbed.add_field(name=f"{y['position']}", value=f"{y['team']['name']} Points: {y['points']} MP: {y['playedGames']} \n W: {y['won']} D: {y['draw']} L: {y['lost']} GF: {y['goalsFor']} GA: {y['goalsAgainst']} GD: {y['goalDifference']}", inline=False)
     counter+=1

     if counter<=25:                   
        return embed
     else:   
        return embed, newEmbed

bot.run(botToken)
