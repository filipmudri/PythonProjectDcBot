import os
import requests
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
import datetime

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
RIOT_API_KEY = os.getenv("RIOT_API_KEY")
#GUILD_ID = 783290868655194132  # guild ID

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_puuid(gameName: str, tagLine: str):
    url = f"https://americas.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{gameName}/{tagLine}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    return r.json()["puuid"]

def get_last_match(puuid: str):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count=1"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    return r.json()[0]

def had_highest_damage(puuid: str, match_id: str):
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return None
    match = r.json()
    participants = match["info"]["participants"]
    damages = [(p["puuid"], p["totalDamageDealtToChampions"]) for p in participants]
    max_damage = max(damages, key=lambda x: x[1])
    return max_damage[0] == puuid, max(damages, key=lambda x: x[1])[1]

import datetime

def get_match_ids(puuid: str, count: int = 20):
    """Získa posledných X match ID pre hráča"""
    url = f"https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?count={count}"
    headers = {"X-Riot-Token": RIOT_API_KEY}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return []
    return r.json()

def check_damage_history(puuid: str, count: int = 20):
    """Prejde posledných X zápasov a zistí:
       - kedy mal hráč naposledy najväčší damage
       - koľkokrát mal najväčší damage
    """
    match_ids = get_match_ids(puuid, count)
    if not match_ids:
        return None, 0

    last_top = None
    top_count = 0

    for match_id in match_ids:
        url = f"https://europe.api.riotgames.com/lol/match/v5/matches/{match_id}"
        headers = {"X-Riot-Token": RIOT_API_KEY}
        r = requests.get(url, headers=headers)
        if r.status_code != 200:
            continue
        match = r.json()

        participants = match["info"]["participants"]
        damages = [(p["puuid"], p["totalDamageDealtToChampions"]) for p in participants]
        max_damage = max(damages, key=lambda x: x[1])

        # ak náš hráč bol top
        if max_damage[0] == puuid:
            top_count += 1
            game_creation = match["info"]["gameCreation"] // 1000  # ms → s
            last_top = datetime.datetime.fromtimestamp(game_creation)

    return last_top, top_count


def format_time_difference(dt: datetime.datetime):
    """Naformátuje rozdiel času (pred 5 min, 3 hod, 2 dni)"""
    if not dt:
        return "nikdy"
    now = datetime.datetime.now()
    diff = now - dt

    if diff.days > 0:
        return f"pred {diff.days} dňami"
    hours = diff.seconds // 3600
    if hours > 0:
        return f"pred {hours} hodinami"
    minutes = diff.seconds // 60
    if minutes > 0:
        return f"pred {minutes} minútami"
    return "pred chvíľou"


@bot.event
async def on_ready():
    print(f"✅ Prihlásený ako {bot.user}")

    #guild = discord.Object(id=GUILD_ID)

    # Vymazať staré príkazy
    #await bot.tree.sync(guild=guild)  # nutné pre synchronizáciu
    #print("🔄 Slash commands synchronizované pre guild.")

    try:
        synced = await bot.tree.sync()
        print(f"Synced: {len(synced)} command(s)")
    except Exception as e:
        print(e)


# Slash command
@bot.tree.command(name = "hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello, {interaction.user.mention}! World", ephemeral=True)

@bot.tree.command(name="damage_check")
async def damage_check(interaction: discord.Interaction, game_name: str, tag_line: str):
    await interaction.response.defer()
    puuid = get_puuid(game_name, tag_line)
    if not puuid:
        await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
        return
    match_id = get_last_match(puuid)
    if not match_id:
        await interaction.followup.send("❌ Nepodarilo sa získať posledný zápas.")
        return
    result, max_damage = had_highest_damage(puuid, match_id)
    if result is None:
        await interaction.followup.send("❌ Chyba pri načítaní detailu zápasu.")
        return
    if result:
        await interaction.followup.send(f"✅ Hráč **{game_name}#{tag_line}** mal najväčší damage: {max_damage}")
    else:
        await interaction.followup.send(f"❌ Hráč **{game_name}#{tag_line}** nemal najväčší damage. Max: {max_damage}")

@bot.tree.command(name="damage_check_robo")
async def damage_check_robo(interaction: discord.Interaction):
    await interaction.response.defer()

    # pevne nastavené meno a tagline
    game_name = "RoboFico"
    tag_line = "SMER"

    puuid = get_puuid(game_name, tag_line)
    if not puuid:
        await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
        return
    match_id = get_last_match(puuid)
    if not match_id:
        await interaction.followup.send("❌ Nepodarilo sa získať posledný zápas.")
        return
    result, max_damage = had_highest_damage(puuid, match_id)
    if result is None:
        await interaction.followup.send("❌ Chyba pri načítaní detailu zápasu.")
        return
    if result:
        # await interaction.followup.send(f"✅ Hráč **{game_name}#{tag_line}** mal najväčší damage: {max_damage}")
        await interaction.followup.send(f"✅ Hráč mal najväčší damage: {max_damage} no way")
    else:
        # await interaction.followup.send(f"❌ Hráč **{game_name}#{tag_line}** nemal najväčší damage. Max: {max_damage}")
        await interaction.followup.send(f"❌ Hráč nemal najväčší damage. Max: {max_damage}")

    @bot.tree.command(name="last_top_damage")
    async def last_top_damage(interaction: discord.Interaction, game_name: str, tag_line: str):
        await interaction.response.defer()
        puuid = get_puuid(game_name, tag_line)
        if not puuid:
            await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
            return

        last_top, _ = check_damage_history(puuid, count=20)
        if not last_top:
            await interaction.followup.send(
                f"❌ Hráč **{game_name}#{tag_line}** nemal najväčší damage v posledných zápasoch.")
            return

        time_str = format_time_difference(last_top)
        await interaction.followup.send(f"✅ Hráč **{game_name}#{tag_line}** mal naposledy najväčší damage {time_str}.")

    @bot.tree.command(name="top_damage_count")
    async def top_damage_count(interaction: discord.Interaction, game_name: str, tag_line: str):
        await interaction.response.defer()
        puuid = get_puuid(game_name, tag_line)
        if not puuid:
            await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
            return

        _, top_count = check_damage_history(puuid, count=20)
        await interaction.followup.send(
            f"✅ Hráč **{game_name}#{tag_line}** mal najväčší damage **{top_count}x** z posledných 20 hier.")


@bot.tree.command(name="last_top_damage_robo")
async def last_top_damage_robo(interaction: discord.Interaction):
    await interaction.response.defer()

    game_name = "RoboFico"
    tag_line = "SMER"

    puuid = get_puuid(game_name, tag_line)
    if not puuid:
        await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
        return

    last_top, _ = check_damage_history(puuid, count=20)
    if not last_top:
        await interaction.followup.send(f"❌ Hráč **{game_name}#{tag_line}** nemal najväčší damage v posledných zápasoch.")
        return

    time_str = format_time_difference(last_top)
    await interaction.followup.send(f"✅ Hráč **{game_name}#{tag_line}** mal naposledy najväčší damage {time_str}.")


@bot.tree.command(name="top_damage_count_robo")
async def top_damage_count_robo(interaction: discord.Interaction):
    await interaction.response.defer()

    game_name = "RoboFico"
    tag_line = "SMER"

    puuid = get_puuid(game_name, tag_line)
    if not puuid:
        await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
        return

    _, top_count = check_damage_history(puuid, count=20)
    await interaction.followup.send(f"✅ Hráč **{game_name}#{tag_line}** mal najväčší damage **{top_count}x** z posledných 20 hier.")

    @bot.tree.command(name="last_top_damage_p_mudri")
    async def last_top_damage_robo(interaction: discord.Interaction):
        await interaction.response.defer()

        game_name = "Defender145"
        tag_line = "XTC"

        puuid = get_puuid(game_name, tag_line)
        if not puuid:
            await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
            return

        last_top, _ = check_damage_history(puuid, count=20)
        if not last_top:
            await interaction.followup.send(
                f"❌ Hráč **{game_name}#{tag_line}** nemal najväčší damage v posledných zápasoch.")
            return

        time_str = format_time_difference(last_top)
        await interaction.followup.send(f"✅ Hráč **{game_name}#{tag_line}** mal naposledy najväčší damage {time_str}.")



# async def damage_check(interaction: discord.Interaction, gameName: str, tagLine: str):
#     await interaction.response.defer()
#     puuid = get_puuid(gameName, tagLine)
#     if not puuid:
#         await interaction.followup.send("❌ Nepodarilo sa získať PUUID.")
#         return
#     match_id = get_last_match(puuid)
#     if not match_id:
#         await interaction.followup.send("❌ Nepodarilo sa získať posledný zápas.")
#         return
#     result, max_damage = had_highest_damage(puuid, match_id)
#     if result is None:
#         await interaction.followup.send("❌ Chyba pri načítaní detailu zápasu.")
#         return
#     if result:
#         await interaction.followup.send(f"✅ Hráč **{gameName}#{tagLine}** mal najväčší damage: {max_damage}")
#     else:
#         await interaction.followup.send(f"❌ Hráč **{gameName}#{tagLine}** nemal najväčší damage. Max: {max_damage}")

bot.run(DISCORD_TOKEN)
