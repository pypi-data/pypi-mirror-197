"""Contains Command class and bot commands as a global variable.

Also adds 'help' to print all added commands to bot_commands.
"""
from collections.abc import Callable
from typing import List

import discord


bot_commands = {}


class Command:
    """The Commands class, that contains the data needed for a discord
    command."""

    command_name: str = ""
    callback: Callable
    allowed_num_args: List[List[str]] = []
    description: str = ""
    var_args: bool = False


def add_command(
    command_name: str,
    callback: Callable,
    allowed_num_args: List[List[str]],
    description: str = "",
    var_args: None | bool = None,
):
    """The interface/method to add commands to the bot. 'help' command gets
    added when importing this module.

    A basic example to add a command can be seen here:

    # called with "next". No args allowed/required.
    add_command("next",
                _next,
                allowed_num_args=[[]],
                description="This plays the next song in the current playlist."
    )

    A more complex example is the following:

    # This either requires 1 argument or 2 arguments.
    # The described command removes a song,
    # or when called with 2 arguments, it removes the song from the given playlist.
    add_command("remove",
                _remove,
                allowed_num_args=[["song_name"], ["playlist", "song_name"]],
                description="Removes selected song from chosen playlist."
    )

    :param command_name: name of the command, doesn't require any prefix.
    :param callback: the function that gets called when the command is invoked.
    :param allowed_num_args: array of string-arrays containing the argument name. See example can be seen above.
    :param description: optional description to the command
    :param var_args: allow multiple (unnamed) arguments
    :return:
    """
    if var_args is None:
        var_args = False
    cmd = Command()
    cmd.command_name = command_name
    cmd.callback = callback
    cmd.allowed_num_args = allowed_num_args
    cmd.description = description
    cmd.var_args = var_args
    bot_commands[command_name] = cmd


async def _help(message: discord.Message, _client: discord.Client, _args: list) -> None:
    """Replies/sends every command to the user's channel.

    :param message: received discord message
    :param _client: client
    :param _args: received arguments
    :return: None.
    """
    msg = "Available commands: ```yaml\n"
    for name, command in bot_commands.items():
        if name == "help":
            continue
        msg += f'"{name}":'.ljust(20, " ")
        msg += f"{command.description}\n"

    if len(bot_commands) <= 1:
        msg += "This bot has no commands.\n"

    msg += "```"
    await message.channel.send(msg)


add_command("help", _help, allowed_num_args=[[]], description="This prints all commands.")
