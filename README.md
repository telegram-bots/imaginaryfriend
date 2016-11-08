My great plan is to create a Telegram chat bot that would be like [shizoid](https://github.com/top4ek/shizoid), but in Python and maybe with some extra features.

#### Dependencies
* `python >= 3.5.2`
* `python-telegram-bot==5.2.0`
* `orator==0.9.2`

#### Setup
1. Install dependencies with PIP
2. Rename `main.cfg.example` to `main.cfg`, set `bot` and `db` properties
3. Execute command `orator migrate -c db.py` to create database and required tables
4. Run the `run.py` using python