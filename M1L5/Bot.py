import discord
from discord.ext import commands
from discord import app_commands
import random
import json
import os

TOKEN = "token"

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

# =========================================================
# Banco de dados simples
# =========================================================

DB_FILE = "eco_data.json"

if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

# =========================================================
# Dados do bot
# =========================================================

eco_tips = [
    "Use garrafas reutilizáveis.",
    "Evite plástico descartável.",
    "Desligue aparelhos sem uso.",
    "Use transporte público ou bicicleta.",
    "Recicle papel, vidro e plástico.",
    "Economize água ao escovar os dentes.",
]

facts = [
    "Mais de 8 milhões de toneladas de plástico chegam aos oceanos por ano.",
    "Uma lata de alumínio pode levar até 200 anos para se decompor.",
    "O Brasil possui uma das maiores biodiversidades do planeta.",
    "Reciclar economiza energia e reduz a poluição.",
]

quiz_questions = [
    {
        "question": "Qual gás é o principal responsável pelo aquecimento global?",
        "answer": "co2"
    },
    {
        "question": "Qual material demora mais para se decompor: papel ou plástico?",
        "answer": "plastico"
    },
    {
        "question": "Reciclar ajuda a reduzir a poluição? (sim/nao)",
        "answer": "sim"
    }
]

challenges = [
    "Fique 1 dia sem usar copos descartáveis.",
    "Recicle pelo menos 5 objetos hoje.",
    "Economize água durante o banho.",
    "Plante uma árvore ou cuide de uma planta.",
]

# =========================================================
# Evento inicial
# =========================================================

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Bot conectado como {bot.user}")

# =========================================================
# Comando: ajuda
# =========================================================

@bot.tree.command(name="ecohelp", description="Mostra os comandos do EcoGuard")
async def ecohelp(interaction: discord.Interaction):

    embed = discord.Embed(
        title="🌍 EcoGuard Commands",
        description="Comandos do bot ambiental",
        color=0x2ecc71
    )

    embed.add_field(name="/dica", value="Receba uma dica ecológica", inline=False)
    embed.add_field(name="/curiosidade", value="Curiosidade ambiental", inline=False)
    embed.add_field(name="/quiz", value="Quiz sobre poluição", inline=False)
    embed.add_field(name="/desafio", value="Desafio ecológico diário", inline=False)
    embed.add_field(name="/ecoacao", value="Registrar ação sustentável", inline=False)
    embed.add_field(name="/ranking", value="Ranking sustentável", inline=False)

    await interaction.response.send_message(embed=embed)

# =========================================================
# Dicas ecológicas
# =========================================================

@bot.tree.command(name="dica", description="Receba uma dica ecológica")
async def dica(interaction: discord.Interaction):

    tip = random.choice(eco_tips)

    embed = discord.Embed(
        title="♻️ Dica Ecológica",
        description=tip,
        color=0x27ae60
    )

    await interaction.response.send_message(embed=embed)

# =========================================================
# Curiosidades
# =========================================================

@bot.tree.command(name="curiosidade", description="Curiosidade sobre o meio ambiente")
async def curiosidade(interaction: discord.Interaction):

    fact = random.choice(facts)

    embed = discord.Embed(
        title="🌱 Curiosidade Ambiental",
        description=fact,
        color=0x16a085
    )

    await interaction.response.send_message(embed=embed)

# =========================================================
# Quiz
# =========================================================

@bot.tree.command(name="quiz", description="Quiz sobre poluição")
async def quiz(interaction: discord.Interaction):

    q = random.choice(quiz_questions)

    await interaction.response.send_message(
        f"🧠 Quiz:\n{q['question']}\n\nResponda no chat!"
    )

# =========================================================
# Desafio ecológico
# =========================================================

@bot.tree.command(name="desafio", description="Receba um desafio ecológico")
async def desafio(interaction: discord.Interaction):

    challenge = random.choice(challenges)

    embed = discord.Embed(
        title="🔥 Desafio Verde",
        description=challenge,
        color=0x1abc9c
    )

    await interaction.response.send_message(embed=embed)

# =========================================================
# Sistema de pontos ecológicos
# =========================================================

@bot.tree.command(
    name="ecoacao",
    description="Registrar uma ação sustentável"
)
@app_commands.describe(
    acao="Exemplo: reciclagem, bicicleta, economizar água"
)
async def ecoacao(interaction: discord.Interaction, acao: str):

    data = load_data()

    user_id = str(interaction.user.id)

    if user_id not in data:
        data[user_id] = {
            "name": interaction.user.name,
            "points": 0
        }

    data[user_id]["points"] += 10

    save_data(data)

    embed = discord.Embed(
        title="✅ Ação registrada",
        description=f"Você registrou: **{acao}**\n+10 EcoPoints 🌿",
        color=0x2ecc71
    )

    await interaction.response.send_message(embed=embed)

# =========================================================
# Ranking ecológico
# =========================================================

@bot.tree.command(name="ranking", description="Ranking sustentável")
async def ranking(interaction: discord.Interaction):

    data = load_data()

    if not data:
        await interaction.response.send_message(
            "Ainda não há participantes."
        )
        return

    ranking_list = sorted(
        data.items(),
        key=lambda x: x[1]["points"],
        reverse=True
    )

    embed = discord.Embed(
        title="🏆 Ranking Sustentável",
        color=0xf1c40f
    )

    for i, (user_id, info) in enumerate(ranking_list[:10], start=1):
        embed.add_field(
            name=f"{i}. {info['name']}",
            value=f"{info['points']} pontos 🌱",
            inline=False
        )

    await interaction.response.send_message(embed=embed)

# =========================================================
# Mensagens automáticas educativas
# =========================================================

@bot.event
async def on_message(message):

    if message.author.bot:
        return

    keywords = {
        "poluição": "A poluição afeta oceanos, florestas e cidades 🌍",
        "plástico": "Evite plástico descartável ♻️",
        "reciclagem": "Reciclar ajuda o planeta 🌱",
    }

    for word, response in keywords.items():
        if word in message.content.lower():
            await message.channel.send(response)

    await bot.process_commands(message)

# =========================================================
# Executar bot
# =========================================================

bot.run(TOKEN)
