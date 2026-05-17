import discord
from discord.ext import commands, tasks
import random
import os
import asyncio
import datetime
from aiohttp import web

# Activation des permissions (y compris les statuts pour les jeux)
intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True
intents.presences = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# IDs de l'OMERTA
ID_BIENVENUE = 1505275545812860950
ID_MESSAGES = 1505275843830878289
ID_ALERTES = 1505278942737731707
ID_COMMANDES = 1505279169079152721

# Dictionnaire pour stocker les anniversaires (Format: {ID: "JJ/MM"})
anniversaires = {}

# ==========================================
# LE LEURRE POUR RENDER (Anti-Crash)
# ==========================================
async def handle_web(request):
    return web.Response(text="L'OMERTA tourne H24.")
async def web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle_web)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()

# ==========================================
# DÉMARRAGE DU BOT
# ==========================================
@bot.event
async def on_ready():
    bot.loop.create_task(web_server()) # Lance le faux site pour Render
    check_anniversaires.start()        # Lance le radar d'anniversaires
    await bot.change_presence(activity=discord.Game(name="Protéger la Squad"))
    print("---------------------------------")
    print(f"🔥 L'OMERTA EST EN PLACE ! {bot.user.name} est connecté.")
    print("---------------------------------")

# ==========================================
# 1. ACCUEIL ET GESTION
# ==========================================
@bot.event
async def on_member_join(member):
    salon_bienvenue = bot.get_channel(ID_BIENVENUE)
    if salon_bienvenue:
        msgs = [
            f"{member.mention} ce gros charo est arrivé.",
            f"Merde, {member.mention} est là.",
            f"{member.mention} EST LA🔥.",
            f"{member.mention} est là (allo selem il est pas sélectionné).",
            f"Yo le frro {member.mention}"
        ]
        await salon_bienvenue.send(random.choice(msgs))

@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int = 5):
    """Efface les messages (ex: !clear 10)"""
    await ctx.channel.purge(limit=amount + 1)
    msg = await ctx.send(f"🧹 **{amount} messages** ont été balayés par l'OMERTA.")
    await asyncio.sleep(3)
    await msg.delete()

# ==========================================
# 2. GAMING & VOCAL (MULTI-JEUX)
# ==========================================
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if len(after.channel.members) == 1:
            salon = bot.get_channel(ID_ALERTES)
            if salon:
                await salon.send(f"🚨 {member.mention} t'attend en vocal dans **{after.channel.name}** !")

@bot.event
async def on_presence_update(before, after):
    if not before.activity and after.activity:
        if after.activity.name:
            jeu = after.activity.name.lower()
            
            # Liste des jeux surveillés par l'OMERTA
            jeux_de_la_squad = [
                "roblox", 
                "8 ball pool", 
                "fc 26", 
                "ea sports fc 26", 
                "gta v", 
                "grand theft auto v", 
                "minecraft", 
                "fortnite", 
                "supermarket together"
            ]
            
            if jeu in jeux_de_la_squad:
                salon = bot.get_channel(ID_MESSAGES)
                if salon:
                    await salon.send(f"🎮 **Alerte Gaming :** {after.mention} vient de lancer **{after.activity.name}** ! Rejoignez-le !")

@bot.command()
async def squad(ctx):
    """Appel aux armes général"""
    await ctx.send(f"⚠️ **RassembleMENT OMERTA !** @everyone {ctx.author.mention} veut lancer une session maintenant !")

# ==========================================
# 3. SONDAGES
# ==========================================
@bot.command()
async def sondage(ctx, *, question):
    """Crée un sondage stylé (ex: !sondage On lance un tournoi ?)"""
    embed = discord.Embed(title="📊 Sondage OMERTA", description=question, color=0x2b2d31)
    embed.set_footer(text=f"Sondage lancé par {ctx.author.display_name}")
    
    await ctx.message.delete()
    msg = await ctx.send(embed=embed)
    
    await msg.add_reaction("✅")
    await msg.add_reaction("❌")

# ==========================================
# 4. ANNIVERSAIRES
# ==========================================
@bot.command()
async def setanniv(ctx, date: str):
    """Enregistre ton anniversaire (ex: !setanniv 15/04)"""
    try:
        jour, mois = date.split("/")
        if 1 <= int(jour) <= 31 and 1 <= int(mois) <= 12:
            anniversaires[ctx.author.id] = f"{int(jour):02d}/{int(mois):02d}"
            await ctx.send(f"🎂 C'est noté boss ! L'OMERTA n'oubliera pas ton anniv le **{anniversaires[ctx.author.id]}**.")
        else:
            await ctx.send("❌ Date invalide. Utilise `!setanniv JJ/MM` (ex: 15/04).")
    except:
        await ctx.send("❌ Format invalide. Utilise `!setanniv JJ/MM` (ex: 15/04).")

@tasks.loop(hours=24)
async def check_anniversaires():
    # Fuseau horaire UTC+1 (Heure de Tunis)
    tz = datetime.timezone(datetime.timedelta(hours=1))
    now = datetime.datetime.now(tz)
    date_jour = f"{now.day:02d}/{now.month:02d}"
    
    salon_qg = bot.get_channel(ID_MESSAGES)
    if not salon_qg: return
    
    for user_id, date_anniv in anniversaires.items():
        if date_anniv == date_jour:
            user = bot.get_user(user_id)
            if user:
                await salon_qg.send(f"🎉 **ALERTE GÉNÉRALE !** 🎉\nAujourd'hui c'est l'anniversaire de {user.mention} ! La squad, faites du bruit !")

@check_anniversaires.before_loop
async def before_check():
    await bot.wait_until_ready()
    tz = datetime.timezone(datetime.timedelta(hours=1))
    now = datetime.datetime.now(tz)
    futur = now.replace(hour=0, minute=0, second=0, microsecond=0)
    if now >= futur:
        futur += datetime.timedelta(days=1)
    attente = (futur - now).total_seconds()
    await asyncio.sleep(attente)

# ==========================================
# 5. DÉLIRES & UTILITAIRES
# ==========================================
@bot.command()
async def food(ctx):
    plats = ["un bon Tacos bien lourd", "un gros Burger", "une Pizza au thon"]
    boissons = ["un Coca bien frais 🥤", "un Fanta 🍊", "une Boga 🍏"]
    await ctx.send(f"🍔 **Le boss ne sait pas quoi manger ?**\nCe soir l'OMERTA a tranché : **{random.choice(plats)}**, (sans tomates, sans laitue et sans laitage) ! Et pour faire passer ça, **{random.choice(boissons)}**.")

@bot.command()
async def pileouface(ctx):
    await ctx.send(random.choice(["🪙 **Pile !**", "🪙 **Face !**"]))

@bot.command()
async def des(ctx):
    await ctx.send(f"🎲 Le dé roule et s'arrête sur le... **{random.randint(1, 6)}** !")

@bot.command()
async def remind(ctx, minutes: int, *, message):
    await ctx.send(f"⏰ C'est noté. Je te rappelle dans **{minutes} minutes** !")
    await asyncio.sleep(minutes * 60)
    await ctx.send(f"🔔 **RAPPEL pour {ctx.author.mention} :** {message}")

bot.run(os.environ.get('DISCORD_TOKEN'))
