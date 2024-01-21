const mongoose = require("mongoose");

const CafeSchema = new mongoose.Schema ({
    creator_id: String, 
    cafeName: {type: String, default: "New Cafe"},
    money: {type: Number, default: 0},
    save_time: {type: String, default: "0000-00-00 00:00:00"},
    active_cats: {type: Object, default: {}},
});

module.exports = mongoose.model("cafe", CafeSchema);
