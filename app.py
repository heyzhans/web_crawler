import json
import csv
import time
import random
import datetime
from os import system

from bs4 import BeautifulSoup
import requests
import schedule
import time

from pymongo import MongoClient
#create web app using python flask
from flask import Flask, render_template, request, redirect, url_for, jsonify


app = Flask(__name__)
#connect to MongoDB azure with PRIMARY CONNECTION STRING
client = MongoClient("mongodb://root:pass@10.0.1.9:27017/webcrawler?authSource=admin") 
db = client["webcrawler"]
collection = db["tengrinews"]
DOMEN = "https://tengrinews.kz/"
URL = "https://tengrinews.kz/tag/%D0%B0%D0%BB%D0%BC%D0%B0%D1%82%D1%8B/"

def get_response(url_def):   
    response = requests.get(url = url_def) 
    if response.status_code == 200:    #хороший get запрос 
        src = response.content 
        return src 
    else:
        return f"{response.status_code}" 

def get_soup(response):
    soup = BeautifulSoup(response, "lxml")
    all_news = soup.find_all("div", class_ = "tn-news-author-list-item")

    news_info = []
    for item in all_news:
        try:
            title = item.find("div", class_ = "tn-news-author-list-item-text").find("span", class_ = "tn-news-author-list-title")  # статья и название статьи
            description = item.find("div", class_ = "tn-news-author-list-item-text").find("p", class_ = "tn-announce") # статья и содержание статьи
            date_time = item.find("div", class_ = "tn-news-author-list-item-text").find("li") # статья и дата публикации статьи
            news_url = DOMEN + item.find("a").get("href") 
        except Exception:
            information = {
            "title": title.text,
            "description": description.text,
            "date_time": date_time.text.strip(),
            "url": news_url
            }
        else:
            information = {
            "title": title.text,
            "description": description.text,
            "date_time": date_time.text.strip(),
            "url": news_url
        }
        news_info.append(information)
    return news_info

#add function search keyword
def search_keyword(keyword):
    response = get_response(url_def = URL) 
    soup = get_soup(response)
    for item in soup:
        if keyword in item["title"]:
            return item


def add():
    response = get_response(url_def = URL) 
    soup = get_soup(response)
    #save to db
    #сохраняет только новые записи не повторяя их и переодически проверяет на наличие новых записей
    for item in soup:
        if collection.find_one({"title": item["title"]}) is None:
            collection.insert_one(item)

#перидодически проверяет на наличие новых записей и добавляет их в базу данных
#запуск функции add() каждые 10 минут
schedule.every(10).minutes.do(add)

# Запуск заданий в отдельном потоке
def run_schedule():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Запуск потока для выполнения заданий
if __name__ == '__main__':
    import threading
    t = threading.Thread(target=run_schedule)
    t.start()
        
@app.route("/")
def index():
    articles = collection.find({})
    return render_template('index.html', articles=articles)
    
    

#add route for search keyword
@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    result = search_keyword(keyword)
    return render_template("search.html", result=result)

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000, debug=True)

























