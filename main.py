import requests
import json
import os
import telebot
import datetime
from dotenv import load_dotenv


load_dotenv()
bot=telebot.TeleBot(os.getenv("TOKEN"))

with open('heroes.json', 'r') as heroes:
  heroid = json.load(heroes)


@bot.message_handler(commands=['start'])
def get_match_id(message):
  bot.send_message(message.chat.id, 'Привет. Этот бот создан на базе OpenDota API\nОзнакомиться с командами: /help')


@bot.message_handler(commands=['help'])
def get_match_id(message):
  bot.send_message(message.chat.id, '/findmatch - узнать информацию о матче по его ID')


@bot.message_handler(commands=['findmatch'])
def get_match_id(message):
  match_id = bot.send_message(message.chat.id, 'Введите id матча')
  bot.register_next_step_handler(match_id, get_match_data)

def get_match_data(message):
  match_id = int(message.text)
  try:
    resp = requests.get(f'https://api.opendota.com/api/matches/{match_id}')
    response = resp.json()

    with open(f'{match_id}.json', 'w') as outfile:
      json.dump(response, outfile)

    with open(f'{match_id}.json', 'r') as outfile:
      result = json.load(outfile)

    data_win = result["radiant_win"]
    data_duration = str(datetime.timedelta(seconds=result["duration"]))
    data_radiant_score = result["radiant_score"]
    data_dire_score = result["dire_score"]
    data_patch = result["patch"]
    data_players_radiant = []
    data_players_dire = []


    for elem in result["players"]:
      if elem.get("team_number") == 0:
        players_info = dict()
        players_info['hero'] = heroid[str(elem.get('hero_id'))]
        players_info['kills'] = elem.get("kills", None)
        players_info['deaths'] = elem.get("deaths", None)
        players_info['assists'] = elem.get("assists", None)
        data_players_radiant.append(players_info)
      elif elem.get("team_number") == 1:
        players_info = dict()
        players_info['hero'] = heroid[str(elem.get('hero_id'))]
        players_info['kills'] = elem.get("kills", None)
        players_info['deaths'] = elem.get("deaths", None)
        players_info['assists'] = elem.get("assists", None)
        data_players_dire.append(players_info)
      else:
        pass


    if data_win:
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
      
    else:
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
      
    os.remove(f'{match_id}.json')
  except:
    pass
  


bot.infinity_polling()

