import json

with open('avatar.json') as f:
    data = json.load(f)

    print(data['avatar_url'])