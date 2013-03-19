from dotamatch import teams
import dota2data

def getdata():
    # this will store our data
    data = {}

    # team data goes into the teams array
    data['teams'] = []
    
    # make a Teams object
    teamobject = teams.Teams(dota2data.apikey)

    # loop through the sc teams
    for teamid in dota2data.teamids:
        team = teamobject.teams(start_at_team_id=teamid,teams_requested=1)[0]
        team.url = 'http://dotabuff.com/teams/' + str(team.team_id)
        data['teams'].append(team)

    # return the data
    return data
