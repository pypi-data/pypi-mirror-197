<a href="https://raw.github.com/cobrapitz/MehlBot/master/docs/badges/interrogate-badge.svg"><img alt="PyPI" src="https://raw.github.com/cobrapitz/MehlBot/master/docs/badges/interrogate-badge.svg"></a>
<a href="https://github.com/cobrapitz/MehlBot/blob/master/LICENSE"><img alt="PyPI" src="https://img.shields.io/github/license/cobrapitz/mehlbot"></a>
<a href="https://github.com/cobrapitz/MehlBot"><img alt="PyPI" src="https://img.shields.io/badge/mehl-bot-f39f37"></a>
<a href="https://pypi.org/project/mehlbot/"><img alt="PyPI" src="https://img.shields.io/pypi/v/mehlbot"></a>
<a href='https://mehlbot.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/mehlbot/badge/?version=latest' alt='Documentation Status' /></a>


[//]: # (<a href="https://github.com/psf/black"><img alt="PyPI" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>)
[//]: # (<a href="https://pypi.org/project/mehlbot/"><img alt="PyPI" src="https://img.shields.io/badge/mehl-bot-f39f37"></a>)
[//]: # (![t]&#40;https://app.codecov.io/gh/cobrapitz/mehlbot&#41;)
[//]: # ([![security: bandit]&#40;https://img.shields.io/badge/security-bandit-yellow.svg&#41;]&#40;https://github.com/PyCQA/bandit&#41;)
[//]: # (![example workflow]&#40;https://github.com/github/docs/actions/workflows/main.yml/badge.svg&#41;)

# MehlBot

MehlBot is a Discord bot that responds to commands by executing (callback) functions.

It's built around the `discord.Client` class.
This allows an easy integration to existing bots and creation of new bots. 

Documentation: [docs](https://mehlbot.readthedocs.io/en/latest/)

See [examples/hellow_bot.py](./examples/hello_bot.py) for full source code.
```Python
# imports ... 

class HelloBot(discord.Client):  # discord.Client class

    def __init__(self, intents: Intents, **options) -> None:
        super().__init__(intents=intents, **options)

    async def on_ready(self) -> None:  # Gets called when bot is ready/started
        print("Bot started.")

    async def on_message(self, message: Message):
        if message.author == self.user:  # skip if message's author is the bot
            return

        # necessary callback command
        # bot_commands are in mehlbot.command
        command_found = await command_callback.process_command(self, bot_commands, message)

        # prefix with command if message is command
        log_msg = "" if not command_found else "command: "
        log_msg += f"{message.author.nick} ({message.author.name}): '{message.content}'"
        print(log_msg)


def main():
    hello_bot = HelloBot(discord.Intents.all())  # discord intents
    with Path("token.txt").open() as file:  # load token form file (.gitignore) or use env
        token = file.read()
    hello_bot.run(token)
```


- - - 
### Dev 

- `poetry run task --list` to show all defined tasks to run. (run task with: `poetry run task <task>`)
- note `make html` -> rst files copy into source folder, otherwise moduels not found

[//]: # (- `pre-commit install` should always be the first thing you do.)

