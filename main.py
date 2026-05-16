import discord
from discord.ext import commands
import random
import os

intents = discord.Intents.default()
intents.members = True
intents.voice_states = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

ID_BIENVENUE = 1505275545812860950
ID_MESSAGES = 1505275843830878289
ID_ALERTES = 1505278942737731707
ID_COMMANDES = 1505279169079152721

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Surveiller l'OMERTA"))
    print("---------------------------------")
    print(f"🔥 L'OMERTA EST EN PLACE ! {bot.user.name} est connecté.")
    print("---------------------------------")

@bot.event
async def on_member_join(member):
    salon_bienvenue = bot.get_channel(ID_BIENVENUE)
    if salon_bienvenue:
        messages_bienvenue = [
            f"{member.mention} ce gros charo est arrivé.",
            f"Merde, {member.mention} est là.",
            f"{member.mention} EST LA🔥.",
            f"{member.mention} est là (allo selem il est pas sélectionné).",
            f"Yo le frro {member.mention}"
        ]
        message_choisi = random.choice(messages_bienvenue)
        await salon_bienvenue.send(message_choisi)

@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel is None and after.channel is not None:
        if len(after.channel.members) == 1:
            salon_alertes = bot.get_channel(ID_ALERTES)
            if salon_alertes:
                await salon_alertes.send(f"🚨 {member.mention} t'attend en vocal dans **{after.channel.name}** !")

@bot.command()
async def setup(ctx):
    salon_bienvenue = bot.get_channel(ID_BIENVENUE)
    if salon_bienvenue:
        await salon_bienvenue.send("🛑 **Poste de contrôle.**\nC'est ici que l'OMERTA surveille les allées et venues. Pas de blabla, le bot notifie juste quand l'un de vous débarque.")

    salon_messages = bot.get_channel(ID_MESSAGES)
    if salon_messages:
        await salon_messages.send("💬 **Le QG.**\nDiscussions générales, délires, jeux, embrouilles... Tout ce qui concerne la squad se passe ici.")

    salon_alertes = bot.get_channel(ID_ALERTES)
    if salon_alertes:
        await salon_alertes.send("📡 **Le Radar.**\nSi un gars de la squad poireaute tout seul en vocal, le bot balancera un ping automatique ici pour qu'on le rejoigne.")

    salon_commandes = bot.get_channel(ID_COMMANDES)
    if salon_commandes:
        await salon_commandes.send("🤖 **Le Terminal.**\nPour éviter de polluer le QG, tapez toutes les commandes du bot ici.")

    await ctx.send("✅ Boss, les messages de présentation ont été envoyés dans tous les salons !")

bot.run(os.environ.get('DISCORD_TOKEN'))
