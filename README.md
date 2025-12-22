# 🎮 League of Legends Damage Bot

Jednoduchý Discord bot, ktorý pomocou **Riot API** zisťuje štatistiky poškodenia (damage) hráčov. Bot skontroluje tvoju poslednú hru alebo históriu a vypíše na discorde, či si bol najlepším hráčom v udelenom poškodení.

## 🛠️ Inštalácia
Pre správne fungovanie bota je potrebné nainštalovať tieto knižnice:

```bash
pip install discord.py requests python-dotenv
```
## 🔑 Premenné prostredia (.env)
Vytvorte si v hlavnom priečinku súbor s názvom .env a vložte doň svoje API kľúče. Bot ich automaticky načíta pri štarte:

```
DISCORD_BOT_TOKEN=tvoj_discord_bot_token

RIOT_API_KEY=tvoj_riot_api_kluc
```
DISCORD_BOT_TOKEN: Vytvorte bota na [Discord Developer Portal](https://discord.com/developers/applications) a skopírujte jeho token

RIOT_API_KEY: Zaregistrujte sa na [Riot Developer Portal](https://developer.riotgames.com/)

## 🤖 Pridajte bota na Discord server
V Discord Developer Portáli choďte do "OAuth2" → "URL Generator"

Vyberte "bot" v "SCOPES"

V "BOT PERMISSIONS" vyberte:

"Send Messages"

"Use Slash Commands"

Skopírujte vygenerovanú URL, otvorte v prehliadači a pridajte bota na váš server

## 🚀 Spustenie bota
Bota spustíš jednoducho cez terminál:

Bash
```
python bot.py
```
## 📖 Čo bot dokáže?
Bot využíva endpointy Riot API na získanie údajov o zápasoch:

Kontrola poslednej hry: Príkazom ```/damage_check``` zistí, či mal hráč v poslednom zápase najvyšší damage zo všetkých 10 hráčov.

História zápasov: Príkazy ako ```/top_damage_count``` prehľadajú posledných 20 zápasov a spočítajú, koľkokrát bol hráč "top damager".

Časový údaj: Povie ti, pred akou dobou si naposledy reálne "potiahol" hru s najväčším damage.

## 🕹️ Všeobecné príkazy
```/hello``` - Základný testovací príkaz

```/damage_check <meno> <tag>``` - Zistí, či hráč mal najvyšší damage v poslednej hre

```/last_top_damage <meno> <tag>``` - Kedy hráč naposledy mal top damage

```/top_damage_count <meno> <tag>``` - Koľkokrát mal top damage z posledných 20 hier

Obsahuje aj príkazy pre natvrdo nastavených hráčov

Bot je nastavený pre EÚ región. Ak chceš použiť iný región, uprav endpointy v kóde.

Bot využíva Riot Games API a nie je spojený so spoločnosťou Riot Games.
Riot Games, League of Legends sú ochranné známky spoločnosti Riot Games, Inc.