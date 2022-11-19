import discord
from discord.ext import commands, bridge


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @bridge.bridge_command()
    @commands.has_permissions(kick_members=True)
    async def kick(self,ctx, member: discord.User, *, reason=None):
        """Kicks a member for a specified reason"""
        if reason==None:
            reason= "No reason provided"
        await member.send(f"You've been kicked in {ctx.guild} for: {reason}")
        await ctx.guild.kick(member)
        await ctx.send(f'User {member.mention} has been kicked for: {reason}')

    @bridge.bridge_command()
    @commands.has_permissions(ban_members=True)
    async def ban(self,ctx, member: discord.User, *, reason=None):
        """Bans a member for a specified reason"""
        if reason==None:
            reason= "No reason provided"
        await member.send(f"You've been banned in {ctx.guild} for: {reason}")
        await ctx.guild.ban(member)
        await ctx.send(f'User {member.mention} has been banned for: {reason}')
    
    @bridge.bridge_command()
    @commands.has_permissions(ban_members=True)
    async def unban(self,ctx, member: discord.User, *, reason=None):
        """Unbans a member for a specified reason"""
        if reason==None:
            reason= "No reason provided"
        await member.send(f"You've been unbanned in {ctx.guild} for: {reason}")
        await ctx.guild.unban(member)
        await ctx.send(f'User {member.mention} has been unbanned for: {reason}')
    

def setup(bot):
    bot.add_cog(Moderation(bot))
