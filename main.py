import discord
import os
from os import listdir
from discord.ext import bridge, commands
from plyer import notification
import asyncpg
import config

intents = discord.Intents.default()
intents.message_content = True
DEFAULT_PREFIX = ","
TOKEN = config.TOKEN

bot = bridge.Bot(command_prefix=",", intents=intents)

#creates db pool
async def create_db_pool():
    bot.db = await asyncpg.create_pool(database = "Flareonbot", user = "postgres", password = "henlowo")
    print("Connection successful")

#Gets the prefix
async def get_prefix(bot, message):
    #If the message is in direct messages
    if not message.guild:
        return commands.when_mentioned_or(DEFAULT_PREFIX)(bot, message)

    prefix = await bot.db.fetch('SELECT prefix FROM guilds WHERE "guild_id" = $1', message.guild.id)

    #If the prefix doesn't exist
    if len(prefix) == 0:
        await bot.db.execute('INSERT INTO guilds("guild_id", prefix) VALUES ($1, $2)', message.guild.id, DEFAULT_PREFIX)
    #If there is a prefix
    else:
        prefix = prefix[0].get("prefix")
    

    return commands.when_mentioned_or(prefix)(bot, message)


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
    print(f"{ctx.author} Has used command: {ctx.command}")
#On application command completion
@bot.event
async def on_application_command_completion(ctx):
    print(f"{ctx.author} Has used command: {ctx.command}")

#Before prefixed command runs
@bot.event
async def on_command(ctx):
    print(f"{ctx.author} Has used command: {ctx.command}")

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
class Developer(commands.Cog):
    def __init__(self, bot): 
        self.bot = bot

    @bridge.bridge_command(checks = [if_dev_check])
    async def load(self, ctx, extension):
        "Loads the specified cog"
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Loaded {extension}')
        print(f'Loaded {extension}')

    @bridge.bridge_command(checks = [if_dev_check])
    async def unload(self, ctx, extension):
        "Unloads the specified cog"
        self.bot.unload_extension(f'cogs.{extension}')
        await ctx.send(f'Unloaded {extension}')
        print(f'Unloaded {extension}')

    @bridge.bridge_command(checks = [if_dev_check])
    async def reload(self, ctx, extension):
        "Reloads the specified cog"
        self.bot.unload_extension(f'cogs.{extension}')
        self.bot.load_extension(f'cogs.{extension}')
        await ctx.send(f'Reloaded {extension}')
        print(f'Reloaded {extension}')

    @bridge.bridge_command(checks = [if_dev_check])
    async def restart(self, ctx):
        "Restarts all the cogs"
        for filename in os.listdir("./cogs"):
            if filename.endswith(".py"):
                self.bot.unload_extension(f"cogs.{filename[:-3]}")
                self.bot.load_extension(f"cogs.{filename[:-3]}")
                print(f"Restarted cog {filename[:-3]}")
                await ctx.send(f"Restarted cog: {filename[:-3]}")
        
#Adds the developer cog
bot.add_cog(Developer(bot))

#Loads all the cogs in the cogs folder
for filename in listdir("./cogs"):
    if filename.endswith(".py"):
        try:
            bot.load_extension(f"cogs.{filename[:-3]}")
            print("loaded " + filename)
        except:
            print("Could not load, could be missing a setup function or not intended as a cog. File: " + filename)

bot.loop.run_until_complete(create_db_pool())
bot.run(TOKEN)