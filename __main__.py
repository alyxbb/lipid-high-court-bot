import json
import discord
from discord.ext import commands
lawsuitinprog=False


Client = commands.Bot(commands.when_mentioned_or("!"),description="a bot for the lipidcraft server")


@Client.command(description="Sue someone")
async def sue(ctx):
    await ctx.message.delete(delay=0.5) # if no delay it doenst delete for some reason
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
        await setupmsg.edit(embed=setupembed,delete_after=60)
        plaintiff=ctx.author
        defendant=msg.content
        reason=message.content

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
