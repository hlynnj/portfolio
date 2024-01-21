const socket = require("socket.io-client/lib/socket");
const logic = require("./logic");

let io;

const userToSocketMap = {}; // maps user ID to socket object
const socketToUserMap = {}; // maps socket ID to user object

const getSocketFromUserID = (userid) => userToSocketMap[userid];
const getUserFromSocketID = (socketid) => socketToUserMap[socketid];
const getSocketFromSocketID = (socketid) => io.sockets.connected[socketid];

const addUser = (user, socket) => {
  const oldSocket = userToSocketMap[user._id];
  // call the game logic to add this player to the game state
  // logic.addCat(user._id); --> i don't think we need this line
  if (oldSocket && oldSocket.id !== socket.id) {
    // there was an old tab open for this user, force it to disconnect
    // FIXME: is this the behavior you want?
    oldSocket.disconnect();
    delete socketToUserMap[oldSocket.id];
  }

  userToSocketMap[user._id] = socket;
  socketToUserMap[socket.id] = user;
};

const removeUser = (user, socket) => {
  if (user) {
    delete userToSocketMap[user._id];
    // call the game logic to remove this player from the game state
    // logic.removePlayer(user._id); --> i don't think we need this line
  }
  delete socketToUserMap[socket.id];
};

/** socket emits to Cafe.js */

// draws the canvas 1 time / second
setInterval(() => {
  io.emit("update", logic.gameState);
}, 1000 / 10);

// updates one cat's location at random 1 time / 10 seconds
setInterval(() => {
  logic.addCat();
  io.emit("addActiveCat", logic.gameState);
}, 5000);

// decrements all cats' happiness by 0.01 / 2 seconds
setInterval(() => {
  io.emit("decrementHappiness");
}, 2000)

//updates money 1 time / 5 seconds
setInterval(() => {
  io.emit("addMoney", logic.gameState);
}, 1000);

module.exports = {
  init: (http) => {
    io = require("socket.io")(http);

    io.on("connection", (socket) => {
      console.log(`socket has connected ${socket.id}`);
      socket.on("disconnect", (reason) => {
        const user = getUserFromSocketID(socket.id);
        removeUser(user, socket);
      });
      socket.on("move", (dir) => {
        const user = getUserFromSocketID(socket.id);
        if (user) logic.movePlayer(user._id, dir);
      });
    });
  },

  addUser: addUser,
  removeUser: removeUser,

  getSocketFromUserID: getSocketFromUserID,
  getUserFromSocketID: getUserFromSocketID,
  getSocketFromSocketID: getSocketFromSocketID,
  getIo: () => io,
};
