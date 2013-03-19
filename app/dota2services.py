from dotamatch import teams
import dota2data
from app import db
from models import Dota2Team

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

        # check to see if this team is in the database yet
        db_team = db.session.query(Dota2Team).filter(Dota2Team.team_id==team.team_id).all()
        
        if db_team:
            # team_id should be unique so grab the first element of the list
            db_team = db_team[0]

            # if webapi says inactive fill in teaminfo from database
            if team.rating == 'inactive':
                teaminfo['rating'] = db_team.rating
            
            else:
                # update the team rating in the database if necessary
                if team.rating != db_team.rating:
                    db_team.rating = team.rating
                    db.session.commit()
                
                # either way the webapi rating goes into teaminfo
                teaminfo['rating'] = str(team.rating)
                
        else:
            # make a new row in the database
            db_team = Dota2Team(team.team_id)
            db.session.add(db_team)
            db.session.commit()

            # webapi rating goes into teaminfo
            teaminfo['rating'] = str(team.rating)

        # put the other info we want in to the dict
        teaminfo['team_id'] = team.team_id
        teaminfo['name'] = team.name
        teaminfo['tag'] = team.tag
        teaminfo['games_played'] = team.games_played_with_current_roster
        teaminfo['url'] = 'http://dotabuff.com/teams/' + str(team.team_id)

        # add this team to the list
        data['teams'].append(teaminfo)

    # return the data
    return data
