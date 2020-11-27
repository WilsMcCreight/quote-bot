# # bot.py
# import os
# import random

# from discord.ext import commands
# from dotenv import load_dotenv
# import pandas as pd
# import sqlite3

# from db_control import connect_db, insert_quote


# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

# bot = commands.Bot(command_prefix='!')

# # bot = commands.Bot(command_prefix=when_mentioned)

# @bot.command(when_mentioned)
# async def test(ctx, arg):
#     if arg == "ppp":
#         print("IT WORKED")
#     print("IT MIGHT HAVE WORKED")



# @bot.command(name='99', help='Responds with a random quote from Brooklyn 99')
# async def nine_nine(ctx):
#     brooklyn_99_quotes = [
#         'I\'m the human form of the 💯 emoji.',
#         'Bingpot!',
#         (
#             'Cool. Cool cool cool cool cool cool cool, '
#             'no doubt no doubt no doubt no doubt.'
#         ),
#     ]

#     response = random.choice(brooklyn_99_quotes)
#     await ctx.send(response)

# @bot.command(name='q', help='Saves a quote to the quote book')
# async def save_quote(ctx, *, arg):
#     print(arg)
#     await ctx.send('Ayo')

# @bot.command(name='quote', help='Saves a quote to the quote book')
# async def save_quote_(ctx):
#     await ctx.send('Ayo')

# @bot.command()
# async def save_quote__(ctx, arg):
#     if arg == "ppp":
#         print("IT WORKED")
#     pass

# @bot.command(name='roll', help='Simulates rolling dice.')
# async def roll(ctx, number_of_dice: int, number_of_sides: int):
#     dice = [
#         str(random.choice(range(1, number_of_sides + 1)))
#         for _ in range(number_of_dice)
#     ]
#     await ctx.send(', '.join(dice))

# bot.run(TOKEN)




# # bot.py
# import os
# import random

# from discord.ext import commands
# from dotenv import load_dotenv

# load_dotenv()
# TOKEN = os.getenv('DISCORD_TOKEN')

# bot = commands.Bot(command_prefix='!')

# @bot.command(name='99')
# async def nine_nine(ctx):
#     brooklyn_99_quotes = [
#         'I\'m the human form of the 💯 emoji.',
#         'Bingpot!',
#         (
#             'Cool. Cool cool cool cool cool cool cool, '
#             'no doubt no doubt no doubt no doubt.'
#         ),
#     ]

#     response = random.choice(brooklyn_99_quotes)
#     await ctx.send(response)

# bot.run(TOKEN)








# bot.py
import os
import discord
from dotenv import load_dotenv

from db_control import connect_db, insert_quote, insert_quote_small

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
BOT_ID = os.getenv('BOT_MENTION_ID')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

# @client.event
# async def on_member_join(member):
#     await member.create_dm()
#     await member.dm_channel.send(
#         f'Hi {member.name}, welcome to my Discord server!'
#     )

@client.event
async def on_message(message):
    print(message.author)
    if message.author == client.user:
        return
    if(message.content.startswith(BOT_ID)):
        print("Quote Bot was mentioned")
        text = message.content[len(BOT_ID):].strip()
        if text.startswith('help'):
            await message.channel.send("""Hi, I'm Quote Bot! You can use me to log quotes into a database from which they can be retrieved later. The general quote logging format is as follows:
            1. Quote Bot mention
            2. Quote (Surrounded by quotation marks ("))
            3. Hyphen separator (Optional)
            4. Quotee name
            5. Context

            An example would be:    @Quote Bot "Eatin ass and eatin ass" - Triggs referring to a canibal orgy
            Or without the hyphen:  @Quote Bot “My therapist told me not to kink shame so I won’t” SJ in reference to D&D citizens being attracted to brogmir and a lot of other stuff
            
            You can also log a quick quote by simply mentioning Quote Bot and following that with a quote. 

            For example:    @Quote Bot Brogmir have arm, Brogmir is happy
            Or:             @Quote Bot "Brogmir lost arm, Brogmir is sad"

            These examples will forego the metadata of the quotee's name and the quote's context.

            Ways to retreive quotes and visualize them are underway, stay tuned for more functionality and feel free to send any ideas or feedback to Wils!
            """)

        quote_indices = [i for i, ltr in enumerate(text) if ltr == '"']

        if len(quote_indices) == 0:
            text = '"' + text + '"'
            print("Inserting a small quote:", text)
            if message.author.nick:
                log_quote((message.author.nick, text), insert_quote_small)
            else:
                log_quote((message.author.name, text), insert_quote_small)

        elif len(quote_indices)%2 != 0:
            await message.channel.send('Sorry, the number of quotation marks (") was odd. Not sure how to parse that quote.')

        else:
            print("Inserting a big quote:", text)
            if message.author.nick:
                author_name = message.author.nick
            else:
                author_name = message.author.name
            quote_text = text[quote_indices[0]:quote_indices[-1]+1]
            meta_data = text[quote_indices[-1]+1:]
            meta_data = meta_data.strip()
            if meta_data[0] == '-':
                meta_data = meta_data[1:].strip()
            meta_data = meta_data.split()
            print("SPlit meta_data:", meta_data)
            quotee_name = meta_data[0]
            context = (" ").join(meta_data)
            # print('quote_text:', quote_text)
            # print('meta_data:', meta_data)
            log_quote((author_name, quotee_name, quote_text, context), insert_quote)



def log_quote(quote, insert_func):
    conn = connect_db('Quote.db')
    if (not conn):
        print('Bot failed to connect to database, exiting')
    else:
        curs = conn.cursor()
        insert_func(conn, curs, quote)
        conn.close()    

client.run(TOKEN)