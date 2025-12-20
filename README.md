# 🎮 League of Legends Damage Bot

Jednoduchý Discord bot, ktorý pomocou **Riot API** zisťuje štatistiky poškodenia (damage) hráčov. Bot skontroluje tvoju poslednú hru alebo históriu a vypíše, či si bol najlepším hráčom v udelenom poškodení.

## 🛠️ Inštalácia
Pre správne fungovanie bota je potrebné nainštalovať tieto knižnice:

```bash
pip install discord.py requests python-dotenv
```
🔑 Premenné prostredia (.env)
Vytvor si v hlavnom priečinku súbor s názvom .env a vlož doň svoje API kľúče. Bot ich automaticky načíta pri štarte:

Útržok kódu

DISCORD_BOT_TOKEN=tvoj_discord_bot_token
RIOT_API_KEY=tvoj_riot_api_kluc
DISCORD_BOT_TOKEN: Získaš na Discord Developer Portal.

RIOT_API_KEY: Získaš na Riot Developer Portal.

🚀 Spustenie bota
Bota spustíš jednoducho cez terminál:

Bash

python bot.py
📖 Čo bot dokáže?
Bot využíva endpointy Riot API na získanie údajov o zápasoch:

Kontrola poslednej hry: Príkazom /damage_check zistí, či mal hráč v poslednom zápase najvyšší damage zo všetkých 10 hráčov.

História zápasov: Príkazy ako /top_damage_count prehľadajú posledných 20 zápasov a spočítajú, koľkokrát bol hráč "top damager".

Časový údaj: Povie ti, pred akou dobou si naposledy reálne "potiahol" hru s najväčším damage.

🕹️ Príklady príkazov
/damage_check [meno] [tag] - Skontroluje tvoju poslednú hru.

/last_top_damage [meno] [tag] - Zistí, kedy si mal naposledy najvyšší damage.

/top_damage_count_robo - Rýchly prednastavený check pre konkrétneho hráča.
