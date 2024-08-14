import nextcord
from nextcord.ext import commands
import aiohttp

# تعيين التوكن مباشرة هنا
TOKEN = 'your_bot_token_here'

# تمكين جميع النوايا
intents = nextcord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

AUTHORIZED_USER_ID = YOUR_ID  # معرف المستخدم المصرح له

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user}.')

@bot.slash_command(description="DM BOT FOR ALL MEMBERS")
async def send(interaction: nextcord.Interaction, message: str):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    await interaction.response.send_message("Done! All members have been sent the message.", ephemeral=True)

    guild = interaction.guild
    members = guild.members

    for member in members:
        if not member.bot:
            try:
                await member.send(f"{member.mention}, {message}")
            except:
                pass

@bot.slash_command(description="Change bot status")
async def changestatus(interaction: nextcord.Interaction):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    options = [
        nextcord.SelectOption(label="Competing", value="competing"),
        nextcord.SelectOption(label="Playing", value="playing"),
        nextcord.SelectOption(label="Watching", value="watching"),
        nextcord.SelectOption(label="Streaming", value="streaming"),
        nextcord.SelectOption(label="Do Not Disturb", value="dnd"),
        nextcord.SelectOption(label="Idle", value="idle"),
        nextcord.SelectOption(label="Online [default]", value="online")
    ]

    select = nextcord.ui.Select(placeholder="Choose a status type...", options=options)

    async def status_input(message):
        if message.author.id == AUTHORIZED_USER_ID:
            status_type = select.values[0]
            status_message = message.content

            if status_type == "playing":
                activity = nextcord.Game(name=status_message)
            elif status_type == "competing":
                activity = nextcord.Activity(type=nextcord.ActivityType.competing, name=status_message)
            elif status_type == "watching":
                activity = nextcord.Activity(type=nextcord.ActivityType.watching, name=status_message)
            elif status_type == "streaming":
                activity = nextcord.Streaming(name=status_message, url="https://twitch.tv/test")
            elif status_type == "dnd":
                await bot.change_presence(status=nextcord.Status.dnd, activity=None)
                await interaction.channel.send(f"Status changed to Do Not Disturb")
                bot.remove_listener(status_input, "on_message")
                return
            elif status_type == "idle":
                await bot.change_presence(status=nextcord.Status.idle, activity=None)
                await interaction.channel.send(f"Status changed to Idle")
                bot.remove_listener(status_input, "on_message")
                return
            elif status_type == "online":
                await bot.change_presence(status=nextcord.Status.online, activity=None)
                await interaction.channel.send(f"Status changed to Online")
                bot.remove_listener(status_input, "on_message")
                return

            await bot.change_presence(activity=activity)
            await interaction.channel.send(f"Status changed to {status_type} {status_message}")
            bot.remove_listener(status_input, "on_message")

    async def select_callback(interaction: nextcord.Interaction):
        await interaction.response.send_message("Type your status message:", ephemeral=True)
        bot.add_listener(status_input, "on_message")

    select.callback = select_callback
    view = nextcord.ui.View()
    view.add_item(select)
    await interaction.response.send_message("Choose the status type:", view=view)

@bot.slash_command(description="Change bot avatar")
async def changeavatarbot(interaction: nextcord.Interaction, avatar_url: str):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    async with aiohttp.ClientSession() as session:
        async with session.get(avatar_url) as response:
            if response.status != 200:
                await interaction.response.send_message("Failed to fetch avatar.", ephemeral=True)
                return
            avatar_data = await response.read()

    await bot.user.edit(avatar=avatar_data)
    await interaction.response.send_message("Avatar updated successfully.", ephemeral=True)

@bot.slash_command(description="Change bot bio")
async def changebio(interaction: nextcord.Interaction, bio: str):
    if interaction.user.id != AUTHORIZED_USER_ID:
        await interaction.response.send_message("You are not authorized to use this command.", ephemeral=True)
        return

    await interaction.response.send_message("This functionality is not supported by Nextcord.", ephemeral=True)

bot.run(TOKEN)
