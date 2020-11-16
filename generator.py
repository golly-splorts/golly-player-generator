import random
import json
import os
import itertools

class PlayerGen(object):
    rows = 100
    cols = 120

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
            if nlast==0:
                import pdb; pdb.set_trace()
                raise Exception()
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
                player = p.name()
                while player in playernames:
                    try:
                        player = p.name()
                    except:
                        continue
                roster.append([player, r, c])
                playernames.add(player)
        return roster

    def all_rosters(self):
        all_rosters = {}
        for team in self.teams:
            teamname = team['teamName']
            teamroster = self.roster(teamname)
            all_rosters[teamname] = teamroster
        return all_rosters


if __name__=="__main__":
    p = PlayerGen()
    all_rosters = p.all_rosters()
    with open('roster.json', 'w') as f:
        json.dump(all_rosters, f)
