# 🎮 League of Legends Damage Bot

A Discord bot that uses the **Riot API** to track damage statistics 
for League of Legends players. Check whether you dealt the most 
damage in your last game or across your recent match history.

"Note: Riot API key expires periodically — for a live demo, clone the repo and add your own key."

## 🛠️ Installation

```bash
pip install discord.py requests python-dotenv
```
## 🔑 Premenné prostredia (.env)
Create a `.env` file in the root directory with the following:

```
DISCORD_BOT_TOKEN=your_discord_bot_token
RIOT_API_KEY=your_riot_api_key
```
- **DISCORD_BOT_TOKEN** — Create a bot at the 
[Discord Developer Portal](https://discord.com/developers/applications)
- **RIOT_API_KEY** — Register at the 
[Riot Developer Portal](https://developer.riotgames.com/)

## 🤖 Adding the Bot to Your Server

1. Go to **OAuth2 → URL Generator** in the Discord Developer Portal
2. Select `bot` under **Scopes**
3. Under **Bot Permissions**, select `Send Messages` 
and `Use Slash Commands`
4. Copy the generated URL, open it in your browser, 
and add the bot to your server

## 🚀 Running the Bot

```bash
python bot.py
```
## 📖 Features

- **`/damage_check <name> <tag>`** — Checks if the player had 
the highest damage among all 10 players in their last game
- **`/last_top_damage <name> <tag>`** — Shows when the player 
last had the top damage in a game
- **`/top_damage_count <name> <tag>`** — Counts how many times 
the player had top damage across their last 20 games
- **`/hello`** — Basic test command

Also includes commands for hardcoded (pre-set) players.

> Bot is configured for the EU region. 
> To use a different region, update the endpoints in the code.

---

*This project uses the Riot Games API and is not affiliated 
with Riot Games, Inc. League of Legends is a trademark 
of Riot Games, Inc.*
