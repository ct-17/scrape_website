import requests
import re
from bs4 import BeautifulSoup
from pymongo import MongoClient
# import dns

link_list = []

# conect MongoDB
try:
    client = MongoClient("mongodb+srv://ct17:nmc%401996@cluster0-exw5t.mongodb.net/scrapeDB?retryWrites=true&w=majority")
    print("Ket noi du lieu thanh cong!!!")
except:
    print("Ket noi du lieu that bai.")

db = client.scrapeDB

collection = db.scrapeCollection

page = requests.get("https://vnexpress.net/giao-duc")
links = BeautifulSoup(page.content)

for link in links.find_all("a", {"data-medium": re.compile("Item*")}):
    link_list.append(link.get("href"))

link_all = list(set(link_list))

for url in link_all:
    get_url = requests.get(url)
    value = BeautifulSoup(get_url.content)
    title = value.h1.text
    body = value.article.text
    data = {"title": title, "body": body}
    collection.insert_one(data)

print(collection.find())
# print(len(link_all))