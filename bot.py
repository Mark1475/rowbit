import code
from codeop import CommandCompiler
from distutils.util import change_root
from email import message
from operator import imod
from turtle import title
import discord
from discord.ext import commands
from discord.ext.commands import NotOwner
import os
import random
import datetime
import time
import asyncio

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(intents=intents, command_prefix='$')

pairNum = []

send_time = "16:20"

############################################
async def schedule_message():
    now = datetime.datetime.now()
    then = now+datetime.timedelta(days=1)
    then = now.replace(hour=16, minute=20)
    wait_time = (then-now).total_seconds()
    await asyncio.sleep(wait_time)

    channel = bot.get_channel(978804525513191427)
    await channel.send("420 blaze it!!")
############################################

############################################
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
    #await bot.change_presence(status=discord.Status.invisible)
    #await schedule_message()
############################################

############################################
@bot.command(name="say")
async def say(ctx, arg1, arg2):
    channel = bot.get_channel(int(arg2))

    await channel.send(arg1)
    await ctx.send("Message sent!")

############################################

############################################
#deletes bots messages
@bot.command(name="erase")
@commands.is_owner()
async def erase(ctx):
    def is_me(m):
        return m.author == bot.user

    deleted = await ctx.channel.purge(limit = 15, check =is_me)
    await ctx.channel.send("Deleted {} message(s)".format(len(deleted)))
    await ctx.channel.purge(limit=1)
    await ctx.message.delete()
@erase.error #error message
async def erase_error(ctx, error):
    if isinstance(error, NotOwner):
        await ctx.reply("You don't have permission to use this command!")
############################################

############################################
@bot.event
async def on_message_edit(old, nm):
    oldmessage = old.content
    newmessage = nm.content
    author = old.author.name
    channel = bot.get_channel(978864966738272276)
    message = "Author: " + author + "\n" +"Old: " + oldmessage + " Time: " + old.created_at.strftime("%d, %b %Y %I:%M:%S%p %Z") + "\nNew: " + newmessage + " Time: " + nm.edited_at.strftime("%d, %b %Y %I:%M:%S%p %Z")
    await channel.send(message)
############################################

############################################
#dad bot joke
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if ("I'm " in message.content) or ("I am " in message.content):
        word = message.content.split()
        await message.channel.send(" Hi {}, I am RAMbot".format(word[-1]))

    #new message gain exp
    #if exp is greater than threshold level up and reset exp to 0
    #update level


    #with open(message.author.name + ".txt", 'w') as f:

    await bot.process_commands(message)
############################################

############################################
#sends a random quote from a file
@bot.command(name="rq")
async def rq(ctx):
    if ctx.channel.name != "bottesting":
        return
    with open('quotes.txt') as f: 
        lines = f.readlines()
    f.close()

    line = random.choice(lines)
    sLine = line.split("-", 1)
    embed = discord.Embed(title="Random Quote:", description=" ", color =0x2a86e8)
    embed.add_field(name=sLine[0], value= '''    \t   ''' + sLine[1], inline=False)
    await ctx.message.channel.send(embed=embed)
############################################

############################################
@bot.command(name="hello")
async def hello(ctx):
    if ctx.channel.name != "bottesting":
        return
    await ctx.send("Hello")
############################################

############################################
#displays members from server kinda useless tbh
@bot.command(name="members")
async def members(ctx):
    if ctx.channel.name != "bottesting":
        return
    for member in ctx.channel.guild.members:
        await ctx.channel.send(member)
############################################

############################################
#sends a dm to a user
@bot.command(name="dm")
async def dm(ctx, member: discord.Member, arg1):
    if ctx.channel.name != "bottesting":
        return
    emoji = '\N{THUMBS UP SIGN}'
    await ctx.message.add_reaction(emoji)
    await member.send(arg1)
############################################

@bot.command(name="addRole")
async def addRole(ctx, member: discord.Member, role: discord.Role):
    if ctx.channel.name != "bottesting":
        return
    if role in member.roles:
        await ctx.send(f"{member.mention} already has the role, {role}")
    else:
        await member.add_roles(role)
        await ctx.send(f"Added {role} to {member.mention}")
############################################

############################################
@bot.command(name="removeRole")
async def removeRole(ctx, member: discord.Member, role: discord.Role):
    if ctx.channel.name != "bottesting":
        return
    if role in member.roles:
        await member.remove_roles(role)
        await ctx.send(f"Remove {role} from {member.mention}")
    else:
        await member.add_roles(role)
        await ctx.send(f"{member.mention} does not have the role {role}")
############################################


############################################
@bot.command(name="getnames")
async def getnames(ctx):
    if ctx.channel.name != "bottesting":
        return
    with open('newnames.txt') as f:
        lines = f.readlines()
    f.close()
    for line in lines:
        member = discord.utils.get(ctx.guild.members, name=line)
        await ctx.send(member.mention)
############################################

############################################
@bot.command(name="storenames")
async def storenames(ctx):
    if ctx.channel.name != "bottesting":
        return
    with open("newnames.txt", 'w') as f:
        for mem in ctx.guild.members:
            await ctx.send(mem.name)
            f.write(mem.name+ '\n')
    f.close()    
############################################


############################################
@bot.command(name= "santa")
async def santa(ctx):
    if ctx.channel.name != "bottesting":
        return

    possible = names
    count = 0
    recipient = []

    while(count == 0):
        redo = False
        possible = names.copy()

        for i in range(0, len(names)):
            recip = random.randint(0, len(possible)-1)
            x = 0
            while (x==0):
                if(names[i] == possible[recip]):
                    if(len(possible) == 1):
                        redo = True
                        x = 1
                    else:
                        recip = random.randint(0, len(possible)-1)
                else:
                    x = 1
            if(redo != True):
                recipient.append(possible[recip])
                possible.pop(recip)
                count = 1
            else:
                count = 0
    i = 0
    for name in names:
        #dm name with recipient added later
        await ctx.send("Giver: " + name + " Recipient: " + recipient[i])
        i += 1
############################################

############################################
#displays commands info
@bot.command(name="info")
async def info(ctx):
    if ctx.channel.name != "bottesting":
        return
    embed = discord.Embed(title ="RAMbot help info", description= "List of usage commands", color =0x2a86e8)
    embed.add_field(name="$dm <user> \"message\" ", value="dms user with message", inline=False)
    embed.add_field(name="$leave", value=" bots leaves (botowner only)", inline=False)
    embed.add_field(name="$members", value=" lists members in server", inline=False)
    embed.add_field(name="$erase", value="deletes last 15 bot messages", inline=False)
    embed.add_field(name="$quote", value="Picks a random quote from file", inline=False)
    embed.add_field(name="$addRole <user> rolename", value="Adds role to user if not already assigned", inline=False)
    embed.add_field(name="$removeRole <user> rolename", value="Removes role from user if it has that role assigned", inline=False)
    embed.add_field(name="$info", value="displays list of commands (this whole message)", inline=False)

    await ctx.message.channel.send(embed=embed)
############################################

############################################################
#monster hunters test
@bot.command(name="monster")
async def monster(ctx):
    with open("Rathalos.txt") as f:
        lines = f.readlines()

    me = ""
    for line in lines:
        me += line

    await ctx.message.channel.send(" ` "+ me +" ` ")
    f.close()
############################################################

############################################
#disconnects bot    
@bot.command(name="leave")
@commands.is_owner()
async def leave(ctx):
    if ctx.channel.name != "bottesting":
        return
    await ctx.send("Bye bye!")
    await bot.logout()
    await bot.close()
@leave.error #error message
async def leave_error(ctx, error):
    if isinstance(error, NotOwner):
        await ctx.reply("You don't have permission to use this command!")
############################################

bot.run()