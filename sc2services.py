import sc2ranks
import sc2data

def getdata():
    # this will store our data
    data = {}

    # create an object to handle our api calls
    ranks = sc2ranks.Sc2Ranks(sc2data.apikey)

    # individual league ranks go into the players array
    data['players'] = []
    
    for character in sc2data.characters:
        # this will store data about the player
        player = {}

        # get some data
        info = ranks.fetch_base_character_teams(character['region'],
                                                character['name'],
                                                character['id'])
        
        # fill in easy fields
        player['name'] = info.name
        player['portrait'] = makeportrait(info.portrait)

        # fill in hard fields with default values
        player['leagues'] = ["none", "none", "none", "none"]
        player['ranks'] = [0, 0, 0, 0]
        player['url'] = sc2ranks.character_url(character['region'],
                                            character['name'],
                                            character['id'])
        player['levels'] = [1, 1, 1, 1]

        # fill in hard fields with real values
        for team in info.teams:
            if team.bracket == 1 or team.is_random:
                player['leagues'][team.bracket - 1] = team.league
                player['ranks'][team.bracket - 1] = team.division_rank
                if team.division_rank <= 8:
                    player['levels'][team.bracket - 1] = 4
                elif team.division_rank <= 25:
                    player['levels'][team.bracket - 1] = 3
                elif team.division_rank <= 50:
                    player['levels'][team.bracket - 1] = 2
                else:
                    player['levels'][team.bracket - 1] = 1

        # append this player to the list
        data['players'].append(player)

    # 2v2 teams go into twos
    data['twos'] = []

    for two in sc2data.twos:
        # this will store information about the team
        teaminfo = {}

        # get some data
        info = ranks.fetch_character_teams(two['region'],
                                           two['name'],
                                           two['id'],
                                           2)

        # find the particular 2v2 team we want
        particularteam = None
        for team in info.teams:
            if team.members[0].name == two['partner']:
                particularteam = team
                break

        # fill in general data
        teaminfo['league'] = particularteam.league
        teaminfo['rank'] = particularteam.division_rank
        if particularteam.division_rank <= 8:
            teaminfo['level'] = 4
        elif particularteam.division_rank <= 25:
            teaminfo['level'] = 3
        elif particularteam.division_rank <= 50:
            teaminfo['level'] = 2
        else:
            teaminfo['level'] = 1

        # this list stores info about the team members
        teaminfo['members'] = [
            {'name': two['name']},
            {'name': two['partner']}]

        # add portraits
        for member in teaminfo['members']:
            for player in data['players']:
                if member['name'] == player['name']:
                    member['portrait'] = player['portrait']
                    break

        # append this team to the list
        data['twos'].append(teaminfo)

    # return the data
    return data
        
def makeportrait(portrait, size=75):
    return "background: url('/assets/img/portraits/portraits-%d-%d.jpg') -%dpx -%dpx no-repeat; width: 75px; height: 75px;" % (portrait.icon_id, size, portrait.column * size, portrait.row * size)
