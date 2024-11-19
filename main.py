#импорт библиотек // Import libraries
import requests
import json
import os
import datetime
import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher, F, Router, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import (
    KeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)
from dotenv import load_dotenv


#Получение токена с .env файла // Getting token from .env file
load_dotenv()
TOKEN = os.getenv("TOKEN")
router = Router()

class Form(StatesGroup):
  match_id = State()
  account_id = State()

#Загрузка файлов с дополнительной информацией // Download files with additional information
with open('heroes.json', 'r') as heroes_json:
  heroes = json.load(heroes_json)

with open('countries.json', 'r') as countries:
  country = json.load(countries)

with open('dota2_ranks.json', 'r') as dota2_ranks:
  rank = json.load(dota2_ranks)

#Обработка команды /start // Processing /start command
@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await message.answer('Привет. OpenDotaBot - бот с открытым исходным кодом, основанный на базе API от <a href="https://www.opendota.com/">OpenDota</a>\nОзнакомиться с командами: /help',\
                    parse_mode='HTML', disable_web_page_preview=True) #Использование HTML для форматирования сообщения и убирание предпросмотра ссылки // Using HTML to format a message and removing the link preview


#Обработка команды /help // Processing /help command
@router.message(Command('help'))
async def command_help_handler(message: Message) -> None:
  await message.answer('''/findmatch - Узнать информацию о матче по его ID
/findplayer - Информация о игроке по его ID
''')


#Обработка команды /findmatch // Processing /findmatch command
@router.message(Command('findmatch'))
async def command_findmatch_handler(message, state: FSMContext):
  await state.set_state(Form.match_id)
  await message.answer("Введите ID матча")

@router.message(Form.match_id)
async def get_match_data(message, state: FSMContext):
  await state.update_data(match_id=message.text)
  try:
    resp = requests.get(f'https://api.opendota.com/api/matches/{message.text}') # Отправка запроса на сервер opendota.com // Sending a request to the opendota.com server
    response = resp.json() # Получение ответа в виде json-файла // Collecting info in json-file format

    with open(f'{message.text}.json', 'w') as outfile:
      json.dump(response, outfile) #Сохранение полученного json-файла // Saving received json-file

    with open(f'{message.text}.json', 'r') as outfile:
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
    for elem_result in result["players"]:
      if elem_result.get("team_number") == 0: #Если игрок находится на стороне сил света // If the player is on the radiant side
        players_info = dict()
        for elem_heroes in heroes["heroes"]:
          if str(elem_result.get("hero_id")) == elem_heroes["hero_id"]:
            players_info['hero'] = elem_heroes.get("hero_name")
          else:
            pass
        players_info['kills'] = elem_result.get("kills")
        players_info['deaths'] = elem_result.get("deaths")
        players_info['assists'] = elem_result.get("assists")
        data_players_radiant.append(players_info)
      elif elem_result.get("team_number") == 1: #Если игрок находится на стороне сил тьмы // If the player is on the dire side
        players_info = dict()
        for elem_heroes in heroes["heroes"]:
          if str(elem_result.get("hero_id")) == elem_heroes["hero_id"]:
            players_info['hero'] = elem_heroes.get("hero_name")
          else:
            pass
        players_info['kills'] = elem_result.get("kills")
        players_info['deaths'] = elem_result.get("deaths")
        players_info['assists'] = elem_result.get("assists")
        data_players_dire.append(players_info)
      else:
        pass

    

    #Отправка ботом сообщения с информацией о матче // Bot sending a message with information about a match
    if data_win: #Победа сил света // Radiant match-win 
      await message.answer(f'''🏆Силы света [{data_radiant_score}:{data_dire_score}] Силы тьмы 
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
      await message.answer(f'''Силы света [{data_radiant_score}:{data_dire_score}] Силы тьмы🏆
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
      
    os.remove(f'{message.text}.json') #Удаление ранее полученного json-файла // Deleting a previously received json file

  except:
    pass


#Обработка команд /findplayer и /findaccount // Handling the /findplayer and /findaccount commands
@router.message(Command('findplayer'))
async def command_findplayer_handler(message, state: FSMContext):
  await state.set_state(Form.account_id)
  await message.answer('Введите ID игрока')

@router.message(Form.account_id)
async def get_account_data(message, state: FSMContext):
  await state.update_data(account_id=message.text)
  try:
    resp = requests.get(f'https://api.opendota.com/api/players/{message.text}') #Отправка запроса на opendota.com API // Sending a request to the opendota.com API
    response = resp.json()

    with open(f'{message.text}.json', 'w') as outfile:
      json.dump(response, outfile) #Сохранение полученного json-файла // Saving received json-file

    with open(f'{message.text}.json', 'r') as outfile:
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
      await message.answer_photo(data_avatarfull, caption=f'''ID аккаунта: {data_account_id}\nSteam ID: {data_steamid}\nНикнейм: {data_personaname}
Ранг: {data_player_rank}''')
    else:
      await message.answer_photo(data_avatarfull, caption=f'''ID аккаунта: {data_account_id}\nSteam ID: {data_steamid}\nНикнейм: {data_personaname}
Страна: {data_country}
Ранг: {data_player_rank}''')

    os.remove(f'{message.text}.json') #Удаление ранее полученного json-файла // Deleting a previously received json file

  except:
    pass


async def main():
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    dp.include_router(router)

    # Start event dispatching
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())