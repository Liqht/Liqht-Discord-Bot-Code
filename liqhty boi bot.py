import discord
import asyncio
import requests
import os
import json
import flask
import keep_alive
import random




TOKEN = "NjkyMTEzMjM2MjM2OTU5Nzg3.Xozhig.-zLgbhLgzwSRaCmCx2KUHoMXq_Q"
FortniteToken = '3a7d52ca-bc4f-48fd-98af-44a687eaf731'
HypixelToken = ['00b107dc-7cf1-4a49-be79-ea132d94f4c8']
client = discord.Client()
@client.event
async def on_message(message):
  if message.author == client.user:
    return
  if message.content=='.hello':
    msg = 'Hello {0.author.mention}. Did you know that the inventor Thomas Edison is the reason why people use hello? He was surprised by a phone and expressed this with a misheard “hullo”. Hello was first used in print in 1833 and became popular from the 1860s.'.format(message) 
    await message.channel.send(msg)

  if message.content=='.minecraft':
    msg = 'Minecraft is a sandbox video game developed by Mojang. Minecraft was created by Markus "Notch" Persson in the Java programming language and was released as a public alpha for personal computers in 2009 before officially releasing in November 2011, with Jens Bergensten taking over development around then. It has since been ported to various platforms and is the bestselling video game of all time, with over 180 million copies sold across all platforms and over 112 million monthly active players by 2019.'
    await message.channel.send(msg)

  if message.content=='.fortnite':
    msg = 'Fortnite is an online video game developed by Epic Games and released in 2017. It is available in three distinct game mode versions that otherwise share the same general gameplay and game engine: Fortnite: Save the World, a cooperative shooter-survival game for up to four players to fight off zombie-like creatures and defend objects with fortifications they can build; Fortnite Battle Royale, a free-to-play battle royale game where up to 100 players fight to be the last person standing; and Fortnite Creative, where players are given complete freedom to create worlds and battle arenas. The first two-game modes were released in 2017 as early access titles and Creative was released on December 6, 2018. Save the World is available only for Windows, macOS, PlayStation 4, and Xbox One, while Battle Royale and Creative released for those platforms, in addition for Nintendo Switch, iOS and Android devices.'
    await message.channel.send(msg)

  if message.content=='.ping':
    msg = 'Pong!'
    await message.channel.send(msg)

  if message.content=='.beep':
    msg = 'Boop!'
    await message.channel.send(msg)

  if message.content=='.help':
    embed = discord.Embed(title = "All Commmands", color = 0xff9100)
    embed.add_field(name = "Hello", value=".hello" + '\n', inline = False)
    embed.add_field(name = "Goodbye", value=".goodbye" + '\n', inline = False)
    embed.add_field(name = "What's Minecraft?", value=".minecraft" + '\n', inline = False)
    embed.add_field(name = "What's Fortnite?", value=".fortnite" + '\n', inline = False)
    embed.add_field(name = "Boop!", value=".beep" + '\n', inline = False)
    embed.add_field(name = "Pong!", value=".ping" + '\n', inline = False)
    embed.add_field(name = "Fotrnite Stats (v1)", value=".fstats {platform} {name}" + '\n', inline = False)
    embed.add_field(name = "Hypixel Stats (in progress)", value=".hstats {name} {gamemode}" + '\n', inline = False)
    
    await message.channel.send (embed = embed)
    

  if message.content=='.goodbye':
    msg = 'Goodbye! Cya later, alligator. In a while, crocodile. Catch ya later! Peace out! Toodles! Until next time! Adios, amigos! Farewell! '
    await message.channel.send(msg)



  if message.content.startswith('.fstats'):
    #splits message in half. first is .fortnitestats, second half is username
    words = message.content.split(' ', 2)
    if len(words) < 3:
      await message.channel.send("Not valid command")
      return
    console = words[1].strip().lower()
    
    if console == 'xbox':
      console = 'xbl'
    if console == 'ps4':
      console = 'psn'
    if console != 'pc' and console != 'xbl' and console != 'psn':
      await message.channel.send("Not valid platform/input")
      return
    else:
      res = fortnite_tracker_api(console, words[2])
      if res:
        matches_played = res[0]['value']
        wins = res[1]['value']
        wins_percent = res[2]['value']
        kills = res[3]['value']
        kd = res[4]['value']

        embed = discord.Embed(title = "Lifetime Stats for " + words[2], color = 0x02d5fa)

        embed.add_field(name = "MatchesPlayed", value=matches_played + '\n', inline = False)
        embed.add_field(name = "Wins", value = wins + '\n',  inline = False)
        embed.add_field(name = "Wins percent", value = wins_percent + '\n',  inline = False)
        embed.add_field(name = "Kills", value = kills + '\n',  inline = False)
        embed.add_field(name = "K/D", value = kd + '\n',  inline = False)
        await message.channel.send (embed = embed)
      else:
        await message.channel.send ('Failed to obtain data. Confirm player is not banned, has played a game, or does not have private on.')




  if message.content.startswith('.hstats'):
   words = message.content.split(" ", 2)
   if len(words) < 3:
     words.append("")
   name = words[1].strip()
   print(name)
   data = requests.get("https://api.hypixel.net/player?key=00b107dc-7cf1-4a49-be79-ea132d94f4c8&name=" + name).json()
   x=json.dumps (data, indent=4)
   f = open("file1.txt","w" )
   f.write(x)
   f.close()
   if len(words[2].strip()) == 0:
     gamename = "General"
   else:
     gamename = words[2].strip()
   if gamename.lower() == "skywars":
     gamename ="SkyWars"
   elif gamename.lower() == "bedwars":
     gamename ="Bedwars"
   elif gamename.lower() == "pit":
     gamename ="Pit"
   elif gamename.lower() == "buildbattle":
     gamename ="BuildBattle"
   elif gamename.lower() == "duels":
     gamename ="Duels"
   elif gamename.lower() == "murderymystery":
     gamename ="MurderMystery"
   elif gamename.lower() == "arcade":
     gamename ="Arcade"
   

   embed = discord.Embed(title = ""+ gamename + " Stats for " + data["player"]["displayname"], color = 0x10c942)
   if gamename == "general":
    if "rank" in data["player"] and data["player"]["rank"] != "NORMAL":
      rank = data["player"]["rank"]
    elif "newPackageRank" in data["player"]:
      rank = data["player"]["newPackageRank"]
    elif "packageRank" in data["player"]:
      rank = data["player"]["packageRank"]
    else:
      rank = "Non-Donor"
    print(rank)

    embed.add_field(name = "Rank", value = rank + '\n', inline = False)
    karma = data["player"]["karma"] if "karma" in data["player"] else 0
    print(str(karma))
    print(rank)

    embed.add_field(name = "Karma", value = str(karma) + '\n', inline = False)
    await message.channel.send (embed = embed)
    return
   stats = data["player"]["stats"][gamename]
   

   if "games_played" in stats:
     games_played = stats["games_played"]
   elif "games_played_" + gamename.lower() in stats:
     games_played = stats["games_played_" + gamename.lower()]
   else:
     games_played = "none"
   embed.add_field(name = "Matches Played", value = str(games_played) + '\n', inline = False)


   if gamename.lower() == "skywars":
     print()
     embed.add_field(name= "Wins", value= str(stats["wins"] ) +"\n" , inline = False)
     embed.add_field(name= "Losses", value= str(stats["losses"] ) +"\n" , inline = False)
     embed.add_field(name= "Win Streak", value= str(stats["win_streak"] ) +"\n" , inline = False)
     embed.add_field(name= "Kills", value= str(stats["kills"] ) +"\n" , inline = False)
     embed.add_field(name= "Tokens", value= str(stats["cosmetic_tokens"] ) +"\n" , inline = False)
     embed.add_field(name= "Coins", value= str(stats["coins"] ) +"\n" , inline = False)
     await message.channel.send (embed = embed)
     return

   elif gamename.lower() == "bedwars":
     print()
     embed.add_field(name= "Wins", value= str(stats["wins_bedwars"] ) +"\n" , inline = False)
     embed.add_field(name= "Losses", value= str(stats["losses_bedwars"] ) +"\n" , inline = False)
     embed.add_field(name= "Win Streak", value= str(stats["winstreak"] ) +"\n" , inline = False)
     embed.add_field(name= "Kills", value= str(stats["kills_bedwars"] ) +"\n" , inline = False)
     embed.add_field(name= "Final Kills", value= str(stats["final_kills_bedwars"] ) +"\n" , inline = False)
     embed.add_field(name= "Beds Broken", value= str(stats["beds_broken_bedwars"] ) +"\n" , inline = False)
     embed.add_field(name= "Deaths", value= str(stats["deaths_bedwars"] ) +"\n" , inline = False)
     embed.add_field(name= "Coins", value= str(stats["coins"] ) +"\n" , inline = False)
     await message.channel.send (embed = embed)
     return

   elif gamename.lower() == "pit":
     print()
     embed.add_field(name= "Kills", value= str(stats["pit_stats_ptl"]["kills"] ) +"\n" , inline = False)
     embed.add_field(name= "Deaths", value= str(stats["pit_stats_ptl"]["deaths"] ) +"\n" , inline = False)
     embed.add_field(name= "Assists", value= str(stats["pit_stats_ptl"]["assists"] ) +"\n" , inline = False)
     embed.add_field(name= "Highest Kill Streak", value= str(stats["pit_stats_ptl"]["max_streak"] ) +"\n" , inline = False)
     embed.add_field(name= "Gold", value= str(stats["profile"]["cash"] ) +"\n" , inline = False)
     embed.add_field(name= "Renown", value= str(stats["profile"]["renown"] ) +"\n" , inline = False)

     if "prestiges" in stats["profile"]:
       prestige = stats["profile"]["prestiges"]
       p = prestige[len(prestige) -1 ]["index"]
       embed.add_field(name= "Prestige", value= str(p) +"\n" , inline = False)
     else: 
      embed.add_field(name= "Prestige", value= "0" +"\n" , inline = False)
     await message.channel.send (embed = embed)
     return

   elif gamename.lower() == "buildbattle":
     print()
     embed.add_field(name= "Wins", value= str(stats["wins"] ) +"\n" , inline = False)
     embed.add_field(name= "Coins", value= str(stats["coins"] ) +"\n" , inline = False)
     embed.add_field(name= "Score", value= str(stats["score"] ) +"\n" , inline = False)
     await message.channel.send (embed = embed)
     return

   elif gamename.lower() == "murderymystery":
     print()
     embed.add_field(name= "Wins", value= str(stats["wins"] ) +"\n" , inline = False)
     embed.add_field(name= "Deaths", value= str(stats["deaths"] ) +"\n" , inline = False)
     embed.add_field(name= "Kills", value= str(stats["kills"] ) +"\n" , inline = False)
     embed.add_field(name= "Coins", value= str(stats["coins"] ) +"\n" , inline = False)
     await message.channel.send (embed = embed)
     return
   elif gamename.lower() == "arcade":
     print()
     embed.add_field(name= "Coins", value= str(stats["coins"] ) +"\n" , inline = False)
     embed.add_field(name= "Farm Hunt Wins", value= str(stats["wins_farm_hunt"] ) +"\n" , inline = False)
     embed.add_field(name= "Mini Walls Wins", value= str(stats["wins_mini_walls"] ) +"\n" , inline = False)
     embed.add_field(name= "Soccer Wins", value= str(stats["wins_soccer"] ) +"\n" , inline = False)
     embed.add_field(name= "Party Games Wins", value= str(stats["wins_party"] ) +"\n" , inline = False)
     embed.add_field(name= "Hypixel Says Wins", value= str(stats["wins_simon_says"] ) +"\n" , inline = False)
     await message.channel.send (embed = embed)
     return


   elif gamename.lower() == "duels":
     print()
     page1 = discord.Embed(title = ""+ gamename + " Stats for " + data["player"]["displayname"], color = 0x10c942)
     page1.add_field(name = "Wins", value= str(stats["wins"] ) +"\n" , inline = False)
     page1.add_field(name = "Kills", value= str(stats["kills"] ) +"\n" , inline = False)
     page1.add_field(name = "Losses", value= str(stats["losses"] ) +"\n" , inline = False)
     page1.add_field(name = "Deaths", value= str(stats["deaths"] ) +"\n" , inline = False)
     page1.add_field(name = "Melee Swings", value= str(stats["melee_swings"] ) +"\n" , inline = False)
     page1.add_field(name = "Melee Hits", value= str(stats["melee_hits"] ) +"\n" , inline = False)
     page1.add_field(name = "Bow Shots", value= str(stats["bow_shots"] ) +"\n" , inline = False)
     page1.add_field(name = "Bow Hits", value= str(stats["bow_hits"] ) +"\n" , inline = False)
     page1.add_field(name = "Damage Dealt", value= str(stats["damage_dealt"] ) +"\n" , inline = False)
     page1.add_field(name = "Rounds Played", value= str(stats["rounds_played"] ) +"\n" , inline = False)

     page2 = discord.Embed(title = ""+ gamename + " Stats for " + data["player"]["displayname"], color = 0x10c942)
     page2.add_field(name = "UHC Wins", value= str(stats["uhc_duel_wins"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Kills", value= str(stats["uhc_duel_kills"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Losses", value= str(stats["uhc_duel_losses"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Deaths", value= str(stats["uhc_duel_deaths"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Melee Swings", value= str(stats["uhc_duel_melee_swings"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Melee Hits", value= str(stats["uhc_duel_melee_hits"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Bow Shots", value= str(stats["uhc_duel_bow_shots"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Bow Hits", value= str(stats["uhc_duel_bow_hits"] ) +"\n" , inline = False)
     page2.add_field(name = "UHC Damage Dealt", value= str(stats["uhc_duel_damage_dealt"] ) +"\n" , inline = False)
     
    
     pages = [page1, page2]
     await message.channel.send(embed = page1)
     m = message.channel.last_message

 
     await m.add_reaction('\u25c0')
     await m.add_reaction('\u25b6')
     await m.add_reaction('\u25b6')

     

     i = 0
     emoji = ''
     
     while True:
        if emoji=='\u25c0':
            if i>0:
                i-=1
                await m.edit(embed=pages[i])
        if emoji=='\u25b6':
            if i<2:
                i+=1
                await m.edit(embed=pages[i])

        res=await client.wait_for("reaction_add", check = on_reaction_add)
        print(res)
        if res==None:
            break
        if str(res[1])!='<Bots name goes here>': #Example: 'MyBot#1111'
            emoji=str(res[0].emoji)
            await m.remove_reaction(res[0].emoji,res[1])

     await m.clear_reactions()

   


#def scaffold(guesses, word):
#  if guesses == 0:
#    print"__________"
#    print"|      |"
#    print"|"
#    print"|"
#    print"|"
#    print"|"
#    print"|_________"
#  elif guesses == 1:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|"
#    print"|"
#    print"|"
#    print"|_________"
#  elif guesses == 2:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|      |"
#    print"|"
#    print"|"
#    print"|_________"
#  elif guesses == 3:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|     /|"
#    print"|"
#    print"|"
#    print"|_________"
# elif guesses == 4:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|     /|\"
#    print"|"
#    print"|"
#    print"|_________"
#  elif guesses == 5:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|     /|\"
#    print"|      |"
#    print"|"
#    print"|_________"
#  elif guesses == 6:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|     /|\"
#    print"|      |"
#    print"|     /"
#    print"|_________"
#  elif guesses == 7:
#    print"__________"
#    print"|      |"
#    print"|      0"
#    print"|     /|\"
#    print"|      |"
#    print"|     / \"
#    print"|_________"

#    print"\n"
#    print"word is %s." %wd
#    print"\n"
#    print"\nyou lose"
#    print"\nwould you like to play again? type 1 for yes and 2 for no.
#    again = str(raw_input(">"))
#    again = again.low()
#    if again == "1":
#      handman()
    #return



def fortnite_tracker_api(platform, username):
  URL = 'https://api.fortnitetracker.com/v230/profile/' + platform + '/' + username
  req = requests.get(URL, headers = {"TRN-Api-Key":FortniteToken})
  if req.status_code == 200:
    try:
      print(req.json())
      lifetime_stats = req.json()['lifeTimeStats']
      return lifetime_stats[7:]
    except KeyError:
      return False
  else:
    return False





@client.event
async def on_reaction_add(reaction, user):
  if (user==client.user):
    return False
  return reaction=="\u25c0" or reaction=="\u25b6"
  
@client.event
async def on_ready():
  print(client.user.name)
  print("is online")
  
keep_alive.keep_alive()
client.run(TOKEN)