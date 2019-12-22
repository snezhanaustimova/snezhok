#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import vk_api, random
import json
import requests
import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

vk_session = vk_api.VkApi(token = 'd4579e847bcf3753fbadc6eb68ebba9a4e233804426ef761a4083f48d20505bbbaf870b012948f697f289')

from vk_api.longpoll import VkLongPoll, VkEventType

longpoll = VkLongPoll(vk_session)

vk = vk_session.get_api()

def get_html(url):
    if url:
        r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
        html = r.text
        return html

def parser(html):
    match_list = []
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('div', class_='matches-list')
    matches = table.find_all('a', class_='matches-list-match')
    for i in range(len(matches)):
        
        data_matches = []
        
        match = matches[i].find('div', class_='match-details')

        time = match.find('span', class_='match-time-time')
        date = match.find('span', class_='match-time-date')
        time = str(time.text).strip()
        date = str(date.text).strip()

        teams = match.find('span', class_='match-title')
        team1 = teams.find('span', class_='team team1')
        team2 = teams.find('span', class_='team team2')
        team1 = str(team1.text).strip()
        team2 = str(team2.text).strip()

        tour = matches[i].find('span', class_='match-cat')
        tour = str(tour.text).strip()

#         print(time, date, team1, ' vs ', team2, '     ', tour)

        date = time + ' ' + date
        date = datetime.datetime.strptime(date, '%H:%M %d.%m.%Y')

        data_matches.append(time)
        data_matches.append(date)
        data_matches.append(team1)
        data_matches.append(team2)
        data_matches.append(tour)
        
        match_list.append(data_matches)
        
    return match_list

def get_engl():
    url = 'https://www.liveresult.ru/football/England/Premier-League/scheduled/'
    data = parser(get_html(url))
    return data

def get_germ():
    url = 'https://www.liveresult.ru/football/Germany/Bundesliga-I/scheduled/'
    data = parser(get_html(url))
    return data

def get_span():
    url = 'https://www.liveresult.ru/football/Spain/LaLiga/scheduled/'
    data = parser(get_html(url))
    return data

global Random

def random_id():
    Random = 0
    Random += random.randint(0, 10000000)
    return Random

while True:
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text.lower() == 'привет':
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Привет&#128522; Узнай расписание самых интересных матчей прямо сейчас!&#128521;)',
                    keyboard = open('keyboard.json', "r", encoding='UTF-8').read(),
                    random_id = random_id()
                )
            elif event.text.lower() == 'расписание':
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Всё, что есть...&#128517;',
                    keyboard = open('timetable.json', "r", encoding='UTF-8').read(),
                    random_id = random_id()
                )
                
            elif event.text.lower() == 'английская премьер-лига 2019/2020':
                engl = get_engl()
                match_list = []
                for i in engl:
                    match_view = ''
                    match_view = str(i[1])[:-8] + ' в ' + str(i[0]) + ': ' + str(i[2]) + ' VS. ' + str(i[3]) + ' – ' + str(i[4])
                    match_list.append(match_view)
                for j in match_list:       
                    vk.messages.send(
                        user_id = event.user_id,
                        message = j,
                        random_id = random_id()
                    )
                    
            elif event.text.lower() == 'бундеслига 2019/2020':
                germ = get_germ()
                match_list = []
                for i in germ:
                    match_view = ''
                    match_view = str(i[1])[:-8] + ' в ' + str(i[0]) + ': ' + str(i[2]) + ' VS. ' + str(i[3]) + ' – ' + str(i[4])
                    match_list.append(match_view)
                for j in match_list:       
                    vk.messages.send(
                        user_id = event.user_id,
                        message = j,
                        random_id = random_id()
                    )
                    
            elif event.text.lower() == 'ла-лига 2019/2020':
                span = get_span()
                match_list = []
                for i in span:
                    match_view = ''
                    match_view = str(i[1])[:-8] + ' в ' + str(i[0]) + ': ' + str(i[2]) + ' VS. ' + str(i[3]) + ' – ' + str(i[4])
                    match_list.append(match_view)
                for j in match_list:       
                    vk.messages.send(
                        user_id = event.user_id,
                        message = j,
                        random_id = random_id()
                    )

            else:
                vk.messages.send(
                    user_id = event.user_id,
                    message = 'Я хоть и машина, но не въезжаю&#128532;\nМожет, лучше посмотришь расписание?&#128530;',
                    keyboard = open('keyboard.json', "r", encoding='UTF-8').read(),
                    random_id = random_id()
                )

