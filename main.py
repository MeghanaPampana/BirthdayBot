from typing import Final
import os
from dotenv import load_dotenv
import discord
from discord.ext import commands
from datetime import datetime

load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

birthdays = {}

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command(name='helpMe', description='Provides information about available commands')
async def help(ctx):
    await ctx.send('Available commands: add_birthday, remove_birthday, update_birthday, list_birthdays')

@bot.command(name='add_birthday', description='Add a birthday to the list')
async def birthday(ctx, user: discord.Member, date: str):
    try:
        date = datetime.strptime(date, '%d/%m/%Y')
        birthdays[user.name] = date
        await ctx.send(f'Added {user.display_name}\'s birthday: {date.strftime("%d/%m/%Y")}')
    except ValueError:
        await ctx.send('Invalid date format. Please use DD/MM/YYYY.')

@bot.command(name='remove_birthday', description='Remove a birthday from the list')
async def remove_birthday(ctx, user: discord.Member):
    if user.name in birthdays:
        del birthdays[user.name]
        await ctx.send(f'Removed {user.display_name}\'s birthday.')
    else:
        await ctx.send(f'{user.display_name} is not in the birthday list.')

@bot.command(name='update_birthday', description='Update a birthday in the list')
async def update_birthday(ctx, user: discord.Member, date: str):
    try:
        date = datetime.strptime(date, '%d/%m/%Y')
        birthdays[user.name] = date
        await ctx.send(f'Updated {user.display_name}\'s birthday: {date.strftime("%d/%m/%Y")}')
    except ValueError:
        await ctx.send('Invalid date format. Please use DD/MM/YYYY.')

@bot.command(name='list_birthdays', description='Lists all birthdays')
async def list_birthdays(ctx):
    if birthdays:
        birthday_list = '\n'.join([f'{member}: {date.strftime("%d/%m/%Y")}' for member, date in birthdays.items()])
        await ctx.send(f'Birthdays:\n{birthday_list}')
    else:
        await ctx.send('No birthdays in the list.')

sent_message = False

@bot.event
async def on_message(message):
    global sent_message

    if message.author == bot.user:
        return

    current_date = datetime.now()
    for member, date in birthdays.items():
        if date.month == current_date.month and date.day == current_date.day:
            if not sent_message:
                guild = message.guild
                member_obj = guild.get_member_named(member)
                if member_obj:
                    await message.channel.send(f'Happy birthday, {member_obj.display_name}!')
                else:
                    await message.channel.send(f'Happy birthday, {member}!')
                sent_message = True

    await bot.process_commands(message)
                
bot.run(TOKEN)