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

class Progress:
    def __init__(self, progress):
        self.progress = progress

    def set_progress(self, new_val):
        self.progress = new_val

    def get_progress(self):
        return self.progress
currentProgress = Progress(False)

class ExistingId:
    def __init__(self, existId):
        self.existId = existId

    def add_extId(self, new_val):
        self.existId.append(new_val)

    def set_extId(self, new_val):
        self.existId = new_val

    def get_extId(self):
        return self.existId
existing_ids = ExistingId([])

@bot.event
async def on_ready():
    print(f'{bot.user.name} connected!')

@bot.command(name='submit', pass_context=True, help='Submit drawing image!')
async def submit(ctx):
  if currentProgress.get_progress():
    id = ctx.message.author.id
    mention = ctx.message.author.mention
    if id in existing_ids.get_extId(): await ctx.send("Cannot submit more than once! " + str(mention))
    # elif IN_PROGRESS==False: await ctx.send("Game hasn't started, not submitted. " + str(mention))
    else:
        try:
            url = ctx.message.attachments[0].url            # check for an image, call exception if none found
        except IndexError:
            print("Error: No attachments")
            await ctx.send("No attachments detected!")
        else:
            if url[0:26] == "https://cdn.discordapp.com" or url[0:28] == "https://media.discordapp.net":   # look to see if url is from discord
                r = requests.get(url, stream=True)
                # imageName = str(uuid.uuid4()) + '.jpg'      # uuid creates random unique id to use for image names
                imageName = str(id) + '.jpg'
                if not os.path.exists('submissions'):
                    os.makedirs('submissions')
                with open('submissions/' + imageName, 'wb') as out_file:
                    print('Saving image: ' + imageName)
                    shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)  TODO save images to designated directory with their username!
                await ctx.send('Submitted by '+ str(mention) + ' !')
                existing_ids.add_extId(id)
  else:
      await ctx.send('Submission is currently closed.')


@bot.command(name='start', help='Starts a random prompt for drawing. Use: .start <time in seconds for challenge')
async def start(ctx, time):
    prompt = random.choice(PROMPTS)
    existing_ids.set_extId([])
    currentProgress.set_progress(True);
    await ctx.send("The prompt is: "+ prompt)
    await asyncio.sleep(int(time))
    currentProgress.set_progress(False);
    await ctx.send("Time is up!")
    # compare all the images with ai probability. The highest probability wins
    # clear directory
    existing_ids.set_extId([])
    shutil.rmtree('submissions/', ignore_errors=False, onerror=None)

bot.run(TOKEN)