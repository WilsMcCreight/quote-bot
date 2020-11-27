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

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"Hi {member.name}, welcome to the Discord server! I'm Quote Bot, I'm used to log funn or memorable quotes made during D&D sessions. Mention me with the @ symbol followed by the word help ('@Quote Bot help') and I'll give you examples for interacting with me!"
    )

@client.event
async def on_message(message):
    print(message.author)
    if message.author == client.user:
        return
    if(message.content.startswith(BOT_ID)):
        print("Quote Bot was mentioned")
        text = message.content[len(BOT_ID):].strip()
        if text.lower().startswith('help') and len(text) == 4:
            print('Responding with help message')
        # if text.split()[0].lower() == 'help':
            await message.channel.send("""Hi, I'm Quote Bot! You can use me to log quotes into a database from which they can be retrieved later. The general quote logging format is as follows:
            1. Quote Bot mention
            2. Quote (Surrounded by quotation marks ("))
            3. Hyphen separator (Optional)
            4. Context (Which must always start with the quotee's name)

            An example would be:    @Quote Bot "Eatin ass and eatin ass" - Triggs referring to a canibal orgy
            Or without the hyphen:  @Quote Bot “My therapist told me not to kink shame so I won’t” SJ in reference to D&D citizens being attracted to brogmir and a lot of other stuff
            
            You can also log a quick quote by simply mentioning Quote Bot and following that with a quote. 

            For example:    @Quote Bot Brogmir have arm, Brogmir is happy
            Or:             @Quote Bot "Brogmir lost arm, Brogmir is sad"

            These examples will forego the metadata of the quotee's name and the quote's context.

            Ways to retreive quotes and visualize them are underway, stay tuned for more functionality and feel free to send any ideas or feedback to Wils!
            """)
        else:
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
                quotee_name = meta_data[0]
                context = (" ").join(meta_data)
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