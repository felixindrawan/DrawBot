# bot.py
import os
import asyncio
import random
from discord.ext import commands
import uuid
import requests
import shutil
# import the ai algorithm
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

PROMPTS = ["CAT", "DOG", "CLOCK"]
IN_PROGRESS = False

bot = commands.Bot(command_prefix='.')

@bot.event
async def on_ready():
    print(f'{bot.user.name} connected!')

existing_ids = [] # TODO i dont think this logic actually works
@bot.command(name='submit', pass_context=True, help='Submit drawing image!')
async def submit(ctx):
    id = ctx.message.author.id
    mention = ctx.message.author.mention
    if id in existing_ids: await ctx.send("Cannot submit more than once! " + str(mention))
    # elif IN_PROGRESS==False: await ctx.send("Game hasn't started, not submitted. " + str(mention))
    else:
        existing_ids.append(id)
        try:
            url = ctx.message.attachments[0].url            # check for an image, call exception if none found
        except IndexError:
            print("Error: No attachments")
            await ctx.send("No attachments detected!")
        else:
            if url[0:26] == "https://cdn.discordapp.com":   # look to see if url is from discord
                r = requests.get(url, stream=True)
                # imageName = str(uuid.uuid4()) + '.jpg'      # uuid creates random unique id to use for image names
                imageName = str(id) + '.jpg'
                with open(imageName, 'wb') as out_file:
                    print('Saving image: ' + imageName)
                    shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)  TODO save images to designated directory with their username!
                await ctx.send('Submitted by '+ str(mention) + ' !')

@bot.command(name='start', help='Starts a random prompt for drawing. Use: .start <time in seconds for challenge')
async def start(ctx, time):
    prompt = random.choice(PROMPTS)
    await ctx.send("The prompt is: "+ prompt)
    await asyncio.sleep(int(time))
    await ctx.send("Time is up!")
    
    # compare all the images with ai probability. The highest probability wins
     
    # clear directory
    existing_ids = []


bot.run(TOKEN)