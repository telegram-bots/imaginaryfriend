My great plan is to create a Telegram chat bot that would be like [shizoid](https://github.com/top4ek/shizoid), but in Python and maybe with some extra features.

A-a-a-a-and... it works! Thanks to [@REDNBLACK](https://github.com/REDNBLACK).

## Features

ImaginaryFriend can:

* reply to random messages in chat groups,
* reply to replies to its messages / messages mentioning it,
* send (one!) sticker ("I'm frustrated by all these stickers"),
* do some commands.

### Commands

* `/ping`,
* `/get_stats`: get information on how many pairs are known by ImaginaryFriend,
* `/set_chance`: set the probability that ImaginaryFriend would reply to a random message (must be in range 1-50, default: 5),
* `/get_chance`: get current probability that ImaginaryFriend would reply to a message.

## Installation and Setup

### Dependencies
* `python >= 3.5.2`
* `python-telegram-bot==5.2.0`
* `orator==0.9.2`

### Setup
1. Install dependencies with PIP
2. Rename `main.cfg.example` to `main.cfg`, set `bot` and `db` properties
3. Execute command `orator migrate -c db.py` to create database and required tables
4. Run the `run.py` using python
