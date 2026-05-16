import discord
from discord.ext import commands
import random
import os
import asyncio

# On active toutes les permissions, y compris les statuts pour détecter Roblox
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True
intents.presences = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# ----------------------------------------------------
# CONFIGURATION DES IDS (OMERTA)
# ----------------------------------------------------
ID_BIENVENUE = 1505275545812860950
ID_MESSAGES = 1505275843830878289
ID_ALERTES = 1505278942737731707
ID_COMMANDES = 1505279169079152721
ROLE_SQUAD_ID = 1505275200000000000  # Remplace par ton ID de rôle si tu en as créé un

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Protéger la Squad"))
    print("---------------------------------")
    print(f"🔥 L'OMERTA EST EN PLACE ! {bot.user.name} est connecté.")
    print("---------------------------------")

# ==========================================
# 1. ACCUEIL ET GESTION DE BASE
# ==========================================
@bot.event
async def on_member_join(member):
    # Rôle automatique
    role = member.guild.get_role(ROLE_SQUAD_ID)
    if role:
        try:
            await member.add_roles(role)
        except:
            pass

    # Message de bienvenue
    salon_bienvenue = bot.get_channel(ID_BIENVENUE)
    if salon_bienvenue:
        messages_bienvenue = [
            f"{member.mention} ce gros charo est arrivé.",
            f"Merde, {member.mention} est là.",
            f"{member.mention} EST LA🔥.",
            f"{member.mention} est là (allo selem il est pas sélectionné).",
            f"Yo le frro {member.mention}"
        ]
        await salon_bienvenue.send(random.choice(messages_bienvenue))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Efface les derniers messages (ex: !clear 10)"""
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 **{amount} messages** ont été balayés par l'OMERTA.")
    await asyncio.sleep(3)
    await msg.delete()

# ==========================================
# 2. EXPÉRIENCE VOCALE ET GAMING
# ==========================================
@bot.event
async def on_voice_state_update(member, before, after):
    # Radar vocal : alerte quand quelqu'un attend seul
    if before.channel is None and after.channel is not None:
        if len(after.channel.members) == 1:
            salon_alertes = bot.get_channel(ID_ALERTES)
            if salon_alertes:
                await salon_alertes.send(f"🚨 {member.mention} t'attend en vocal dans **{after.channel.name}** !")

@bot.event
async def on_presence_update(before, after):
    # Détection d'activité Gaming (Ex: Roblox)
    if not before.activity and after.activity:
        if after.activity.name and after.activity.name.lower() == "roblox":
            salon_qg = bot.get_channel(ID_MESSAGES)
            if salon_qg:
                await salon_qg.send(f"🎮 **Alerte Gaming :** {after.mention} vient de lancer Roblox ! Rejoignez-le !")

@bot.command()
async def squad(ctx):
    """Appel aux armes pour organiser une session instantanée"""
    await ctx.send(f"⚠️ **RassembleMENT OMERTA !** @everyone {ctx.author.mention} veut lancer une session maintenant ! Ramenez-vous en vocal !")

# ==========================================
# 3. COMMANDES DÉLIRE ET UTILITAIRES
# ==========================================
@bot.command()
async def food(ctx):
    """Le décideur de menu quand personne ne sait quoi commander"""
    plats = [
        "un bon Tacos bien lourd", 
        "un gros Burger", 
        "une Pizza au thon"
    ]
    boissons = ["un Coca bien frais 🥤", "un Fanta 🍊", "une Boga 🍏"]
    
    choix_plat = random.choice(plats)
    choix_boisson = random.choice(boissons)
    
    await ctx.send(f"🍔 **Le boss ne sait pas quoi manger ?**\nCe soir l'OMERTA a tranché : **{choix_plat}**, (évidemment sans tomates, sans laitue et sans laitage) ! Et pour faire passer ça, **{choix_boisson}**.")

@bot.command()
async def pileouface(ctx):
    """Pour régler les choix difficiles"""
    resultat = random.choice(["🪙 **Pile !**", "🪙 **Face !**"])
    await ctx.send(resultat)

@bot.command()
async def des(ctx):
    """Lance de dé à 6 faces"""
    await ctx.send(f"🎲 Le dé roule et s'arrête sur le... **{random.randint(1, 6)}** !")

@bot.command()
async def remind(ctx, minutes: int, *, message):
    """Système de rappels (ex: !remind 10 aller manger)"""
    await ctx.send(f"⏰ C'est noté. Je te rappelle dans **{minutes} minutes** !")
    await asyncio.sleep(minutes * 60)
    await ctx.send(f"🔔 **RAPPEL pour {ctx.author.mention} :** {message}")

# ==========================================
# DÉMARRAGE DU BOT
# ==========================================
bot.run(os.environ.get('DISCORD_TOKEN'))
