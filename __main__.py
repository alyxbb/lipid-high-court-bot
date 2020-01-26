import json
import discord
from discord.ext import commands
lawsuitinprog=False


Client = commands.Bot(commands.when_mentioned_or("!"),description="a bot for the lipidcraft server")


@Client.command(description="sue someone")
async def sue(ctx):
    global lawsuitinprog
    if not lawsuitinprog:
        setupembed= await getsetupembed(ctx,"not set","not set")
        setupmsg = await ctx.send(embed=setupembed)
        await ctx.send("please ping the person you would like to sue")
        lawsuitinprog=True
    else:
        await ctx.send("lawsuit already in progress")


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


if __name__ == "__main__":
    main()
