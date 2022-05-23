from bs4 import BeautifulSoup
import requests
import os.path
import csv
import json
from time import sleep
h = {"Accept-Language": "en-US"}


#ვიგებთ თუ რა ჭირდება მომხმარებელს,ტოპ 250ის ნახვა თუ კონკრეტული მსახიობის მოძებნა
actor_or_250movie = input("which action would you like,top 250 movies(Sorted by Popularity Ascending) or you want to find and actor: actor or 250 ")
print('-----------------')

while actor_or_250movie != "actor" and actor_or_250movie != "250":
        print("Input was Invalid")
        actor_or_250movie = input("which action would you like,top 250 movies(Sorted by Popularity Ascending) or you want to find and actor: actor or 250 ")
        print('-----------------')

if actor_or_250movie == "actor":
    actor_name = input("input actor(name and surname) ")
    print('-----------------')

    # ვეძებ მომხმარებლის მიერ შეყვანილ მსახიობს
    api_key = 'k_03xy1plm'
    url = f'https://imdb-api.com/en/API/SearchName/k_03xy1plm/{actor_name}'
    reqMS = requests.get(url)
    req_jsonMS = reqMS.text
    req_dictMS = json.loads(req_jsonMS)
    req_dict_readableMS = json.dumps(req_dictMS, indent=5)

    for each in req_dictMS['results']:
        print(f"ID: {each['id']}")
        print(f"Title: {each['title']}")
        print(f"Description: {each['description']}")
        print(f"Image Link: {each['image']}")
        print('-----------------')

    # ვიგებთ უნდა თუ არა CSV ფაილის შენახვა
    response1 = input("do you want to download information about actors best movies(by rating): Y or N ")
    while response1 != "Y" and response1 != "N":
        print("Input was Invalid")
        response1 = input("do you want to download information about actors best movies(by rating): Y or N ")
        print('-----------------')

    if response1 == "Y":
        # ქვემოთ არსებულ ინფუთში მომხმარებელს შეყავს შესაბამისი მსახიობის ID,რომელსაც იღებს აქამდე არსებული კოდის საშუალებით
        actor_code = input("input actor id ")

        url = f'https://www.imdb.com/filmosearch/?explore=title_type&role={actor_code}&ref_=filmo_ref_typ&sort=user_rating,desc&mode=detail&page=1&title_type=movie'

        req = requests.get(url, headers=h)

        html = req.text

        soup = BeautifulSoup(html, 'html.parser')

        # ვამოწმებ უკვე არსებობს თუ არა შეყვანილი მსახიობის csv ფაილი
        if os.path.exists(f'{actor_name}.csv') == False:
            csv_actor = open(f'{actor_name}.csv', "a", newline="\n")
            writer = csv.writer(csv_actor)
            writer.writerow(['Title', 'Rating'])

            csv_row_dict = dict()

            part_title = soup.find_all('h3', {'class': 'lister-item-header'})

            title_list = list()

            for each in part_title:
                title = each.find('a').text
                title_list.append(title)

            part_rating = soup.find_all('div', {'class': 'ratings-bar'})

            index = 0
            for each in part_rating:
                rating = each.find('strong').text
                csv_row_dict[title_list[index]] = rating
                index += 1

            for each in csv_row_dict.keys():
                writer.writerow([each, csv_row_dict[each]])

        else:
            print("Actors CSV file already exists on this device")

    elif response1 == "N":
        print("OK")

elif actor_or_250movie == "250":

    amount = 1
    index = 1
    while amount < 250:
        url = f'https://www.imdb.com/search/title/?groups=top_1000&start={amount}&ref_=adv_prv'

        req = requests.get(url, headers=h)
        html = req.text
        soup = BeautifulSoup(html, 'html.parser')
        part_title = soup.find_all('h3', {'class': 'lister-item-header'})
        print(f'{amount}-{amount + 49}')
        for each in part_title:
            title = each.find('a').text
            print(title)
        print('-----------------')
        amount += 50

sleep(10)






