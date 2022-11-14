import discord
import os
from os import listdir
from discord.ext import bridge, commands
from plyer import notification

intents = discord.Intents.default()
intents.message_content = True

bot = bridge.Bot(command_prefix="!", intents=intents)
bot.remove_command("help")


#Bot events
#----------------------------------------------------------------------------------------------
#When bot is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    notification.notify(
        title = 'Bot is online baka',
        message = 'Bot is online baka',     
        timeout = 10,
    )

#Before application command runs
@bot.event
async def on_application_command(ctx):
    await ctx.defer()

#On application command completion
@bot.event
async def on_application_command_completion(ctx):
    print(ctx.command, ctx.author)

#Before prefixed command runs
@bot.event
async def on_command(ctx):
    await ctx.defer()

#On prefixed command completion
@bot.event
async def on_command_completion(ctx):
    print(ctx.command, ctx.author)
#----------------------------------------------------------------------------------------------

#developer check
def if_dev_check(ctx):
    return ctx.message.author.id == 924096612941299762

#Developer only commands
class developer(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @bridge.bridge_command()
    @commands.check(if_dev_check)
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}')
        print(f'Loaded {extension}')

    @bridge.bridge_command()
    @commands.check(if_dev_check)
    async def unload(self, ctx, extension):
        bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension}')
        print(f'Unloaded {extension}')

    @bridge.bridge_command()
    @commands.check(if_dev_check)
    async def reload(self, ctx, extension):
        bot.unload_extension(f'cogs.{extension}')
        bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension}')
        print(f'Reloaded {extension}')

    @bridge.bridge_command()
    @commands.check(if_dev_check)
    async def restart(self, ctx):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                bot.reload_extension(f"cogs.{filename[:-3]}")

#Adds the developer cog included inside main.py
def setup(bot):
    try:
        bot.add_cog(developer(bot))
    except:
        print("Could not load, could be missing a setup function or not intended as a cog. File: " + filename)

bot.add_cog(developer(bot))

#Loads all the cogs in the cogs folder
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print("loaded " + filename)
        except:
            print("Could not load, could be missing a setup function or not intended as a cog. File: " + filename)

bot.run("TOKEN")