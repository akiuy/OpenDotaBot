#импорт библиотек // Import libraries
import requests
import json
import os
import telebot
import datetime
from dotenv import load_dotenv


#Получение токена с .env файла // Getting token from .env file
load_dotenv()
bot=telebot.TeleBot(os.getenv("TOKEN"))

#Загрузка файлов с дополнительной информацией // Download files with additional information
with open('heroes.json', 'r') as heroes:
  heroid = json.load(heroes)

with open('countries.json', 'r') as countries:
  country = json.load(countries)

with open('dota2_ranks.json', 'r') as dota2_ranks:
  rank = json.load(dota2_ranks)

#Обработка команды /start // Processing /start command
@bot.message_handler(commands=['start'])
def start_message(message):
  bot.send_message(message.chat.id, 'Привет. OpenDotaBot - бот с открытым исходным кодом, основанный на базе API от <a href="https://www.opendota.com/">OpenDota</a>\nОзнакомиться с командами: /help',\
                    parse_mode='HTML', disable_web_page_preview=True) #Использование HTML для форматирования сообщения и убирание предпросмотра ссылки // Using HTML to format a message and removing the link preview


#Обработка команды /help // Processing /help command
@bot.message_handler(commands=['help'])
def help_message(message):
  bot.send_message(message.chat.id, '''/findmatch - Узнать информацию о матче по его ID
/findplayer - Информация о игроке по его ID
/findaccount - Информация о игроке по его ID''')


#Обработка команды /findmatch // Processing /findmatch command
@bot.message_handler(commands=['findmatch'])
def get_match_id(message):
  match_id = bot.send_message(message.chat.id, 'Введите id матча')
  bot.register_next_step_handler(match_id, get_match_data) #Ожидает ответа пользователя с информацией // Waits for user response with information

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


#Обработка команд /findplayer и /findaccount // Handling the /findplayer and /findaccount commands
@bot.message_handler(commands=['findplayer', 'findaccount'])
def get_account_id(message):
  account_id = bot.send_message(message.chat.id, 'Введите id игрока')
  bot.register_next_step_handler(account_id, get_account_data) #Ожидает ответа пользователя с информацией // Waits for user response with information

def get_account_data(message):
  account_id = int(message.text) #Обозначение инфомации пользователя в переменную // Designating user information into a variable 
  try:
    resp = requests.get(f'https://api.opendota.com/api/players/{account_id}') #Отправка запроса на opendota.com API // Sending a request to the opendota.com API
    response = resp.json()

    with open(f'{account_id}.json', 'w') as outfile:
      json.dump(response, outfile) #Сохранение полученного json-файла // Saving received json-file

    with open(f'{account_id}.json', 'r') as outfile:
      result = json.load(outfile) #Чтение полученного json-файла // Reading received json-file

    
    #Обработка и сохранение информации о игроке в переменные // Processing and storing information about the player into variables
    data_account_id = result['profile']['account_id']
    data_steamid = result['profile']['steamid']
    data_personaname = result['profile']['personaname']
    data_avatarfull = result['profile']['avatarfull']
    #Присваеваем значение None, т.к заполнять будем далее // We assign the value None, because we will fill it in later
    data_country = None
    data_country_emoji = None
    data_player_rank = None


    for elem in country["countries"]: #Считываем элементы в с json файла "countries" // Reading elements from the json file "countries"
      if result["profile"]["loccountrycode"] == elem["country_iso_alpha2"]: #Сравниваем код страны, полученный запросом на API с нашим списком // Compare the country code received by the API request with our list
        data_country = elem.get("country") #Если код страны совпадает, то назначиваем название страны в переменную // If the country code matches, then assign the country name to the variable
      else:
        pass
  
    for elem in rank["ranks"]: #Делаем то же самое, но теперь для получения ранга // We do the same thing, but now to gain rank
      if str(result["rank_tier"]) == elem["rank_id"]:
        data_player_rank = elem.get("rank_name")
      else:
        pass


    #Бот отправляет сообщение с результатом // The bot sends a message with the result
    if data_country == None: #Если страна в стиме отсутствует, то не добавляем её в ответ // If the country is not on Steam, then we do not add it to the answer.
      bot.send_photo(message.chat.id, data_avatarfull, caption=f'''ID аккаунта: {data_account_id}\nSteam ID: {data_steamid}\nНикнейм: {data_personaname}
Ранг: {data_player_rank}''')
    else:
      bot.send_photo(message.chat.id, data_avatarfull, caption=f'''ID аккаунта: {data_account_id}\nSteam ID: {data_steamid}\nНикнейм: {data_personaname}
Страна: {data_country}
Ранг: {data_player_rank}''')

    os.remove(f'{account_id}.json') #Удаление ранее полученного json-файла // Deleting a previously received json file

  except:
    pass


bot.infinity_polling()