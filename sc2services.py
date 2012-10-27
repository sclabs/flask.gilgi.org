import sc2ranks
import sc2data

def getdata():
    # these will store our data
    data = {}
    data['players'] = []

    # create an object to handle our api calls
    ranks = sc2ranks.Sc2Ranks(sc2data.apikey)
    
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

        # fill in hard fields with real values
        for team in info.teams:
            if not team.is_random:
                player['leagues'][team.bracket - 1] = team.league
                player['ranks'][team.bracket - 1] = team.division_rank

        # append this player to the list
        data['players'].append(player)

    # return the data
    return data
        
def makeportrait(portrait, size=75):
    return "background: url('/assets/img/portraits/portraits-%d-%d.jpg') -%dpx -%dpx no-repeat; width: 75px; height: 75px;" % (portrait.icon_id, size, portrait.column * size, portrait.row * size)
