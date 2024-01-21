/** UTILS */

/**
 * 
 * @param {int, float} min minimum value
 * @param {int, float} max maximum value
 * @returns a random integer between min (inclusive) and max (exclusive)
 */
const getRandomInt = (min, max) => {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min); //The maximum is exclusive and the minimum is inclusive
};

/**
 * @returns a name of a cat
 */
 const randomNameGenerator = () => {
  var num = Math.random();
  if (num < 0.083) return "Ritz";
  else if (num < 0.166) return "Pompom";
  else if (num < 0.249) return "Pearl";
  else if (num < 0.332) return "Margaret";
  else if (num < 0.415) return "Finnegan";
  else if (num < 0.498) return "Dana";
  else if (num < 0.581) return "Clover";
  else if (num < 0.664) return "Cardigan";
  else if (num < 0.747) return "Brioche";
  else if (num < 0.830) return "Box";
  else if (num < 0.913) return "Arthur";
  else return "Lily";
};

/** GAMESTATE */

/**
 * cats: object containing currently active cats
 * money: total money of game
 * occupiedZones: boolean values, true if cat is in that numbered zone, false otherwise.
 */
const gameState = {
  cats: {},
  money: 0,
  occupiedZones: {
    "1": false,
    "2": false,
    "3": false,
    "4": false,
    "5": false,
    "6": false,
    "7": false,
    "8": false,
    "9": false,
    "10": false,
    "11": false,
    "12": false,
    "13": false,
  },
};

/** LOGIC */

/**
 * adds a random cat at a random zone
 * add rate is controlled by interval in server-socket.js
 */
const addCat = () => {

  // get random name
  const name = randomNameGenerator();
  
  // remove cat with name from current location, if there is one
  if (name in gameState.cats) {
    gameState.occupiedZones[gameState.cats[name].zoneNum] = false;
  }

  // get random zone number, which cannot be occupied by another cat
  let num = getRandomInt(1, 14);

  while (gameState.occupiedZones[num]) {
    num = getRandomInt(1, 14);
  }

  // add / update cat with name to gameState.cats
  gameState.cats[name] = {
    catName: name,
    catHappiness: 0,
    zoneNum: num,
  };

  // new zone is occupied by a cat
  gameState.occupiedZones[num] = true;
};

/**
 * increments gameState.money of current cafe based on:
 * 1) base money of the cats
 * 2) catHappiness of the cats
 */
const addMoney = () => {
  
  let extraMoney = 0;
  Object.values(gameState.cats).forEach((cat) => {
    extraMoney += cat.baseMoney + cat.catHappiness * 0.1;
  });

  gameState.money += extraMoney;
};

/** EXPORTS */

module.exports = {
  gameState,
  addCat,
  addMoney,
};
