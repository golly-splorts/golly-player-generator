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
        """Generate a name, with some probability of alliteration"""
        alliterationrate = 0.10

        # Get first name
        nfirst = len(self.first_names)
        firstindex = random.randint(0, nfirst-1)
        firstname = self.first_names[firstindex]
        
        if random.random() < alliterationrate:
            # Alliterate
            lastnamesletter = [j for j in self.last_names if j[0]==firstname[0]]
            nlast = len(lastnamesletter)
            assert nlast>0
            lastindex = random.randint(0, nlast-1)
            lastname = lastnamesletter[lastindex]
        else:
            # Random
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
                leader = self.consonants[random.randint(0,ncon-1)].upper()
                if leader == 'Q':
                    leader = 'Qu'
                name = leader + base
                names.append(name)

            full_name = " ".join(names)
            playernames.add(full_name)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%rows
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
            c = i%rows
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
            c = i%rows
            roster.append([playernames.pop(), r, c])
            i += 1
            if i==nplayers:
                break

        return roster


    def texas_roster(self):
        """
        Baltimore Texas roster: everybody has Texas in their name.
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        # Set some probabilities (arbitrary)
        prob_split_firstname = 0.33
        prob_alliteration = 0.10

        playernames = set()
        while len(playernames) < nplayers:

            # Get random first name
            nfirst = len(self.first_names)
            firstindex = random.randint(0, nfirst-1)
            firstname = self.first_names[firstindex]
            
            if ' ' in firstname and random.random() < prob_split_firstname:
                # if we get a first name with a space,
                # some probability we split it,
                # insert Texas somewhere,
                # and reassemble it.
                tokens = firstname.split(' ')
                r = random.randint(0,len(tokens))
                newtokens = tokens[:r] + ['Texas'] + tokens[r:]

                playername = " ".join(newtokens)
                playernames.add(playername)

            else:
                if random.random() < prob_alliteration:
                    # Alliterate
                    lastnamesletter = [j for j in self.last_names if j[0]==firstname[0]]
                    nlast = len(lastnamesletter)
                    assert nlast>0
                    lastindex = random.randint(0, nlast-1)
                    lastname = lastnamesletter[lastindex]
                else:
                    # Random
                    nlast = len(self.last_names)
                    lastindex = random.randint(0, nlast-1)
                    lastname = self.last_names[lastindex]

                tokens = firstname.split(' ') + lastname.split(' ')
                r = random.randint(0,len(tokens))
                newtokens = tokens[:r] + ['Texas'] + tokens[r:]

                playername = " ".join(newtokens)
                playernames.add(playername)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%rows
            roster.append([playernames.pop(), r, c])
            i += 1
            if i==nplayers:
                break

        return roster


    def shells_roster(self):
        """
        Delaware Shells roster:
        The names are a mix of business things.
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        # Corporate suffixes
        corp_suffixes = [ "LLC", "SLLC", "PLLC",
            "National Trust and Savings", "LP",
            "LLP", "LLLP", "Credit Union", "Association",
            "Bank", "Loans", "Accounting",
            "Company", "Co.", "Corporation", "Corp.",
            "Club", "Foundation", "Fund",
            "Inc.", "Institute",
            "Society", "Union",
            "Syndicate", "Limited", "Ltd."
        ]

        # C-level suffixes
        c_suffixes = ["CEO", "CTO", "CIO", "CISO", "CFO", "COO", "CLO"]

        # Set some probabilities (arbitrary)
        prob_corp = 0.80

        playernames = set()
        while len(playernames) < nplayers:

            if random.random() < prob_corp:
                # Get a random first or last name,
                # and add a corporate suffix to it
                if random.random() < 0.50:
                    nfirst = len(self.first_names)
                    firstindex = random.randint(0, nfirst-1)
                    name = self.first_names[firstindex]
                else:
                    nlast = len(self.last_names)
                    lastindex = random.randint(0, nlast-1)
                    name = self.last_names[lastindex]
                suffix = corp_suffixes[random.randint(0,len(corp_suffixes)-1)]
                playername = name + " " + suffix
                playernames.add(playername)

            else:
                # Get a random (alliterative) name,
                # and add a C-level suffix to it
                nfirst = len(self.first_names)
                firstindex = random.randint(0, nfirst-1)
                firstname = self.first_names[firstindex]
                # Alliterate
                lastnamesletter = [j for j in self.last_names if j[0]==firstname[0]]
                nlast = len(lastnamesletter)
                assert nlast>0
                lastindex = random.randint(0, nlast-1)
                lastname = lastnamesletter[lastindex]

                name = firstname + " " + lastname
                suffix = c_suffixes[random.randint(0,len(c_suffixes)-1)]
                playername = name + ", " + suffix
                playernames.add(playername)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%rows
            roster.append([playernames.pop(), r, c])
            i += 1

        return roster


    def osha_roster(self):
        """
        Jersey OSHA Violations roster:
        Everybody is named Jim or Jimmy
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        playernames = set()
        while len(playernames) < nplayers:

            firstname = None
            lastname = None
            die = random.random()

            # 90% Jim and Jimi
            # 10% von Smack

            if die < 0.90:
                # first name: Jim/Jimi
                if die < 0.45:
                    firstname = "Jim"
                else:
                    firstname = "Jimmy"

                # last name: anything goes
                if random.random() < 0.50:
                    nfirst = len(self.first_names)
                    firstindex = random.randint(0, nfirst-1)
                    lastname = self.first_names[firstindex]
                else:
                    nlast = len(self.last_names)
                    lastindex = random.randint(0, nlast-1)
                    lastname = self.last_names[lastindex]

                playername = firstname + " " + lastname
                if 'igg' in playername or 'uck' in playername or lastname[0] in self.vowels:
                    continue
                while playername in playernames:
                    ncon = len(self.consonants)
                    leader = self.consonants[random.randint(0, ncon-1)].upper()
                    if leader == 'Q':
                        leader = 'Qu'
                    newlastname = leader + lastname[1:]
                    playername = firstname + " " + newlastname

                playernames.add(playername)

            else:
                # last name: von Smack
                lastname = "von Smack"

                # first name: anything goes
                if random.random() < 0.50:
                    nfirst = len(self.first_names)
                    firstindex = random.randint(0, nfirst-1)
                    firstname = self.first_names[firstindex]
                else:
                    nlast = len(self.last_names)
                    lastindex = random.randint(0, nlast-1)
                    firstname = self.last_names[lastindex]

                playername = firstname + " " + lastname
                if 'igg' in playername or 'uck' in playername or firstname[0] in self.vowels:
                    continue
                while playername in playernames:
                    ncon = len(self.consonants)
                    leader = self.consonants[random.randint(0, ncon-1)].upper()
                    if leader == 'Q':
                        leader = 'Qu'
                    newfirstname = leader + firstname[1:]
                    playername = newfirstname + " " + lastname

                playernames.add(playername)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%rows
            roster.append([playernames.pop(), r, c])
            i += 1

        return roster


    def butchers_roster(self):
        """
        Tucson Butchers roster:
        Everybody has permutations of blood, bone, meat, flesh, etc.
        """
        rows = self.rows
        cols = self.cols
        nplayers = rows*cols

        playernames = set()
        while len(playernames) < nplayers:

            part1 = ["Meat", "Flesh", "Bone", "Blood", "Gore", "Carnage", "Tooth"]
            part2 = ["meat", "flesh", "bone", "blood", "gore", "snack", "saw", "stretcher"] 
            part2 += ["cutter", "ripper", "drainer", "pump", "thrust", "pusher", "remover"]
            part2 += ["flame", "saw", "sticks", "runner", "mancer", "pop"]

            if random.random() < 0.50:
                nfirst = len(self.first_names)
                firstindex = random.randint(0, nfirst-1)
                firstname = self.first_names[firstindex]
                if random.random() < 0.10:
                    lastname = part1[random.randint(0,len(part1)-1)]
                else:
                    lastname = part1[random.randint(0,len(part1)-1)] + part2[random.randint(0,len(part2)-1)]

            else:
                nlast = len(self.last_names)
                lastindex = random.randint(0, nlast-1)
                lastname = self.last_names[lastindex]
                if random.random() < 0.10:
                    firstname = part1[random.randint(0,len(part1)-1)]
                else:
                    firstname = part1[random.randint(0,len(part1)-1)] + part2[random.randint(0,len(part2)-1)]

            playername = firstname + " " + lastname
            playernames.add(playername)

        # Compile all players into the row/column roster
        i = 0
        roster = []
        while len(playernames) > 0:
            r = i//rows
            c = i%rows
            roster.append([playernames.pop(), r, c])
            i += 1

        return roster


    def all_rosters(self):

        team_roster_function_map = {
            #'Detroit Grape Chews': self.grape_chews_roster,
            #'San Diego Balloon Animals': self.balloon_animals_roster,
            #'Alewife Arsonists': self.arsonists_roster,
            #'Baltimore Texas': self.texas_roster,
            'Delaware Corporate Shells': self.shells_roster,
            #'Jersey OSHA Violations': self.osha_roster,
            #'Tucson Butchers': self.butchers_roster
        }

        all_rosters = {}
        for team in self.teams:
            teamname = team['teamName']
            if teamname in team_roster_function_map:
                func = team_roster_function_map[teamname]
                teamroster = func()
            else:
                pass
                #teamroster = self.roster(teamname)
            all_rosters[teamname] = teamroster
        return all_rosters


if __name__=="__main__":
    p = PlayerGen()
    all_rosters = p.all_rosters()
    with open('testroster.json', 'w') as f:
        json.dump(all_rosters, f)
