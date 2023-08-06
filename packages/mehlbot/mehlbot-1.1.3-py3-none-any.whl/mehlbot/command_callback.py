"""The command processor.

Contains methods to process the Commands in command.py.
"""
import discord

from mehlbot.command import Command
from mehlbot.logger import setup_logger


logger = setup_logger(__name__)


async def process_command(client: discord.Client, commands: dict[str, Command], message: discord.Message) -> bool:
    """Processes the message with the given commands. For usage see the.

    /example directory.

    :param client: discord.Client
    :param commands: bot_commands, unless using custom commands storage.
    :param message: received message.
    :return: True if message is command
    """
    message_content = message.content.strip()
    command_name: str

    # Check if command name matches with one of the given commands and argument amount.
    # (special case for var args, only needs matching message begin)
    for command_name, command in commands.items():
        entered_command_keys = message_content.split(" ")
        command_keys = command_name.split(" ")

        if not await method_name(command, command_keys, entered_command_keys):
            continue

        provided_argument_amount = len(entered_command_keys) - len(command_keys)
        allowed_args_matches = False
        num_args = [command.allowed_num_args[0]]
        # Check if any possible variation of the args amount match
        # See complex example.
        for allowed_args in command.allowed_num_args:
            if len(allowed_args) == provided_argument_amount:
                allowed_args_matches = True
                num_args.append(allowed_args)

        # If the command args amount don't match (and not var args)
        # then print incorrect usage of the given command.
        if not allowed_args_matches and not command.var_args:
            if len(command.allowed_num_args[0]) > 0:
                output = "\n"
                for allowed_args in command.allowed_num_args:
                    output += f"> `{command.command_name} <"
                    output += ">, <".join(allowed_args) + ">`\n"
            else:
                output = f"{command.command_name}"

            channel_msg = f"Incorrect command usage: {output}"
            logger.info(channel_msg)
            await message.channel.send(channel_msg)
            continue

        args = entered_command_keys[len(command_keys) :]

        # Extract var args from message
        if command.var_args:
            if len(num_args) > 1:
                channel_msg = f"Command {command_name} is ambiguous because of var args and multiple command args."
                logger.error(channel_msg)
                await message.channel.send(channel_msg)
                return False
            var_args_pos = len(command_keys) + len(num_args[0])
            args = entered_command_keys[len(command_keys) : var_args_pos] + [
                " ".join(entered_command_keys[var_args_pos:]),
            ]

        await command.callback(message, client, args)
        return True
    return False


async def method_name(command: Command, command_keys: list[str], entered_command_keys: list[str]):
    """Check if the command matches any.

    :param command:
    :param command_keys:
    :param entered_command_keys:
    :return:
    """
    matches = True
    for idx, _command_key in enumerate(command_keys):
        if idx >= len(entered_command_keys) and not command.var_args:
            break
        if command_keys[idx] != entered_command_keys[idx]:
            matches = False
            break
    return matches
