import json
import datetime
import random
import string
from random import randrange

path = './temp/data.json'

def main(users):
    data = []
    for user_id, user in enumerate(users):
        user_entry = []
        days = user['days']
        starting_day = datetime.datetime.today() - datetime.timedelta(days)
        address = "ronin:"+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
        print(address)
        personal_address = "ronin:"+''.join(random.choice(string.ascii_lowercase + string.digits) for _ in range(20))
        curr_slp = 0
        for x in range(0, days):
            curr_day = starting_day + datetime.timedelta(x)
            data_entry = {
                "scholar_id": user_id,
                "name": user['name'],
                "address": address,
                "personal_address": personal_address,
                "slp_bal": curr_slp,
                "created_at": curr_day.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "manager_id": 0
            }
            curr_slp += randrange(100, 150)
            user_entry.append(data_entry)
        data.append(user_entry)
    f = open(path, 'w')
    json.dump(data, f, indent=4)

if __name__ == "__main__":
    users = [
        {
            "name": "t1",
            "days": 23
        },
        {
            "name": "d1",
            "days": 33
        },
        {
            "name": "c1",
            "days": 44
        }
    ]
    main(users)