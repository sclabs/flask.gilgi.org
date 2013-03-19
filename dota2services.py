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
        # get the team info
        team = teamobject.teams(start_at_team_id=teamid,teams_requested=1)[0]

        # this dict will store the team's information
        teaminfo = {}

        # put the info we want in to the dict
        teaminfo['name'] = team.name
        teaminfo['tag'] = team.tag
        teaminfo['games_played'] = team.games_played_with_current_roster
        teaminfo['rating'] = team.rating
        teaminfo['url'] = 'http://dotabuff.com/teams/' + str(team.team_id)

        # add this team to the list
        data['teams'].append(teaminfo)

    # return the data
    return data
