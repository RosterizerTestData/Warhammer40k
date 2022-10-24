var express = require('express');
var router = express.Router();
const pool = require('../config/data');
const SqlString = require('sqlstring');
const { processItems } = require('../public/javascripts/manifest.process');

/* GET home page. */
router.get('/', function(req, res, next) {
  console.log(req.body)
  // var sql = SqlString.format("SELECT * FROM datasheets;");
  var sql = SqlString.format("SELECT * FROM factions;");
  console.log(sql)
  pool.query(sql, function (error, results, fields) {
    if(error) {
      console.log(error);
      res.send(sql);
      return;
    }
    console.log(results)
    let factionList = results.filter(faction => faction.faction_id === faction.main_faction_id).sort((a,b) => a.name.localeCompare(b.name));
    console.log(factionList)
    
    //if we actually get a result
    
    res.render('index', { title: 'Wahapedia Exportion', data: factionList});
    // res.send(JSON.stringify(results.map(datasheet => `${datasheet.datasheet_id}: ${datasheet.name} – ${datasheet.unit_composition}`))); 
  });
});
router.get('/favicon.ico', function(req, res, next) {})

router.get('/:faction', async function (req, res, next) {
  console.log('req.body',req.body)
  let sql = '';
  let allResults = {};
  allResults.factions = await getFactions(req.params.faction);
  allResults.datasheets = await getDatasheets(req.params.faction);
  let datasheetList = Array.from(new Set(allResults.datasheets.map(datasheet => datasheet.datasheet_id)));
  console.log(datasheetList)
  allResults.keywords = await getKeywords(datasheetList);
  allResults.models = await getModels(datasheetList);
  allResults.damage = await getDamage(datasheetList);
  allResults.wargear = await getWargear(datasheetList);
  allResults.abilities = await getAbilities(datasheetList);
  allResults.options = await getOptions(datasheetList);
  allResults.psychicPowers = await getPsychicPowers(req.params.faction);
  allResults.stratagems = await getStrategems(req.params.faction);
  allResults.warlordTraits = await getWarlordTraits(req.params.faction);
  allResults.sources = await getSources();
  // console.log('allresults',allResults)
  allResults['!'] = processInfo(allResults,req.params.faction);
  allResults['!'].manifest.assetTaxonomy = processClasses(allResults);
  allResults['!'].manifest.assetCatalog = processItems(allResults);
  res.send(JSON.stringify(allResults['!']));
});


let getFactions = async (fac) => {
  const sql = SqlString.format("SELECT * FROM factions WHERE main_faction_id = ?",[fac]);
  console.log('query',fac,sql)
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  // console.log('factions',results)
  return results;
}

let getDatasheets = async (fac) => {
  const sql = SqlString.format("SELECT * FROM datasheets WHERE faction_id = ?",[fac]);
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  // console.log('datasheets',results)
  return results;
}

let getKeywords = async (datasheets) => {
  const sql = SqlString.format("SELECT * FROM datasheets_keywords WHERE datasheet_id in (?)",[datasheets]);
  console.log('query',sql)
  let results = datasheets.length ? await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  })) : {};
  // console.log('keywords',results)
  return results;
}

let getModels = async (datasheets) => {
  const sql = SqlString.format("SELECT * FROM datasheets_models WHERE datasheet_id in (?)",[datasheets]);
  console.log('query',sql)
  let results = datasheets.length ? await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  })) : {};
  // console.log('models',results)
  return results;
}

let getDamage = async (datasheets) => {
  const sql = SqlString.format("SELECT * FROM datasheets_damage WHERE datasheet_id in (?)",[datasheets]);
  console.log('query',sql)
  let results = datasheets.length ? await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  })) : {};
  // console.log('models',results)
  return results;
}

let getWargear = async (datasheets) => {
  let sql = SqlString.format("SELECT * FROM datasheets_wargear WHERE datasheet_id in (?)",[datasheets]);
  let datasheets_wargear = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  let wargearIDs = Array.from(new Set(datasheets_wargear?.map(wargear => wargear?.wargear_id)));
  sql = SqlString.format("SELECT * FROM wargear_list WHERE wargear_id in (?)",[wargearIDs]);
  let wargear_list = wargearIDs.length ? await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  })) : {};
  sql = SqlString.format("SELECT * FROM wargear WHERE wargear_id in (?)",[wargearIDs]);
  let wargear = wargearIDs.length ? await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  })) : {};
  // console.log('models',results)
  return {
    datasheets_wargear:datasheets_wargear,
    wargear_list:wargear_list,
    wargear:wargear,
  };
}

let getAbilities = async (datasheets) => {
  let sql = SqlString.format("SELECT * FROM datasheets_abilities WHERE datasheet_id in (?)",[datasheets]);
  let datasheets_abilities = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  let abilityIDs = Array.from(new Set(datasheets_abilities.map(ability => ability.ability_id)));
  sql = SqlString.format("SELECT * FROM abilities WHERE ability_id in (?)",[abilityIDs]);
  let abilities = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  // console.log('models',results)
  return {
    datasheets_abilities:datasheets_abilities,
    abilities:abilities,
  };
}
let getOptions = async (datasheets) => {
  const sql = SqlString.format("SELECT * FROM datasheets_options WHERE datasheet_id in (?)",[datasheets]);
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  return results;
}
let getPsychicPowers = async (fac) => {
  const sql = SqlString.format("SELECT * FROM psychic_powers WHERE faction_id = ?",[fac]);
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  return results;
}
let getStrategems = async (fac) => {
  const sql = SqlString.format("SELECT * FROM strategems WHERE faction_id = ?",[fac]);
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  return results;
}
let getWarlordTraits = async (fac) => {
  const sql = SqlString.format("SELECT * FROM warlord_traits WHERE faction_id = ?",[fac]);
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  return results;
}
let getSources = async () => {
  const sql = SqlString.format("SELECT * FROM sources");
  let results = await new Promise((resolve, reject) => pool.query(sql, (error, results) => {
    if(error) {
      console.log(error);
      reject(error);
      return;
    }else{
      resolve(results);
    }
  }));
  return results;
}

module.exports = router;
