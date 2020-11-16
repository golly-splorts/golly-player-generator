import os
import re
import json

with open('roster.json', 'r') as f:
    roster = json.load(f)

if not os.path.exists('pages'):
    raise Exception("Error: pages/ directory must exist")

for teamname, teamroster in roster.items():

    html = []
    html.append('{% extends \'base.html\' %}')
    html.append('{% block content %}')
    html.append('<div class="container">')
    html.append('<h1>%s Roster</h1>'%teamname)
    html.append('<table class="table">')
    html.append('  <thead>')
    html.append('  <tr>')
    html.append('    <th>Player Name</th>')
    html.append('    <th>Player Row</th>')
    html.append('    <th>Player Col</th>')
    html.append('  </tr>')
    html.append('  </thead>')
    html.append('  <tbody>')

    sorted_team = sorted(teamroster,  key=(lambda x: (x[1], x[2])))
    for player, row, col in sorted_team:
        html.append('    <tr>')
        html.append('    <td>%s</td><td>%s</td><td>%s</td>'%(player, row, col))
        html.append('    </tr>')

    html.append('  </tbody>')
    html.append('</table>')
    html.append('</div>')
    html.append('{% endblock %}')

    fname = teamname.lower()
    fname = re.sub(' ', '_', fname)
    fname += '.html'

    print("writing file %s"%fname)
    with open('pages/' + fname, 'w') as f:
        f.write("\n".join(html))
