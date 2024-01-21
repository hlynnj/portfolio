const mongoose = require("mongoose");

const CatSchema = new mongoose.Schema({
  name: String,
  head: String,
  full: String,
  description_type: String,
  description_likes: String,
  description_dislikes: String,
  description_personality: String,
});

// compile model from schema
module.exports = mongoose.model("cat", CatSchema);

const Cat = mongoose.model("cat", CatSchema);
