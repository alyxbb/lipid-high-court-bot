import json
import discord
from discord.ext import commands
lawsuitinprog=False
channel=None
state=0


Client = commands.Bot(commands.when_mentioned_or("!"),description="a bot for the lipidcraft server")





@Client.command(description="Sue someone")
async def sue(ctx):
    global channel
    plantiffrole = discord.utils.get(ctx.guild.roles, name="plaintiff")
    defendantrole = discord.utils.get(ctx.guild.roles, name="defendant")
    await ctx.message.delete(delay=1) # if no delay it doenst delete for some reason
    global lawsuitinprog
    if not lawsuitinprog:
        setupembed= await getsetupembed(ctx,"not set","not set")
        setupmsg = await ctx.send(embed=setupembed)
        await ctx.send("please ping the person you would like to sue",delete_after=10)
        lawsuitinprog=True

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        msg = await Client.wait_for('message', check=check)
        await msg.delete(delay=0.5)
        setupembed = await getsetupembed(ctx, msg.content, "not set")
        await setupmsg.edit(embed=setupembed)
        await ctx.send("please state the reason you are suing this person", delete_after=10)

        message = await Client.wait_for('message', check=check)
        await message.delete(delay=0.5)
        setupembed = await getsetupembed(ctx, msg.content, message.content)
        await setupmsg.edit(embed=setupembed)
        plaintiff=ctx.author
        defendant=msg.mentions[0]
        reason=message.content
        channel=ctx.channel
        await plaintiff.add_roles(plantiffrole)
        await defendant.add_roles(defendantrole)


    else:
        await ctx.send("lawsuit already in progress",deleteafter=60)


@Client.event
async def on_ready():

    rp = discord.Activity(name="over the lipidcraft server", type=discord.ActivityType.watching)
    await Client.change_presence(status=discord.Status.dnd, activity=rp)
    print("ready")

def main():
    with open('config.json') as f:
        config = json.load(f)
    Client.run(config["token"])


async def getsetupembed(ctx,defendant,reason):
    plaintifffield="plaintiff:  "+ctx.author.mention
    defendantfield="defendant: "+defendant
    reasonfield="reason: "+reason
    description=plaintifffield+"\n"+defendantfield+"\n"+reasonfield
    embed = discord.Embed(title="lawsuit setup", description=description, color=0x00ff00)

    return embed

@Client.event
async def on_message(message):
    global channel,state

    if lawsuitinprog and channel==message.channel and not(message.author.bot):
        isplaintiff=False
        isdefendant=False
        for role in message.author.roles:
            if role.name=="plaintiff":
                isplaintiff=True
            elif role.name=="defendant":
                isdefendant=True
        if not(isdefendant or isplaintiff):
            await message.channel.send("you are not a part of this lawsuit")
            await message.delete()
        else:
            if state%2==0:
                if isplaintiff:
                    print("plaintiff just spoke")
                    state+=1
                else:
                    await message.channel.send("it is not your turn to speak",delete_after=10)
                    await message.delete()
            else:
                if isdefendant:
                    print("defendant just spoke")
                    state+=1
                else:
                    await message.channel.send("it is not your turn to speak",delete_after=10)
                    await message.delete()
    await Client.process_commands(message)

if __name__ == "__main__":
    main()
