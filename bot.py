import discord
import random
from discord.ext import commands

token = open("token.txt").read()

client = commands.Bot(command_prefix = '.')

@client.event
async def on_member_join(member):
    print(f'{member} has joined a server')


@client.event
async def on_member_remove(member):
    print(f'{member} has left a server')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.command()
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency*1000)}ms')

@client.command(aliases=['8ball','8b'])
async def _8ball(ctx, *,question):

    responses = ["It is certain.",
"It is decidedly so.",
"Without a doubt.",
"Yes - definitely.",
"You may rely on it.",
"As I see it, yes.",
"Most likely.",
"Outlook good.",
"Yes.",
"Signs point to yes.",
"Reply hazy, try again.",
"Ask again later.",
"Better not tell you now.",
"Cannot predict now.",
"Concentrate and ask again.",
"Don't count on it.",
"My reply is no.",
"My sources say no.",
"Outlook not so good.",
"Very doubtful."]
    
    await ctx.send(f'{random.choice(responses)}')

@_8ball.error
async def _8ball_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send('Ask a question next time dumbass')



@client.command()
@commands.has_role('Admin')
async def clear(ctx, amount=1):
        await ctx.channel.purge(limit=amount + 1)
        await ctx.send(f'Deleted {amount} messages')
@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRole):
        await ctx.send('Sorry you are not allowed to use this command.')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member=None):
    if not member:
        await ctx.send('Please mention a member')
        return
    await member.ban()
    await ctx.send(f'{member.display_name} was banned from the server')
 
@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member=None):
    if not member:
        await ctx.send('Please mention a member')
        return
    await member.kick()
    await ctx.send(f'{member.display_name} was kicked from the server')

@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send('nice try')

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send('nice try')


@client.command()
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name,member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if(user.name,user.discriminator ) ==(member_name,member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.mention}')
            return
client.run(token)

