import nextcord
from nextcord import Embed, SlashOption
from nextcord.ext import commands, tasks

# Bot setup
intents = nextcord.Intents.all()
intents.messages = True
intents.guilds = True
intents.message_content = True
intents.reactions = True


bot = commands.Bot(command_prefix='!', intents=intents)
bot.remove_command("help")


@bot.event
async def on_ready():
    
    print(f'{bot.user} is connected and ready!')
    await bot.change_presence(status=nextcord.Status.idle, activity=nextcord.Activity(type=nextcord.ActivityType.watching, name="Deleting Messages!"))

@bot.command(name='deletemessage')
@commands.has_permissions(manage_messages=True)
async def deletemessage(ctx, message_id1: int, message_id2: int):
    if message_id1 == message_id2:
        await ctx.send("The message IDs are the same. Nothing to delete.")
        return
    
    try:
        message1 = await ctx.channel.fetch_message(message_id1)
        message2 = await ctx.channel.fetch_message(message_id2)
    except nextcord.NotFound:
        await ctx.send("One or both message IDs are invalid.")
        return

    # Ensure message_id1 is less than message_id2
    if message1.created_at > message2.created_at:
        message1, message2 = message2, message1

    def is_between(m):
        return message1.created_at <= m.created_at <= message2.created_at

    total_deleted = 0
    while True:
        deleted = await ctx.channel.purge(check=is_between, limit=100)
        total_deleted += len(deleted)
        if len(deleted) < 100:
            break

    await ctx.send(f"Deleted {total_deleted} messages between {message_id1} and {message_id2}.")




# Catch error if it doesn't log in
try:
    bot.run('YOURTOKEN')
except nextcord.errors.LoginFailure:
    print("Error: Invalid Discord token")