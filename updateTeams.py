import os
import requests
from bot import compsDict
import json
apiToken=os.getenv('soccerToken')
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
  