import requests
import time
from lxml import etree

url = "https://dayzsalauncher.com/#/servercheck/103.152.197.191:2303"
response = requests.get(url)
time.sleep(5)  # Delay for 5 seconds

parser = etree.HTMLParser()
tree = etree.fromstring(response.content, parser)

server_players = tree.xpath('/html/body/app-root/app-server-check/main/div[2]/form/div/label')

if server_players:
    result_players = server_players[0].text.strip()
    print(f'Players::::::|', result_players)
else:
    print("Not found.")
