#General use commands go here

import discord
from discord.ext import bridge, commands


class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    async def ping(self, ctx):
        await ctx.send('pong')
    
# Help command
class definitely_stolen(commands.HelpCommand):
    
    def get_command_signature(self, command:commands.Command):
        return '%s%s %s' % (self.context.clean_prefix, command.qualified_name, command.signature)

    async def send_bot_help(self, mapping):
        embed = discord.Embed(title="Help", color=discord.Color.blurple())

        for cog, commands in mapping.items():
            filtered = await self.filter_commands(commands, sort = True)
            command_signatures = [self.get_command_signature(c) for c in filtered]

            if command_signatures:
                    cog_name = getattr(cog, "qualified_name", "No Category")
                    embed.add_field(name=cog_name, value="\n".join(command_signatures), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_command_help(self, command):
        embed = discord.Embed(title=self.get_command_signature(command), color=discord.Color.blurple())
        if command.help:
            embed.description = command.help
        if alias := command.aliases:
            embed.add_field(name="Aliases", value=", ".join(alias), inline=False)

        channel = self.get_destination()
        await channel.send(embed=embed)
    
    async def send_error_message(self, error):
        embed = discord.Embed(title="Error", description=error, color=discord.Color.red())
        channel = self.get_destination()

        await channel.send(embed=embed)

def setup(bot):
    generalCog = general(bot)
    bot.add_cog(generalCog)
    bot.help_command = definitely_stolen()
    bot.help_command.cog = generalCog