import discord
from mehlbot.command import Command
from mehlbot.logger import setup_logger

logger = setup_logger(__name__)


async def process_command(client, commands: dict[str, Command], message: discord.Message) -> bool:
    message_content = message.content.strip()

    command_name: str
    for command_name, command in commands.items():
        entered_command_keys = message_content.split(" ")
        matches = True
        command_keys = command_name.split(" ")
        for idx, command_key in enumerate(command_keys):
            if idx >= len(entered_command_keys) and not command.var_args:
                break
            if command_keys[idx] != entered_command_keys[idx]:
                matches = False
                break

        if not matches:
            continue

        provided_argument_amount = len(entered_command_keys) - len(command_keys)
        matches = False
        num_args = [command.allowed_num_args[0]]
        for allowed_args in command.allowed_num_args:
            if len(allowed_args) == provided_argument_amount:
                matches = True
                num_args.append(allowed_args)

        if not matches and not command.var_args:
            if len(command.allowed_num_args[0]) > 0:
                output = f"\n"
                for allowed_args in command.allowed_num_args:
                    output += f"> `{command.command_name} <"
                    output += ">, <".join(allowed_args) + ">`\n"
            else:
                output = f"{command.command_name}"

            channel_msg = f"Incorrect command usage: {output}"
            logger.info(channel_msg)
            await message.channel.send(channel_msg)
            continue

        args = entered_command_keys[len(command_keys):]
        if command.var_args:
            if len(num_args) > 1:
                channel_msg = f"Command {command_name} is ambiguous because of var args and multiple command args."
                logger.error(channel_msg)
                await message.channel.send(channel_msg)
                return False
            var_args_pos = len(command_keys) + len(num_args[0])
            args = entered_command_keys[len(command_keys):var_args_pos] + [
                " ".join(entered_command_keys[var_args_pos:])]

        await command.callback(message, client, args)
        return True
    return False
