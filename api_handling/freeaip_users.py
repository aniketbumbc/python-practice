import requests


def fetch_random_user():
    url = 'https://api.freeapi.app/api/v1/public/randomusers?page=1&limit=10'
    response = requests.get(url)
    data = response.json()

    if data["success"] and "data" in data:
        user_data = data["data"]["data"]
        for user in user_data:
            print(user["name"]["title"]+ ". " + user["name"]["first"] + " " + user["name"]["last"])
        
    else:
        raise Exception("Failed to fetch user data")
        
        


# users = data.get("data", {}).get("data", [])
# for user in users:
#     name = user.get("name", {})
#     title = name.get("title", "")
#     first = name.get("first", "")
#     last = name.get("last", "")
#     print(f"{title}. {first} {last}")


def main():
    try:
        fetch_random_user()
    except Exception as e:
        print(e)



main()