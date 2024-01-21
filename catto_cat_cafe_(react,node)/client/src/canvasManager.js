let canvas;

/** ZONES */
export const zones = {
  "1": {x: 90, y: 20},
  "2": {x: 55, y: 105},
  "3": {x: 185, y: 145},
  "4": {x: 230, y: 40},
  "5": {x: 320, y: 110},
  "6": {x: 215, y: 240},
  "7": {x: 105, y: 305},
  "8": {x: 250, y: 285},
  "9": {x: 450, y: 235},
  "10": {x: 400, y: 300},
  "11": {x: 545, y: 305},
  "12": {x: 580, y: 130},
  "13": {x: 65, y: 245},
};

/** CAT IMAGE SOURCES */
const sources = {
  "Ritz": {body: "https://i.ibb.co/3htwHcj/ritz-full.png"},
  "Pompom": {body: "https://i.ibb.co/g4bfhMT/pompom-full.png"},
  "Pearl": {body: "https://i.ibb.co/SXr5YXh/pearl-full.png"},
  "Margaret": {body: "https://i.ibb.co/2sZGTkV/margaret-full.png"},
  "Finnegan": {body: "https://i.ibb.co/Mn9F5VW/finnegan-full.png"},
  "Dana": {body: "https://i.ibb.co/g4zcxmS/dana-full.png"},
  "Clover": {body: "https://i.ibb.co/QfQD4nS/clover-full.png"},
  "Cardigan": {body: "https://i.ibb.co/FW9cQY6/cardigan-full.png"},
  "Brioche": {body: "https://i.ibb.co/3yVMLtG/brioche-full.png"},
  "Box": {body: "https://i.ibb.co/5rScVTJ/box-full.png"},
  "Arthur": {body: "https://i.ibb.co/02TSswh/arthur-full.png"},
  "Lily": {body: "https://i.ibb.co/hZjLQjs/lily-full.png"},
};

/** UTILS */

/**
 * Draws an icon at given location, given resizing factor based on window size
 * @param {*} context 
 * @param {int} x : x-coord of top left corner to render icon
 * @param {int} y : y-coord of top left corner to render icon
 * @param {str} source : url leading to image src
 * @param {float} factor : factor in return val from getAspectRatio()
 */
const drawIcon = (context, x, y, source, factor) => {
  var image = new Image();
  image.src = source;
  context.drawImage(image, x, y, image.width/factor, image.height/factor); // last two params adjust icon size
};

// background image
var image = new Image();
image.src = "https://i.ibb.co/wQfqTxv/cafe-bg-furniture.png";

/**
 * @returns object containing the following:
 * factor: scale canvas size according to window size
 * topleft: offset in top left corner to center canvas in given window size
 */
 export const getAspectRatio = () => {
  var ratio = Math.min(window.innerWidth / image.width, window.innerHeight / image.height);
  return {factor: ratio, topleft: (window.innerWidth - (image.width * ratio) ) / 2};
};

/** DRAWING FUNCTIONS */

/**
 * Draws corresponding cat icon in given zone with given name
 * @param {*} context 
 * @param {int} zoneNum : zone number of cat to be rendered
 * @param {str} name : name of cat to be rendered
 * @param {float} ratio : factor in return val from getAspectRatio()
 * @param {int} topleft : topleft in return val from getAspectRatio()
 */
const drawCat = (context, zoneNum, name, ratio) => {

  // converting coordinates according to aspect ratio
  let drawX = zones[zoneNum].x * ratio;
  let drawY = zones[zoneNum].y * ratio;

  // retrieving src for different cat icons
  let source = sources[name].body;
  let factor = 10;

  drawIcon(context, drawX, drawY, source, factor / ratio);
};

/** MAIN DRAW */

/**
 * Draws the cafe screen.
 * @param {object} drawState : gameState (as defined in logic.js)
 * @returns null if no canvas element exists. otherwise, does not return
 */
export const drawCanvas = (drawState) => {

  // get the canvas element
  canvas = document.getElementById("game-canvas");
  if (!canvas) return;
  const context = canvas.getContext("2d");

  // determine aspect ratio
  const ratios = getAspectRatio();
  const ratio = ratios.factor;
  const topleft = ratios.topleft;

  // canvas should take up entire width of window
  // canvas height should be the same as the image height
  context.canvas.width = window.innerWidth;
  context.canvas.height = image.height * ratio * 0.87;

  // render background image
  context.drawImage(image, 0, 0, image.width * ratio, image.height * ratio * 0.87);

  // draw all the cats
  Object.values(drawState.cats).forEach((cat) => {
    drawCat(context, cat.zoneNum, cat.catName, ratio, 0);
  });
};