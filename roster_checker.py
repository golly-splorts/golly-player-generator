import json

with open('rosters.json', 'r') as f:
    rosters = json.load(f)

corp = rosters['Delaware Corporate Shells']

print("This number should be 12,000:")
print(len(corp))

