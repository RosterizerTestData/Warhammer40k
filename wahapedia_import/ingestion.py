import mysql.connector
from mysql.connector import errorcode
import re
import config
import csv

try:
  db = mysql.connector.connect(
    host=config.host,
    user=config.user,
    passwd=config.passwd,
    database=config.database
  )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cur = db.cursor(named_tuple=True)
  
  try:
    with open('wahapediaSetupDatabase.sql',mode='r') as f:
      resItr = cur.execute(f.read(), multi=True)
      for res in resItr:
        print("Running query: ", res)
        print(f"Affected {res.rowcount} rows" )
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to load wahapediaSetupDatabase.sql")
    
  
  # ORDER OF DATA INSERTION
  # sources;
  # factions;
  # wargear;
  # wargear_list;
  # datasheets;
  # abilities;
  # datasheets_abilities;
  # psychic_powers;
  # warlord_traits;
  # strategems;
  # datasheets_damage;
  # datasheets_keywords;
  # datasheets_models;
  # datasheets_options;
  # datasheets_wargear;
  
  # all the data has an unused column at the end, which is why every processor cuts off the last column
  # MySQL doesn't have the boolean datatype, we're using INT with 1 = true, 0 = false, -1 = data input error
  print("\nSOURCES")
  try:
    with open("wahapedia/Source.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["source_id"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "edition"):
          indexer["edition"] = i
        elif(column == "version"):
          indexer["version"] = i
        elif(column == "errata_date"):
          indexer["errata_date"] = i
        elif(column == "errata_link"):
          indexer["errata_link"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO sources (source_id, name, type, edition, version, errata_date, errata_link) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["source_id"]] if row[indexer["source_id"]] != '' else None, # source_id
          row[indexer["name"]] if row[indexer["name"]] != '' else None, # name
          row[indexer["type"]] if row[indexer["type"]] != '' else None, # type
          row[indexer["edition"]] if row[indexer["edition"]] != '' else None, # edition
          row[indexer["version"]] if row[indexer["version"]] != '' else None, # version
          row[indexer["errata_date"]] if row[indexer["errata_date"]] != '' else None, # errata_date
          row[indexer["errata_link"]] if row[indexer["errata_link"]] != '' else None, # errata_link
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into sources")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Source.csv")
    
  print("\nFACTIONS")
  try:
    with open("wahapedia/Factions.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["faction_id"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "link"):
          indexer["link"] = i
        elif(column == "is_subfaction"):
          indexer["is_subfaction"] = i
        i = i + 1
      
      primary_factions = {}
      
      query = "INSERT IGNORE INTO factions (faction_id, name, link, is_subfaction, main_faction_id) VALUES "
      data = []
      for row in csvF:
        
        main_faction_id = None
        if(re.sub('/.*$', '', re.sub('https://wahapedia.ru/wh40k9ed/factions/','',row[indexer["link"]])) == re.sub('[^0-9a-zA-Z]+', '-', row[indexer["name"]].lower())):
          main_faction_id = row[indexer["faction_id"]]
          primary_factions[row[indexer["link"]]] = main_faction_id
          
        query+="(%s,%s,%s,%s,%s),"
        # data has duplicate information
        data = data + [
          row[indexer["faction_id"]] if row[indexer["faction_id"]] != '' else None, # faction_id
          row[indexer["name"]] if row[indexer["name"]] != '' else None, # name
          row[indexer["link"]] if row[indexer["link"]] != '' else None, # link
          row[indexer["is_subfaction"]] if row[indexer["is_subfaction"]] != '' else None, # link
          main_faction_id, # effectively foreign key to this table's faction_id
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into factions")
      db.commit()
      
      # updating non primary_factions with their associated primary_faction's faction_id
      cur.execute("UPDATE factions f1 INNER JOIN factions f2 ON f1.link LIKE CONCAT(f2.link, '%') SET f1.main_faction_id = f2.main_faction_id WHERE f2.main_faction_id IS NOT NULL;")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Factions.csv")
  
  print("\nWARGEAR")
  try:
    with open("wahapedia/Wargear.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["wargear_id"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "description"):
          indexer["description"] = i
        elif(column == "is_relic"):
          indexer["is_relic"] = i
        elif(column == "faction_id"):
          indexer["faction_id"] = i
        elif(column == "legend"):
          indexer["legend"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO wargear (wargear_id, name, type, description, is_relic, faction_id, legend) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s),"
        # data has unused column
        data = data + [
          row[indexer["wargear_id"]] if row[indexer["wargear_id"]] != '' else None, # wargear_id
          row[indexer["name"]] if row[indexer["name"]] != '' else None, # name
          row[indexer["type"]] if row[indexer["type"]] != '' else None, # type
          row[indexer["description"]] if row[indexer["description"]] != '' else None, # description
          1 if row[indexer["is_relic"]] == "true" else 0 if row[indexer["is_relic"]] == "false" else -1, # is_relic, boolean
          row[indexer["faction_id"]] if row[indexer["faction_id"]] != '' else None, # faction_id
          row[indexer["legend"]] if row[indexer["legend"]] != '' else None, # legend
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into wargear")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Wargear.csv")
  
  print("\nWARGEAR LIST")
  try:
    with open("wahapedia/Wargear_list.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      query = "INSERT IGNORE INTO wargear_list (wargear_id, line, name, weapon_range, type, strength, armor_piercing, damage, abilities) VALUES "
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "wargear_id"):
          indexer["wargear_id"] = i
        elif(column == "line"):
          indexer["line"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "Range"):
          indexer["weapon_range"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "S"):
          indexer["strength"] = i
        elif(column == "AP"):
          indexer["armor_piercing"] = i
        elif(column == "D"):
          indexer["damage"] = i
        elif(column == "abilities"):
          indexer["abilities"] = i
        i = i + 1
      
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["wargear_id"]] if row[indexer["wargear_id"]] != '' else None, # wargear_id
          row[indexer["line"]] if row[indexer["line"]] != '' else None, # line
          row[indexer["name"]] if row[indexer["name"]] != '' else None, # name
          row[indexer["weapon_range"]].replace('"', '″') if row[indexer["weapon_range"]] != '' else None, # weapon_range
          row[indexer["type"]] if row[indexer["type"]] != '' else None, # type
          row[indexer["strength"]] if row[indexer["strength"]] != '' else None, # strength
          row[indexer["armor_piercing"]] if row[indexer["armor_piercing"]] != '' else None, # armor_piercing
          row[indexer["damage"]] if row[indexer["damage"]] != '' else None, # damage
          row[indexer["abilities"]] if row[indexer["abilities"]] != '' else None, # abilities
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into wargear_list")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Wargear_list.csv")
  
  print("\nDATASHEETS")
  try:
    with open("wahapedia/Datasheets.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["datasheet_id"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "link"):
          indexer["link"] = i
        elif(column == "faction_id"):
          indexer["faction_id"] = i
        elif(column == "source_id"):
          indexer["source_id"] = i
        elif(column == "role"):
          indexer["role"] = i
        elif(column == "unit_composition"):
          indexer["unit_composition"] = i
        elif(column == "transport"):
          indexer["transport"] = i
        elif(column == "power_points"):
          indexer["power_points"] = i
        elif(column == "priest"):
          indexer["priest"] = i
        elif(column == "psyker"):
          indexer["psyker"] = i
        elif(column == "open_play_only"):
          indexer["open_play_only"] = i
        elif(column == "crusade_only"):
          indexer["crusade_only"] = i
        elif(column == "virtual"):
          indexer["virtual_"] = i
        elif(column == "Cost"):
          indexer["cost"] = i
        elif(column == "cost_per_unit"):
          indexer["cost_per_unit"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets (datasheet_id, name, link, faction_id, source_id, role, unit_composition, transport, power_points, priest, psyker, open_play_only, crusade_only, virtual_, cost, cost_per_unit) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["datasheet_id"]] if row[indexer["datasheet_id"]] != '' else None,  # datasheet_id
          row[indexer["name"]] if row[indexer["name"]] != '' else None,  # name
          row[indexer["link"]] if row[indexer["link"]] != '' else None,  # link
          row[indexer["faction_id"]] if row[indexer["faction_id"]] != '' else None,  # faction_id
          row[indexer["source_id"]] if row[indexer["source_id"]] != '' else None,  # source_id
          row[indexer["role"]] if row[indexer["role"]] != '' else None,  # role
          row[indexer["unit_composition"]] if row[indexer["unit_composition"]] != '' else None,  # unit_composition
          row[indexer["transport"]] if row[indexer["transport"]] != '' else None,  # transport
          row[indexer["power_points"]] if row[indexer["power_points"]] != '' else None,  # power_points
          row[indexer["priest"]] if row[indexer["priest"]] != '' else None,  # priest
          row[indexer["psyker"]] if row[indexer["psyker"]] != '' else None, # psyker
          1 if row[indexer["open_play_only"]] == "true" else 0 if row[indexer["open_play_only"]] == "false" else -1, # open_play_only, boolean
          1 if row[indexer["crusade_only"]] == "true" else 0 if row[indexer["crusade_only"]] == "false" else -1, # crusade_only, boolean
          1 if row[indexer["virtual_"]] == "true" else 0 if row[indexer["virtual_"]] == "false" else -1, # virtual_, boolean
          row[indexer["cost"]] if row[indexer["cost"]] != '' else None, # cost
          1 if row[indexer["cost_per_unit"]] == "true" else 0 if row[indexer["cost_per_unit"]] == "false" else -1, # cost_per_unit, boolean
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets.csv")
  
  print("\nABILITIES")
  try:
    with open("wahapedia/Abilities.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["ability_id"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "legend"):
          indexer["legend"] = i
        elif(column == "is_other_wargear"):
          indexer["is_other_wargear"] = i
        elif(column == "faction_id"):
          indexer["faction_id"] = i
        elif(column == "description"):
          indexer["description"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO abilities (ability_id, type, name, legend, is_other_wargear, faction_id, description) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["ability_id"]], # ability_id
          row[indexer["type"]], # type
          row[indexer["name"]], # name
          row[indexer["legend"]], # legend
          1 if row[indexer["is_other_wargear"]] == "true" else 0 if row[indexer["is_other_wargear"]] == "false" else -1, # is_other_wargear, boolean
          row[indexer["faction_id"]], # faction_id,
          row[indexer["description"]], # description
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into abilities")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Abilities.csv")
  
  print("\nDATASHEETS ABILITIES")
  try:
    with open("wahapedia/Datasheets_abilities.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "datasheet_id"):
          indexer["datasheet_id"] = i
        elif(column == "line"):
          indexer["line"] = i
        elif(column == "ability_id"):
          indexer["ability_id"] = i
        elif(column == "is_index_wargear"):
          indexer["is_index_wargear"] = i
        elif(column == "cost"):
          indexer["cost"] = i
        elif(column == "model"):
          indexer["model"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets_abilities (datasheet_id, line, ability_id, is_index_wargear, cost, model) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["datasheet_id"]], # datasheet_id
          row[indexer["line"]], # line
          row[indexer["ability_id"]], # ability_id
          1 if row[indexer["is_index_wargear"]] == "true" else 0 if row[indexer["is_index_wargear"]] == "false" else -1, # is_index_wargear, boolean
          row[indexer["cost"]], # cost
          row[indexer["model"]], # model
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets_abilities")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets_abilities.csv")
  
  print("\nPSYCHIC POWERS")
  try:
    with open("wahapedia/PsychicPowers.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["psychic_power_id"] = i
        elif(column == "roll"):
          indexer["roll"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "faction_id"):
          indexer["faction_id"] = i
        elif(column == "legend"):
          indexer["legend"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "description"):
          indexer["description"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO psychic_powers (psychic_power_id, roll, name, faction_id, legend, type, description) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s),"
        # input data is out of order (doesn't start with id) and contains duplicate information
        data = data + [
          row[indexer["psychic_power_id"]], # psychic_power_id
          row[indexer["roll"]], # roll
          row[indexer["name"]], # name
          row[indexer["faction_id"]], # faction_id
          row[indexer["legend"]], # legend
          row[indexer["type"]], # type
          row[indexer["description"]], # description
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into psychic_powers")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/PsychicPowers.csv")
  
  print("\nWARLORD TRAITS")
  try:
    with open("wahapedia/Warlord_traits.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "faction_id"):
          indexer["faction_id"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "roll"):
          indexer["roll"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "legend"):
          indexer["legend"] = i
        elif(column == "description"):
          indexer["description"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO warlord_traits (trait_id, faction_id, type, roll, name, legend, description) VALUES "
      data = []
      for row in csvF:
        # data doesn't have ID for rows
        query+="(DEFAULT,%s,%s,%s,%s,%s,%s),"
        # data has duplicate information
        data = data + [
          row[indexer["faction_id"]], # faction_id
          row[indexer["type"]], # type
          row[indexer["roll"]], # roll
          row[indexer["name"]], # name
          row[indexer["legend"]], # legend
          row[indexer["description"]], # description
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into warlord_traits")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Warlord_traits.csv")
  
  print("\nSTRATAGEMS")
  try:
    with open("wahapedia/Stratagems.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "id"):
          indexer["strategem_id"] = i
        elif(column == "faction_id"):
          indexer["faction_id"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "type"):
          indexer["type"] = i
        elif(column == "cp_cost"):
          indexer["cp_cost"] = i
        elif(column == "legend"):
          indexer["legend"] = i
        elif(column == "source_id"):
          indexer["source_id"] = i
        elif(column == "description"):
          indexer["description"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO strategems (strategem_id, faction_id, name, type, cp_cost, legend, source_id, description) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s,%s),"
        # input data is out of order (doesn't start with id)
        data = data + [
          row[indexer["strategem_id"]], # strategem_id
          row[indexer["faction_id"]], # faction_id
          row[indexer["name"]], # name
          row[indexer["type"]], # type
          row[indexer["cp_cost"]], # cp_cost
          row[indexer["legend"]], # legend
          row[indexer["source_id"]], # source_id
          row[indexer["description"]], # description
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into strategems")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Stratagems.csv")
  
  print("\nDATASHEETS DAMAGE")
  try:
    with open("wahapedia/Datasheets_damage.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "datasheet_id"):
          indexer["datasheet_id"] = i
        elif(column == "line"):
          indexer["line"] = i
        elif(column == "Col1"):
          indexer["col1"] = i
        elif(column == "Col2"):
          indexer["col2"] = i
        elif(column == "Col3"):
          indexer["col3"] = i
        elif(column == "Col4"):
          indexer["col4"] = i
        elif(column == "Col5"):
          indexer["col5"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets_damage (datasheet_id, line, col1, col2, col3, col4, col5) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s),"
        # every col column is highly variable
        data = data + [
          row[indexer["datasheet_id"]], # datasheet_id
          row[indexer["line"]], # line
          row[indexer["col1"]].replace('+', ''), # col1
          row[indexer["col2"]].replace('+', ''), # col2
          row[indexer["col3"]].replace('+', ''), # col3
          row[indexer["col4"]].replace('+', ''), # col4
          row[indexer["col5"]].replace('+', ''), # col5
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets_damage")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets_damage.csv")
  
  print("\nDATASHEETS KEYWORDS")
  try:
    with open("wahapedia/Datasheets_keywords.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "datasheet_id"):
          indexer["datasheet_id"] = i
        elif(column == "keyword"):
          indexer["keyword"] = i
        elif(column == "model"):
          indexer["model"] = i
        elif(column == "is_faction_keyword"):
          indexer["is_faction_keyword"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets_keywords (datasheet_id, keyword, model, is_faction_keyword) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s),"
        data = data + [
          row[indexer["datasheet_id"]], # datasheet_id
          row[indexer["keyword"]], # keyword
          row[indexer["model"]] if row[indexer["model"]] != '' else None, # model
          1 if row[indexer["is_faction_keyword"]] == "true" else 0 if row[indexer["is_faction_keyword"]] == "false" else -1, # is_faction_keyword, boolean
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets_keywords")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets_keywords.csv")
  
  print("\nDATASHEETS MODELS")
  try:
    with open("wahapedia/Datasheets_models.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "datasheet_id"):
          indexer["datasheet_id"] = i
        elif(column == "line"):
          indexer["line"] = i
        elif(column == "name"):
          indexer["name"] = i
        elif(column == "M"):
          indexer["movement"] = i
        elif(column == "WS"):
          indexer["weapon_skill"] = i
        elif(column == "BS"):
          indexer["ballistic_skill"] = i
        elif(column == "S"):
          indexer["strength"] = i
        elif(column == "T"):
          indexer["toughness"] = i
        elif(column == "W"):
          indexer["wounds"] = i
        elif(column == "A"):
          indexer["attacks"] = i
        elif(column == "Ld"):
          indexer["leadership"] = i
        elif(column == "Sv"):
          indexer["save"] = i
        elif(column == "Cost"):
          indexer["cost"] = i
        elif(column == "cost_description"):
          indexer["cost_description"] = i
        elif(column == "models_per_unit"):
          indexer["models_per_unit"] = i
        elif(column == "cost_including_wargear"):
          indexer["cost_including_wargear"] = i
        elif(column == "base_size"):
          indexer["base_size"] = i
        elif(column == "base_size_descr"):
          indexer["base_size_descr"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets_models (datasheet_id, line, name, movement, weapon_skill, ballistic_skill, strength, toughness, wounds, attacks, leadership, save, cost, cost_description, models_per_unit, cost_including_wargear, base_size, base_size_descr) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["datasheet_id"]], # datasheet_id
          row[indexer["line"]], # line
          row[indexer["name"]], # name
          row[indexer["movement"]].replace('"', ''), # movement
          row[indexer["weapon_skill"]][0] if row[indexer["weapon_skill"]][0] != '-' else None, # weapon_skill, deformatted
          row[indexer["ballistic_skill"]][0] if row[indexer["ballistic_skill"]][0] != '-' else None, # ballistic_skill, deformatted
          row[indexer["strength"]] if row[indexer["strength"]][0] != '-' else None, # strength, formatted
          row[indexer["toughness"]] if row[indexer["toughness"]][0] != '-' else None, # toughness, formatted
          row[indexer["wounds"]] if row[indexer["wounds"]][0] != '-' else None, # wounds, formatted
          row[indexer["attacks"]] if row[indexer["attacks"]][0] != '-' else None, # attacks, formatted
          row[indexer["leadership"]] if row[indexer["leadership"]][0] != '-' else None, # leadership, formatted
          row[indexer["save"]][0] if row[indexer["save"]][0] != '-' else None, # save, deformatted
          row[indexer["cost"]], # cost
          row[indexer["cost_description"]], # cost_description
          row[indexer["models_per_unit"]], # models_per_unit
          1 if row[indexer["cost_including_wargear"]] == "true" else 0 if row[indexer["cost_including_wargear"]] == "false" else -1, # cost_including_wargear, boolean
          row[indexer["base_size"]], # base_size
          row[indexer["base_size_descr"]], # base_size_descr
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets_models")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets_models.csv")
  
  print("\nDATASHEETS OPTIONS")
  try:
    with open("wahapedia/Datasheets_options.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "datasheet_id"):
          indexer["datasheet_id"] = i
        elif(column == "line"):
          indexer["line"] = i
        elif(column == "button"):
          indexer["button"] = i
        elif(column == "description"):
          indexer["description"] = i
        elif(column == "is_index_wargear"):
          indexer["is_index_wargear"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets_options (datasheet_id, line, button, description, is_index_wargear) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s),"
        data = data + [
          row[indexer["datasheet_id"]], # datasheet_id
          row[indexer["line"]], # line
          row[indexer["button"]], # button
          row[indexer["description"]], # description
          1 if row[indexer["is_index_wargear"]] == "true" else 0 if row[indexer["is_index_wargear"]] == "false" else -1, # is_index_wargear, boolean
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets_options")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets_options.csv")
  
  print("\nDATASHEETS WARGEAR")
  try:
    with open("wahapedia/Datasheets_wargear.csv",mode='r') as f:
      csvF = csv.reader(f, delimiter='|')
      
      indexer = {}
      i = 0
      columns = next(csvF)
      for column in columns:
        column = column.replace(u'\ufeff', '')
        if(column == "datasheet_id"):
          indexer["datasheet_id"] = i
        elif(column == "line"):
          indexer["line"] = i
        elif(column == "wargear_id"):
          indexer["wargear_id"] = i
        elif(column == "cost"):
          indexer["cost"] = i
        elif(column == "is_index_wargear"):
          indexer["is_index_wargear"] = i
        elif(column == "model"):
          indexer["model"] = i
        elif(column == "is_upgrade"):
          indexer["is_upgrade"] = i
        i = i + 1
      
      query = "INSERT IGNORE INTO datasheets_wargear (datasheet_id, line, wargear_id, cost, is_index_wargear, model, is_upgrade) VALUES "
      data = []
      for row in csvF:
        query+="(%s,%s,%s,%s,%s,%s,%s),"
        # MySQL doesn't support booleans, so we're re-using an INT (-1 is data isn't boolean)
        data = data + [
          row[indexer["datasheet_id"]], # datasheet_id
          row[indexer["line"]], # line
          row[indexer["wargear_id"]], # wargear_id
          row[indexer["cost"]], # cost
          1 if row[indexer["is_index_wargear"]] == "true" else 0 if row[indexer["is_index_wargear"]] == "false" else -1, # is_index_wargear, boolean
          row[indexer["model"]], # model
          1 if row[indexer["is_upgrade"]] == "true" else 0 if row[indexer["is_upgrade"]] == "false" else -1, # is_upgrade, boolean
        ]
      query = query[:-1] + " ON DUPLICATE KEY UPDATE check_me=1"
      cur.execute(query,data)
      print(cur.rowcount, "rows inserted into datasheets_wargear")
      db.commit()
  except mysql.connector.Error as err:
    print(err)
  except IOError:
    print("unable to open wahapedia/Datasheets_wargear.csv")
  
  print("\nDATA ERRORS")
  try:
    query = "SELECT COUNT(*) AS count FROM sources WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in sources".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM factions WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in factions".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM wargear WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in wargear".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM wargear_list WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in wargear_list".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM abilities WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in abilities".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets_abilities WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets_abilities".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM psychic_powers WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in psychic_powers".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM warlord_traits WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in warlord_traits".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM strategems WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in strategems".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets_damage WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets_damage".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets_keywords WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets_keywords".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets_models WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets_models".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets_options WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets_options".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  try:
    query = "SELECT COUNT(*) AS count FROM datasheets_wargear WHERE check_me = 1"
    cur.execute(query)
    errors = cur.fetchone().count
    if(errors):
      print("{count} Error(s) in datasheets_wargear".format(count=errors))
  except mysql.connector.Error as err:
    print(err)
  
  print("\nscript ending")
  cur.close()
  db.close()
