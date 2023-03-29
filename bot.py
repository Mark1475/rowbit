import discord
from discord.ext import commands
from discord.ext.commands import NotOwner
import os
import random
import datetime
import time
import asyncio
import mariadb as mdb
import sys

intents = discord.Intents.all()
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)

pairNum = []

try:
    con = mdb.connect(
        host = "IP",
        port = 3306,
        user = "root",
        password = "data",
        database="monstersdb"
    )
    cur = con.cursor()
    print("Connected!")
except mdb.Error as e:
    print(e)
    sys.exit(1)
############################################

############################################
@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    
############################################

############################################
@bot.command(name="monsterinfo")
async def say(ctx, arg1, arg2):
    #
    if arg2 == '-s':
        cur.execute("SELECT * FROM Monsterview WHERE monster LIKE \"%" + arg1 + "%\"")
    elif arg2 == '-e':
        cur.execute("SELECT * FROM Monsterview WHERE monster = \"" + arg1 + "\";")
    else:
        await ctx.send("Query mode invalid. Should be either -s(to search) or -e(to get exact monster)")
    tavnit = '|'
    separator = '+'
    widths = []
    columns = []
    output = ""
    results = cur.fetchall()

    for cd in cur.description:
        widths.append(max(cd[2], len(cd[0])))
        columns.append(cd[0])
    for w in widths:
        tavnit += " %-"+"%ss |" % (w,)
        separator += "-"*w + '--+'

    output += "```"+separator+"\n"
    output += tavnit % tuple(columns) + "\n"
    output += separator+"\n"
    for row in results:
        output += tavnit % row+"\n"
    output += separator+"```\n"
    
    await ctx.send(output)


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
#dad bot joke
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if ("I'm " in message.content) or ("I am " in message.content):
        word = message.content.split()
        await message.channel.send(" Hi {}, I am RAMbot".format(word[-1]))

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
# for secrect santa among friends
@bot.command(name= "santa")
async def santa(ctx):
    if ctx.channel.name != "bottesting":
        return
    names=[]
    count = 0
    recipient = []
    
    for guild in bot.guilds:
        for member in guild.members:
            #members not participating in secret santa and bots
            if member.name == "mem1" or member.name == "mem2" or member.name == "bot1" :
                continue    
            names.append(member)

    possible = names

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
    for n in names:
        await n.send(" You get " + recipient[i].name)
        i += 1
    await ctx.send("Done!!")    
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
    embed.add_field(name="$monsterinfo", value="Searches monster info from a database :O", inline=False)

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
    await bot.logout()
    await bot.close()
    exit(0)
@leave.error #error message
async def leave_error(ctx, error):
    if isinstance(error, NotOwner):
        await ctx.reply("You don't have permission to use this command!")
############################################

bot.run("Bot_token")