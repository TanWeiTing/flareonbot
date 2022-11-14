<<<<<<< Updated upstream
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

=======
import discord
import os
from os import listdir
from discord.ext import bridge, commands
from plyer import notification

intents = discord.Intents.default()
intents.message_content = True

bot = bridge.Bot(command_prefix=",", intents=intents)

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
    print(f"{ctx.author} Has used command: {ctx.command}")

#Before prefixed command runs
@bot.event
async def on_command(ctx):
    await ctx.defer()

#On prefixed command completion
@bot.event
async def on_command_completion(ctx):
    print(f"{ctx.author} Has used command: {ctx.command}")

#On command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
            message = f"This command is on cooldown. Please try again after {round(error.retry_after, 1)} seconds. Error:CommandOnCooldown"
    elif isinstance(error, commands.MissingPermissions):
            message = "You are missing the required permissions to run this command! Error:MissingPermissions"
    elif isinstance(error, commands.MissingRequiredArgument):
            message = f"Missing a required argument: {error.param} Error:MissingRequiredArgument"
    elif isinstance(error, commands.CommandNotFound):
            message = f" Uh oh, command does not exist! Try `,help` for a list of commands. Error:CommandNotFound"
    elif isinstance(error, commands.ConversionError):
            message = f"Uh oh, I can't convert that to a number! Try again. Error:ConversionError)"
    elif isinstance(error, commands.CheckFailure):
            message = "You don't have the required permissions to run this command! Error:CheckFailure"
    elif isinstance(error, commands.CommandInvokeError):
            message = "Something went wrong while running the command! Error:CommandInvokeError"
    elif isinstance(error, commands.UserInputError):
            message = "Invalid input! Error:UserInputError"
    elif isinstance(error, commands.NoPrivateMessage):
            message = "This command cannot be used in DMs!"
    else:
            message = "Something went wrong!"

    await ctx.send(message)

#----------------------------------------------------------------------------------------------

#developer check
def if_dev_check(ctx):
    return ctx.author.id == 924096612941299762

#Developer only commands
class developer(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @bridge.bridge_command(checks = [if_dev_check])
    async def load(self, ctx, extension):
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}')
        print(f'Loaded {extension}')

    @bridge.bridge_command(checks = [if_dev_check])
    async def unload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension}')
        print(f'Unloaded {extension}')

    @bridge.bridge_command(checks = [if_dev_check])
    async def reload(self, ctx, extension):
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension}')
        print(f'Reloaded {extension}')

    @bridge.bridge_command(checks = [if_dev_check])
    async def restart(self, ctx):
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.bot.unload_extension(f"cogs.{filename[:-3]}")
                self.bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Restarted cog {filename[:-3]}")
                await ctx.send(f"Restarted cog: {filename[:-3]}")
        

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

>>>>>>> Stashed changes
bot.run("TOKEN")