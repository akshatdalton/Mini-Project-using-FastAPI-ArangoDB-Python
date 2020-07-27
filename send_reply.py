from fastapi import FastAPI, Request
from twilio.rest import Client
import re
import Movie_dattabase

account_sid = 'ACXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
auth_token = 'XXXXXXXXXXXXXXXXXXXXXXXXXXXX'
client = Client(account_sid, auth_token)

app = FastAPI()

@app.post("/")
async def sms_reply(request: Request):
    item = await request.body()
    item_name = str(item)
    print(item_name)

    match = re.search(r'Body=([\w+%]+)&', item_name)
    keywords = match.group(1).split('+')

    match2 = re.findall(r'From=([\w%]+)&', item_name)
    sent_by = match2[0][3:]

    list = set

    if len(keywords) == 2:
        if str(keywords[1]) == 'ACTORS':
            list = Movie_database.all_actors_list()
        else:
            list = Movie_database.all_movies_list()
    elif len(keywords) == 5:
        if keywords[-3] == 'ACTOR':
            list =  Movie_database.actors_movie_list(keywords[-1])
        else:
            list =  Movie_database.movie_actor_list(keywords[-1])
    else:
        if keywords[-3] == 'DIRECTOR':
            list = Movie_database.actor_director_list(keywords[3], keywords[-1])
        elif keywords[-3] == 'ACTOR':
            list = Movie_database.actors_common_list(keywords[3], keywords[-1])
        else:
            list = {'Try Something Else'}

    message = str
    for i in list:
        message += str(i) + " "
        
    client.messages.create(
                     body= f"{message}",
                     from_= 'XXXXXXXXXXX', # your Twilio Phone Number
                     to= f'+{sent_by}'
                )

    return str(list)
    
