import os
import re
import json

with open('roster.json', 'r') as f:
    roster = json.load(f)

if not os.path.exists('pages'):
    raise Exception("Error: pages/ directory must exist")

for teamname, teamroster in roster.items():

    tableclasses = "table table-bordered table-striped table-hover table-dark table-sm"

    html = []
    html.append('{% extends \'base.html\' %}')
    html.append('{% block content %}')
    html.append('<div class="container">')
    html.append('<h1>%s <small>Team Roster</small></h1>'%teamname)
    html.append('<table class="%s">'%tableclasses)
    html.append('  <caption>%s Team Roster</caption>'%teamname)
    html.append('  <thead>')
    html.append('  <tr>')
    html.append('    <th class="text-center">Row</th>')
    html.append('    <th class="text-center">Col</th>')
    html.append('    <th>Player Name</th>')
    html.append('  </tr>')
    html.append('  </thead>')
    html.append('  <tbody>')

    sorted_team = sorted(teamroster,  key=(lambda x: (x[1], x[2])))
    #sorted_team = sorted(teamroster,  key=(lambda x: x[0]))
    for player, row, col in sorted_team:
        link = "https://example.com/example.html?p=%s&q=%s"%(row+1, col+1)
        html.append('    <tr>')
        html.append('    <td class="text-center">%s</td><td class="text-center">%s</td><td><a href="%s">%s</a></td>'%(row+1, col+1, link, player))
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
