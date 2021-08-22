# bot.py
import os
import asyncio
import random
from discord.ext import commands
from discord.utils import get
import uuid
import requests
import shutil
# import the ai algorithm
import Prediction

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv('TOKEN')
GUILD = os.getenv('GUILD')

# get prompts
def readFile(fileName):
    fileObj = open(fileName, "r")  # opens the file in read mode
    words = fileObj.read().splitlines()  # puts the file into an array
    fileObj.close()
    return words

PROMPTS = readFile('categories.txt')

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

    def add_extId(self, new_val, new_mention):
        self.existId.append([new_val, new_mention])

    def set_extId(self, new_val):
        self.existId = new_val

    def get_extUser(self):
        return self.existId

existing_ids = ExistingId([])

class FileSubmissions:
    def __init__(self, files):
        self.files = files

    def add_files(self, new_val):
        self.files.append(new_val)

    def set_files(self, new_val):
        self.files = new_val

    def get_files(self):
        return self.files
submittedFiles = FileSubmissions([])

class DrawingScores:
    def __init__(self, scores):
        self.scores = scores
    def add_score(self,score):
        self.scores.append(score)
    def set_score(self,val):
        self.scores = val
    def get_store(self):
        return self.scores
drawingScores = DrawingScores([])

@bot.event
async def on_ready():
    print(f'{bot.user.name} connected!')

@bot.command(name='submit', pass_context=True, help='Submit drawing image!')
async def submit(ctx):
  if currentProgress.get_progress():
    id = ctx.message.author.id
    mention = ctx.message.author.mention
    if [id, mention] in existing_ids.get_extIds(): await ctx.send("Cannot submit more than once! " + str(mention))
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
                imageName = str(id) + '.png'
                submittedFiles.add_files(imageName)
                if not os.path.exists('submissions'):
                    os.makedirs('submissions')
                with open('submissions/' + imageName, 'wb') as out_file:
                    print('Saving image: ' + imageName)
                    shutil.copyfileobj(r.raw, out_file)     # save image (goes to project directory)  TODO save images to designated directory with their username!
                await ctx.send('Submitted by '+ str(mention) + ' !')
                existing_ids.add_extId(id,mention)
  else:
      await ctx.send('Submission is currently closed.')


@bot.command(name='start', help='Starts a random prompt for drawing. Use: .start <time in seconds for challenge')
async def start(ctx, time):
    if (currentProgress.get_progress()):
        await ctx.send('There is a quiz currently going on')
        return

    prompt = random.choice(PROMPTS)
    if os.path.exists('submissions'):
        shutil.rmtree('submissions/', ignore_errors=False, onerror=None)
    existing_ids.set_extId([])
    submittedFiles.set_files([])
    currentProgress.set_progress(True);
    await ctx.send("The prompt is: "+ prompt)
    await asyncio.sleep(int(time))
    currentProgress.set_progress(False);
    await ctx.send("Time is up!")
    # compare all the images with ai probability. The highest probability wins
    users = existing_ids.get_extIds()
    for i in range(len(users)):
        id = users[i][0]
        mention = users[i][1]
        ret = Prediction.Predict(str(id)+".png")
        print(ret)
        label = ret[0]
        prob = ret[1]
        user = get(bot.get_all_members(), id=id)
        print(user)
        probability = prob*100
        strProb =  ": Your drawing is {probability: .2f}% paper_clip".format(probability=probability)
        await ctx.send(strProb)
    # clear directory
    existing_ids.set_extId([])




bot.run(TOKEN)