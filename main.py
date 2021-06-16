import os
import discord
from discord.utils import get
from random import randrange

class Player:
  def __init__(self, author, level):
    self.author = author
    self.level = level

class Match:
  def __init__(self, lobbyName, players):
    self.lobbyName = lobbyName
    self.players = players

client = discord.Client()
frases = [":flag_br:VOCÊ DISSE O PLANO???:flag_br:",
          ":flag_br:REPETE SE VC TIVER CORAGEM:flag_br:",
          ":flag_br:REPETE!!:flag_br:"]
players = []
level = ''
match = None

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  global match
  if message.author == client.user:
    return
  
  # 
  # !X5   
  #
  if message.content.startswith('!x5'):
    await message.channel.send("EU OUVI X5? :eyes: :eyes: :eyes:")
    await message.channel.send("**Comandos:**\n**!level {level}** => Digite para atribuir um level a você. Só é preciso digiar uma vez ou caso queira atualizar o seu level.\n**!create {nome}** => Criar lobby X5\n**!join {nomeDoX5}** => Entrar no X5\nAssim que a Lobby completar 10 jogadores, irei sortear os times!")

  # 
  # !LOBBY   
  #
  if message.content.startswith('!create'):
    lobbyName = message.content.split()[1]
    match = Match(lobbyName, [])
    await message.channel.send('Lobby ' + lobbyName + ' criada!')
    await message.channel.send('Digite **!join ' + lobbyName + '** para entrar no X5!')

  # 
  # !JOIN   
  #
  if message.content.startswith('!join'):
    lobbyName = message.content.split()[1]
  
    if match.lobbyName != lobbyName:
      await message.channel.send('X5 ainda não foi criado!\nDigite **!lobby {nome}** para criar um X5!')
      return
    
    if match.lobbyName == lobbyName:
      for role in message.author.roles:
        strRole = str(role)
        if "Level" in strRole:
          level = strRole.split()[1]
      match.players.append(Player(message.author, level))

      playersLeft = 10 - len(match.players)
      if playersLeft == 1:
        await message.channel.send('**' + str(len(match.players)) + ' Jogadores no X5! Falta ' + str(playersLeft) + '!**')
      elif playersLeft == 9:
        await message.channel.send('**' + str(len(match.players)) + ' Jogador no X5! Faltam ' + str(playersLeft) + '!**')
      elif playersLeft == 0:
        await message.channel.send(':boom:**X5 FECHADO!**:boom:\nSorteando times...')
      else:
        await message.channel.send('**' + str(len(match.players)) + ' Jogadores no X5! Faltam ' + str(playersLeft) + '!**')
      
    else:
      await message.channel.send('Nome da Lobby inválida!\nDigite **!lobby {nome}** para criar um X5!')

  # 
  # !LEVEL   
  #
  if message.content.startswith('!level'):
    member = message.author
    print(member)
    level = message.content.split()[1]

    if int(level) < 1 or int(level) > 20:
      await message.channel.send("ERRO! {}".format(message.author.mention) + " Digite um level válido! Desde quando tem level " + level + " na GC?")
    else:
      role = get(message.guild.roles, name='Level ' + level)
      await member.add_roles(role)
      await message.channel.send("{}".format(message.author.mention) + " é Level " + level + "!")

  # 
  # PLANO?   
  #
  if 'PLANO' in message.content.upper():
    num = randrange(len(frases))
    await message.channel.send(frases[num])


discordToken = os.environ['TOKEN']
client.run(discordToken)