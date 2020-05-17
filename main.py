import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
import pprint

res = requests.get('https://news.ycombinator.com/news')
soup = BeautifulSoup(res.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')


def sort_stories_by_votes(hnlist):
    return sorted(hnlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hn(links, subtext):
    hn = []
    count=0
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        full_subtext = subtext[idx].select('.score')
        if len(full_subtext):
            points = int(full_subtext[0].getText().replace(' points', ''))
            if points > 99:
                hn.append({'title': title, 'link': href, 'votes': points})
                count += 1
                #print(count)
        if count>=5:
            break
    return sort_stories_by_votes(hn)


pprint.pprint(create_custom_hn(links,subtext))
account_sid = 'Get from Twilio'
auth_token = 'Get from Twilio'
client = Client(account_sid, auth_token)

message = client.messages \
                .create(
                     body=str(create_custom_hn(links,subtext)),
                     from_='Your generated phone number here:(eg.+025131)76745)',
                     to='Your phone number here Eg:+9180001234518'
                 )
print(message.sid)
