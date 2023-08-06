import discord

bot_commands = {}


class Command:
    command_name: str = ""
    callback = None
    allowed_num_args: list[[str]] = []
    description: str = ""
    var_args: bool = False


def add_command(command_name: str, callback, allowed_num_args: list[[str]], description="", var_args=False):
    global bot_commands
    cmd = Command()
    cmd.command_name = command_name
    cmd.callback = callback
    cmd.allowed_num_args = allowed_num_args
    cmd.description = description
    cmd.var_args = var_args
    bot_commands[command_name] = cmd


async def _help(message: discord.Message, client, args):
    global bot_commands
    msg = "Available commands: ```yaml\n"
    for name, command in bot_commands.items():
        if name == "help":
            continue
        msg += f'"{name}":'.ljust(20, " ")
        msg += f'{command.description}\n'

    if len(bot_commands) <= 1:
        msg += "This bot has no commands.\n"

    msg += "```"
    await message.channel.send(msg)


add_command("help", _help,
            allowed_num_args=[[]],
            description="This prints all commands.")
