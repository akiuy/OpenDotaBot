#импорт библиотек // import libraries
import requests
import json
import os
import telebot
import datetime
from dotenv import load_dotenv


#Получение токена с .env файла // Getting token from .env file
load_dotenv()
bot=telebot.TeleBot(os.getenv("TOKEN"))

#Прочтение файла с героями // #Reading file with heroes
with open('heroes.json', 'r') as heroes:
  heroid = json.load(heroes)


#Обработка команды /start // processing /start command
@bot.message_handler(commands=['start'])
def get_match_id(message):
  bot.send_message(message.chat.id, 'Привет. Этот бот создан на базе OpenDota API\nОзнакомиться с командами: /help')


#Обработка команды /help // processing /help command
@bot.message_handler(commands=['help'])
def get_match_id(message):
  bot.send_message(message.chat.id, '/findmatch - узнать информацию о матче по его ID')


#Обработка команды /findmatch // processing /findmatch command
@bot.message_handler(commands=['findmatch'])
def get_match_id(message):
  match_id = bot.send_message(message.chat.id, 'Введите id матча')
  bot.register_next_step_handler(match_id, get_match_data) #Берёт информацию с сообщения пользователя // Taking information from user`s message

def get_match_data(message):
  match_id = int(message.text) #Обозначение инфомации пользователя в переменную // Designating user information into a variable 
  try:
    resp = requests.get(f'https://api.opendota.com/api/matches/{match_id}') # Отправка запроса на сервер opendota.com // Sending a request to the opendota.com server
    response = resp.json() # Получение ответа в виде json-файла // Collecting info in json-file format

    with open(f'{match_id}.json', 'w') as outfile:
      json.dump(response, outfile) #Сохранение полученного json-файла // Saving received json-file

    with open(f'{match_id}.json', 'r') as outfile:
      result = json.load(outfile) #Чтение полученного json-файла // Reading received json-file

    #Обработка и сохранение результатов матча в переменные // Processing and saving match results into variables
    data_win = result["radiant_win"]
    data_duration = str(datetime.timedelta(seconds=result["duration"]))
    data_radiant_score = result["radiant_score"]
    data_dire_score = result["dire_score"]
    #Создание пустых списков для сохранения информации о игроках // Creating empty lists to save player information
    data_players_radiant = []
    data_players_dire = []


    #Обработка информации о игроках, сохранение в списки в виде словарей // Processing information about players, saving to lists in the form of dictionaries
    for elem in result["players"]:
      if elem.get("team_number") == 0: #Если игрок находится на стороне сил света // If the player is on the radiant side
        players_info = dict()
        players_info['hero'] = heroid[str(elem.get('hero_id'))]
        players_info['kills'] = elem.get("kills", None)
        players_info['deaths'] = elem.get("deaths", None)
        players_info['assists'] = elem.get("assists", None)
        data_players_radiant.append(players_info)
      elif elem.get("team_number") == 1: #Если игрок находится на стороне сил тьмы // If the player is on the dire side
        players_info = dict()
        players_info['hero'] = heroid[str(elem.get('hero_id'))]
        players_info['kills'] = elem.get("kills", None)
        players_info['deaths'] = elem.get("deaths", None)
        players_info['assists'] = elem.get("assists", None)
        data_players_dire.append(players_info)
      else:
        pass


    #Отправка ботом сообщения с информацией о матче // Bot sending a message with information about a match
    if data_win: #Победа сил света // Radiant match-win 
      bot.send_message(message.chat.id, f'''🏆Силы света [{data_radiant_score}:{data_dire_score}] Силы тьмы 
Длительность: {data_duration}\n
🏆Силы света:\n
{data_players_radiant[0].get('hero')} - [{data_players_radiant[0].get('kills')}/{data_players_radiant[0].get('deaths')}/{data_players_radiant[0].get('assists')}]
{data_players_radiant[1].get('hero')} - [{data_players_radiant[1].get('kills')}/{data_players_radiant[1].get('deaths')}/{data_players_radiant[1].get('assists')}]
{data_players_radiant[2].get('hero')} - [{data_players_radiant[2].get('kills')}/{data_players_radiant[2].get('deaths')}/{data_players_radiant[2].get('assists')}]
{data_players_radiant[3].get('hero')} - [{data_players_radiant[3].get('kills')}/{data_players_radiant[3].get('deaths')}/{data_players_radiant[3].get('assists')}]
{data_players_radiant[4].get('hero')} - [{data_players_radiant[4].get('kills')}/{data_players_radiant[4].get('deaths')}/{data_players_radiant[4].get('assists')}]

Силы тьмы:\n
{data_players_dire[0].get('hero')} - [{data_players_dire[0].get('kills')}/{data_players_dire[0].get('deaths')}/{data_players_dire[0].get('assists')}]
{data_players_dire[1].get('hero')} - [{data_players_dire[1].get('kills')}/{data_players_dire[1].get('deaths')}/{data_players_dire[1].get('assists')}]
{data_players_dire[2].get('hero')} - [{data_players_dire[2].get('kills')}/{data_players_dire[2].get('deaths')}/{data_players_dire[2].get('assists')}]
{data_players_dire[3].get('hero')} - [{data_players_dire[3].get('kills')}/{data_players_dire[3].get('deaths')}/{data_players_dire[3].get('assists')}]
{data_players_dire[4].get('hero')} - [{data_players_dire[4].get('kills')}/{data_players_dire[4].get('deaths')}/{data_players_dire[4].get('assists')}]
''')
      
    else: ##Победа сил тьмы // Dire match-win 
      bot.send_message(message.chat.id, f'''Силы света [{data_radiant_score}:{data_dire_score}] Силы тьмы🏆
Длительность: {data_duration}
Силы света:\n
{data_players_radiant[0].get('hero')} - [{data_players_radiant[0].get('kills')}/{data_players_radiant[0].get('deaths')}/{data_players_radiant[0].get('assists')}]
{data_players_radiant[1].get('hero')} - [{data_players_radiant[1].get('kills')}/{data_players_radiant[1].get('deaths')}/{data_players_radiant[1].get('assists')}]
{data_players_radiant[2].get('hero')} - [{data_players_radiant[2].get('kills')}/{data_players_radiant[2].get('deaths')}/{data_players_radiant[2].get('assists')}]
{data_players_radiant[3].get('hero')} - [{data_players_radiant[3].get('kills')}/{data_players_radiant[3].get('deaths')}/{data_players_radiant[3].get('assists')}]
{data_players_radiant[4].get('hero')} - [{data_players_radiant[4].get('kills')}/{data_players_radiant[4].get('deaths')}/{data_players_radiant[4].get('assists')}]\n
🏆Силы тьмы:\n
{data_players_dire[0].get('hero')} - [{data_players_dire[0].get('kills')}/{data_players_dire[0].get('deaths')}/{data_players_dire[0].get('assists')}]
{data_players_dire[1].get('hero')} - [{data_players_dire[1].get('kills')}/{data_players_dire[1].get('deaths')}/{data_players_dire[1].get('assists')}]
{data_players_dire[2].get('hero')} - [{data_players_dire[2].get('kills')}/{data_players_dire[2].get('deaths')}/{data_players_dire[2].get('assists')}]
{data_players_dire[3].get('hero')} - [{data_players_dire[3].get('kills')}/{data_players_dire[3].get('deaths')}/{data_players_dire[3].get('assists')}]
{data_players_dire[4].get('hero')} - [{data_players_dire[4].get('kills')}/{data_players_dire[4].get('deaths')}/{data_players_dire[4].get('assists')}]
''')
      
    os.remove(f'{match_id}.json') #Удаление ранее полученного json-файла // Deleting a previously received json file
  except:
    pass
  


bot.infinity_polling()

