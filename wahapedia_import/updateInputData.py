import requests
import os

if(not os.path.exists("./wahapedia")):
  os.mkdir("./wahapedia")

print("getting Abilities")
r = requests.get("https://wahapedia.ru/wh40k9ed/Abilities.csv")
with open("./wahapedia/Abilities.csv", "wb") as f:
  f.write(r.content)

print("getting Datasheets")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets.csv")
with open("./wahapedia/Datasheets.csv", "wb") as f:
  f.write(r.content)
  
print("getting Datasheets_abilities")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets_abilities.csv")
with open("./wahapedia/Datasheets_abilities.csv", "wb") as f:
  f.write(r.content)
  
print("getting Datasheets_damage")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets_damage.csv")
with open("./wahapedia/Datasheets_damage.csv", "wb") as f:
  f.write(r.content)
  
print("getting Datasheets_keywords")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets_keywords.csv")
with open("./wahapedia/Datasheets_keywords.csv", "wb") as f:
  f.write(r.content)
  
print("getting Datasheets_models")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets_models.csv")
with open("./wahapedia/Datasheets_models.csv", "wb") as f:
  f.write(r.content)
  
print("getting Datasheets_options")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets_options.csv")
with open("./wahapedia/Datasheets_options.csv", "wb") as f:
  f.write(r.content)
  
print("getting Datasheets_wargear")
r = requests.get("https://wahapedia.ru/wh40k9ed/Datasheets_wargear.csv")
with open("./wahapedia/Datasheets_wargear.csv", "wb") as f:
  f.write(r.content)
  
print("getting Factions")
r = requests.get("https://wahapedia.ru/wh40k9ed/Factions.csv")
with open("./wahapedia/Factions.csv", "wb") as f:
  f.write(r.content)
  
print("getting PsychicPowers")
r = requests.get("https://wahapedia.ru/wh40k9ed/PsychicPowers.csv")
with open("./wahapedia/PsychicPowers.csv", "wb") as f:
  f.write(r.content)
  
print("getting Source")
r = requests.get("https://wahapedia.ru/wh40k9ed/Source.csv")
with open("./wahapedia/Source.csv", "wb") as f:
  f.write(r.content)
  
print("getting Stratagems")
r = requests.get("https://wahapedia.ru/wh40k9ed/Stratagems.csv")
with open("./wahapedia/Stratagems.csv", "wb") as f:
  f.write(r.content)
  
print("getting Wargear")
r = requests.get("https://wahapedia.ru/wh40k9ed/Wargear.csv")
with open("./wahapedia/Wargear.csv", "wb") as f:
  f.write(r.content)
  
print("getting Wargear_list")
r = requests.get("https://wahapedia.ru/wh40k9ed/Wargear_list.csv")
with open("./wahapedia/Wargear_list.csv", "wb") as f:
  f.write(r.content)
  
print("getting Warlord_traits")
r = requests.get("https://wahapedia.ru/wh40k9ed/Warlord_traits.csv")
with open("./wahapedia/Warlord_traits.csv", "wb") as f:
  f.write(r.content)

print("done downloading files")