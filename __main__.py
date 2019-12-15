import json
import discord
from discord.ext import commands


Client = commands.Bot(commands.when_mentioned_or("!"),description="a bot for the lipidcraft server")


@Client.command(description="sue someone")
async def sue(ctx):
    setupembed= await getsetupembed(ctx)
    game = await ctx.send(embed=setupembed)


@Client.event
async def on_ready():
    rp = discord.Activity(name="over the lipidcraft server", type=discord.ActivityType.watching)
    await Client.change_presence(status=discord.Status.dnd, activity=rp)
    print("ready")

def main():
    with open('config.json') as f:

        config = json.load(f)
    Client.run(config["token"])


async def getsetupembed(ctx):
    creator = ctx.author.mention
    defendantfield="defendant: "+"not set"
    reasonfield="reason: "+"not set"
    description=creator+"\n"+defendantfield+"\n"+reasonfield
    embed = discord.Embed(title="lawsuit setup", description=description, color=0x00ff00)

    return embed


if __name__ == "__main__":
    main()
