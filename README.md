My great plan is to create a Telegram chat bot that would be like [shizoid](https://github.com/top4ek/shizoid), but in Python and maybe with some extra features.

A-a-a-a-and... it works! Thanks to [@REDNBLACK](https://github.com/REDNBLACK). 

## Features

ImaginaryFriend can:

* reply to random messages in chat groups,
* reply to replies to its messages / messages mentioning it,
* send (one!) sticker ("I'm frustrated by all these stickers"),
* detect repeating media files and send [:||||||||||||:] to chat,
* do some commands.

### Examples

```
– @ImaginaryFriendBot один ты меня понимаешь
– Ты глупый кот. Меня зовут антон иванов, мне только что поймала ту же пустоту.
– привет, Антон
– Привет!
– оч приятно, Антон. Я Боря
– Я не знаю юридических тонкостей но по факту квартира же твоя! Боря кот. Оч приятно антон.
– Чем ты занимаешься, ты юрист?
– Ты не видишь чтоль?
– Ну извини, решил уточнить. Как дела то?
– Как дела с потоками в яве обстоят? Ну ты понел. Дела отлично, а твои как?
```

```
– Нет. У меня друг в дестве кусался.
– он тебя загрыз?
– Он же говна кусок.
– тебя загрыз кусок говна?
– Тебя наверх задрать надо.
– ты сегодня особо в тему пишешь, что с тобой, ты поумнел?
– Что бы крашилось :3?
– да ты суицидник XD
– Ты не очень умный?
– годный бот
– Бот захватит мир.
```

## Commands

* `/ping`: you know the drill,
* `/get_stats`: get information on how many pairs are known by ImaginaryFriend,
* `/chance n`: set the probability that ImaginaryFriend would reply to a random message (must be in range 1-50, default: 5),
* `/сhance`: get current probability that ImaginaryFriend would reply to a message,
* `/mod_f pattern`: find all the words starting with pattern,
* `/mod_d word`: remove word from ImaginaryFriend's dictionary,
* `/meow`, `/woof`, `/borscht`, `/boobs`, `/butts` and others: make ImaginaryFriend send a corresponding picture,
* `/vzhuh phrase`: make ImaginaryFriend create a [_вжух_ meme](https://vk.com/vzhuhcat).

## Installation and Setup

### Setup using Docker
1. Install [Docker](https://store.docker.com/search?offering=community&type=edition)
2. Rename `main.cfg.example` to `main.cfg`
3. Talk to [@botfather](https://telegram.me/botfather) and create your own bot.
4. Open `main.cfg` file in text editor and paste your newly created bot token into `bot`.`token` property
5. Execute `docker-compose up`
6. Congrats! You now have ImaginaryFriend of your own!

## Setup without Docker
1. Install [Python >= 3.5.2](https://www.python.org/downloads/)
2. Install [Redis >= 3.2](https://redis.io/download)
3. Install dependencies with PIP by executing command `pip install -r requirements.txt`
4. Talk to [@botfather](https://telegram.me/botfather) and create your own bot.
5. Open `main.cfg` file in text editor and paste your newly created bot token into `bot`.`token` property
6. (Optionally) Configure `updates` property for websocket support
7. Execute the `python run.py`
