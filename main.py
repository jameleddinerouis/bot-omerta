{\rtf1\ansi\ansicpg1252\cocoartf2867
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 import discord\
from discord.ext import commands\
import random\
\
# 1. Les Intents (permissions)\
intents = discord.Intents.default()\
intents.members = True\
intents.voice_states = True\
intents.message_content = True\
\
# 2. Cr\'e9ation du bot\
bot = commands.Bot(command_prefix="!", intents=intents)\
\
# ==========================================\
# \uc0\u9881 \u65039  CONFIGURATION DES SALONS (TES IDs)\
# ==========================================\
ID_BIENVENUE = 1505275545812860950\
ID_MESSAGES = 1505275843830878289\
ID_ALERTES = 1505278942737731707\
ID_COMMANDES = 1505279169079152721\
# ==========================================\
\
@bot.event\
async def on_ready():\
    await bot.change_presence(activity=discord.Game(name="Surveiller l'OMERTA"))\
    print("---------------------------------")\
    print(f"\uc0\u55357 \u56613  L'OMERTA EST EN PLACE ! \{bot.user.name\} est connect\'e9.")\
    print("---------------------------------")\
\
@bot.event\
async def on_member_join(member):\
    """Envoie un message quand un membre arrive."""\
    salon_bienvenue = bot.get_channel(ID_BIENVENUE)\
    if salon_bienvenue:\
        messages_bienvenue = [\
            f"\{member.mention\} ce gros charo est arriv\'e9.",\
            f"Merde, \{member.mention\} est l\'e0.",\
            f"\{member.mention\} EST LA\uc0\u55357 \u56613 .",\
            f"\{member.mention\} est l\'e0 (allo selem il est pas s\'e9lectionn\'e9).",\
            f"Yo le frro \{member.mention\}"\
        ]\
        message_choisi = random.choice(messages_bienvenue)\
        await salon_bienvenue.send(message_choisi)\
\
@bot.event\
async def on_voice_state_update(member, before, after):\
    """Envoie une alerte dans #alertes quand qqn est seul en vocal."""\
    if before.channel is None and after.channel is not None:\
        if len(after.channel.members) == 1:\
            salon_alertes = bot.get_channel(ID_ALERTES)\
            if salon_alertes:\
                await salon_alertes.send(f"\uc0\u55357 \u57000  \{member.mention\} t'attend en vocal dans **\{after.channel.name\}** !")\
\
@bot.command()\
async def setup(ctx):\
    """Commande \'e0 utiliser une seule fois pour expliquer les salons."""\
    # Le bot envoie un message dans BIENVENUE\
    salon_bienvenue = bot.get_channel(ID_BIENVENUE)\
    if salon_bienvenue:\
        await salon_bienvenue.send("\uc0\u55357 \u57041  **Poste de contr\'f4le.**\\nC'est ici que l'OMERTA surveille les all\'e9es et venues. Pas de blabla, le bot notifie juste quand l'un de vous d\'e9barque.")\
\
    # Le bot envoie un message dans MESSAGES\
    salon_messages = bot.get_channel(ID_MESSAGES)\
    if salon_messages:\
        await salon_messages.send("\uc0\u55357 \u56492  **Le QG.**\\nDiscussions g\'e9n\'e9rales, d\'e9lires, jeux, embrouilles... Tout ce qui concerne la squad se passe ici.")\
\
    # Le bot envoie un message dans ALERTES\
    salon_alertes = bot.get_channel(ID_ALERTES)\
    if salon_alertes:\
        await salon_alertes.send("\uc0\u55357 \u56545  **Le Radar.**\\nSi un gars de la squad poireaute tout seul en vocal, le bot balancera un ping automatique ici pour qu'on le rejoigne.")\
\
    # Le bot envoie un message dans COMMANDES\
    salon_commandes = bot.get_channel(ID_COMMANDES)\
    if salon_commandes:\
        await salon_commandes.send("\uc0\u55358 \u56598  **Le Terminal.**\\nPour \'e9viter de polluer le QG, tapez toutes les commandes du bot ici.")\
\
    await ctx.send("\uc0\u9989  Boss, les messages de pr\'e9sentation ont \'e9t\'e9 envoy\'e9s dans tous les salons !")\
\
# Lancement du bot\
bot.run('MTUwNTI4MTc2NjYxOTg3MzMwMQ.GdJx5Y.frZqO31jbeAgRwNsRgu4yIUWVnXbRnSKA7FHj0')}