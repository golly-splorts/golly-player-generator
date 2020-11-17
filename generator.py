import random
import json
import os
import itertools

class PlayerGen(object):
    rows = 100
    cols = 120

    consonants = "bcdfghjklmnpqrstvwxyz"
    vowels = "aeiou"

    def __init__(self):
        wd = os.path.abspath(os.path.dirname(__file__))
        
        fn = os.path.join(wd, 'sorted_first.txt')
        ln = os.path.join(wd, 'sorted_last.txt')
        tm = os.path.join(wd, 'teams.json')
        
        with open(fn, 'r') as f:
            first_names = f.readlines()
        self.first_names = [s.strip() for s in first_names]
        
        with open(ln, 'r') as f:
            last_names = f.readlines()
        self.last_names = [s.strip() for s in last_names]
        
        with open(tm, 'r') as f:
            teams = json.load(f)
        self.teams = teams

    def name(self):
        """Generate a name, with a 10% chance of alliteration"""
        alliterationrate = 0.10

        # Get first name
        nfirst = len(self.first_names)
        firstindex = random.randint(0, nfirst-1)
        firstname = self.first_names[firstindex]
        
        # Last name has 10% chance of alliteration
        if random.random() < alliterationrate:
            # Alliterate
            lastnamesletter = [j for j in self.last_names if j[0]==firstname[0]]
            nlast = len(lastnamesletter)
            assert nlast>0
            lastindex = random.randint(0, nlast-1)
            lastname = lastnamesletter[lastindex]
        else:
            nlast = len(self.last_names)
            lastindex = random.randint(0, nlast-1)
            lastname = self.last_names[lastindex]

        return firstname + ' ' + lastname

    def roster(self, team_name):
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols
        roster = []
        playernames = set()
        for r in range(rows):
            for c in range(cols):
                player = self.name()
                while player in playernames:
                    try:
                        player = self.name()
                    except:
                        continue
                roster.append([player, r, c])
                playernames.add(player)
        return roster

    
    def grape_chews_roster(self):
        """
        Roster names are all Severus/Serverus combinations,
        3 names, changing the first letter of each name
        Beverus Weverus Xeverus
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        playernames = set()
        while len(playernames) < nplayers:
            names = []
            for i in range(3):
                # 3/4 Severus, 1/4 Serverus
                if random.random() < 0.25:
                    base = "erverus"
                else:
                    base = "everus"
                
                # Pick random first letter
                ncon = len(self.consonants)
                leader = self.consonants[random.randint(0,ncon-1)]
                if leader == 'Q':
                    leader = 'Qu'
                name = leader.upper() + base
                names.append(name)

            full_name = " ".join(names)
            playernames.add(full_name)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%cols
            roster.append([playernames.pop(), r, c])
            i += 1

        return roster


    def balloon_animals_roster(self):
        """
        Roster names consist of 3,000 names,
        and 4 clones of each player.
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        ncore = nplayers//3
        playernames = set()
        while len(playernames) < nplayers:
            name = self.name()
            for suffix in ["I", "II", "III", "IV"]:
                playername = name + " " + suffix
                playernames.add(playername)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%cols
            roster.append([playernames.pop(), r, c])
            i += 1
            if i==nplayers:
                break

        return roster


    def arsonists_roster(self):
        """
        Arsonists roster: MAXIMUM ALLITERATION BABY
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        playernames = set()
        while len(playernames) < nplayers:
            # Get random first name
            nfirst = len(self.first_names)
            firstindex = random.randint(0, nfirst-1)
            firstname = self.first_names[firstindex]

            # Alliterate
            lastnamesletter = [j for j in self.last_names if j[0]==firstname[0]]
            nlast = len(lastnamesletter)
            assert nlast>0
            lastindex = random.randint(0, nlast-1)
            lastname = lastnamesletter[lastindex]

            playername = firstname + ' ' + lastname
            playernames.add(playername)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%cols
            roster.append([playernames.pop(), r, c])
            i += 1
            if i==nplayers:
                break

        return roster


    def all_rosters(self):

        team_roster_function_map = {
            #'Detroit Grape Chews': self.grape_chews_roster,
            #'San Diego Balloon Animals': self.balloon_animals_roster,
            'Alewife Arsonists': self.arsonists_roster,
            #'Baltimore Texas': self.texas_roster,
            #'Delaware Corporate Shells': self.shells_roster,
            #'Jersey OSHA Violations': self.osha_roster
        }

        all_rosters = {}
        for team in self.teams:
            teamname = team['teamName']
            if teamname in team_roster_function_map:
                func = team_roster_function_map[teamname]
                teamroster = func()
            else:
                #teamroster = self.roster(teamname)
                continue
            all_rosters[teamname] = teamroster
        return all_rosters


if __name__=="__main__":
    p = PlayerGen()
    all_rosters = p.all_rosters()
    with open('roster.json', 'w') as f:
        json.dump(all_rosters, f)
