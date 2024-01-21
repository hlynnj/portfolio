/*
|--------------------------------------------------------------------------
| api.js -- server routes
|--------------------------------------------------------------------------
|
| This file defines the routes for your server.
|
*/

const express = require("express");

// import models so we can interact with the database
const User = require("./models/user");
const Cafe = require("./models/cafe");
const Cat = require("./models/cat");

// import authentication library
const auth = require("./auth");

// api endpoints: all these paths will be prefixed with "/api/"
const router = express.Router();

const logic = require("../server/logic.js");

//initialize socket
const socketManager = require("./server-socket");

router.post("/login", auth.login);
router.post("/logout", auth.logout);
router.get("/whoami", (req, res) => {
  if (!req.user) {
    // not logged in
    return res.send({});
  }

  res.send(req.user);
});

router.post("/initsocket", (req, res) => {
  // do nothing if user not logged in
  if (req.user)
    socketManager.addUser(req.user, socketManager.getSocketFromSocketID(req.body.socketid));
  res.send({});
});

// |------------------------------|
// | write your API methods below!|
// |------------------------------|
router.get("/allcafes", (req, res) => {
  Cafe.find({ creator_id: req.query.creator_id }).then((allcafes) => {
    res.send(allcafes);
  });
});

router.post("/newcafe", (req, res) => {
  const newCafe = new Cafe({
    creator_id: req.body.creator_id,
    cafeName: req.body.cafeName,
    money: 0,
    save_time: req.body.save_time,
    active_cats: {
      Ritz: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 5,
      },
      Pompom: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Pearl: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Margaret: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Finnegan: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Dana: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Clover: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Cardigan: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Brioche: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Box: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Arthur: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
      Lily: {
        catHappiness: 0,
        zoneNum: 0,
        baseMoney: 10,
      },
    },
  });

  newCafe.save().then((newCafe) => res.send(newCafe));
});

router.post("/updateCafe", (req, res) => {
  Cafe.findByIdAndUpdate(req.body._id, { money: req.body.money, active_cats: req.body.active_cats }, { useFindAndModify: false }).then(
    (updated) => {
      res.send(updated);
    }
  );
});

router.get("/catprofile", (req, res) => {
  Cat.find({ name: req.query.cat_name }).then((catinfo) => {
    res.send(catinfo);
  });
});

/**
router.get("/resetcatalog", (req, res) => {
  Cat.deleteMany({}).then(() => {
    console.log("reset catalog");
  });
  let Clover = new Cat({
    name: "Clover",
    head: "",
    full: "https://i.ibb.co/xDZWhbK/clover-full.png",
    description_type: "White",
    description_likes: "Gloves, shiny things",
    description_dislikes: "Fish, violence",
    description_personality:
      "Very fluffy and knows it well. Devious, arrogant, and intelligent in equal parts, Clover will take any and every opportunity to get attention. He has this dreadful penchant for stealing all manner of trinkets and knickknacks in order to inspire a chase or two, pulling out mind-boggling feline acrobatics no matter the environment. But with just one look at his sparkly eyes and a few pets of his remarkable fluff, it just seems so natural to let him slink away… at least he’s smart enough not to break anything?",
  });

  Clover.save();

  let Arthur = new Cat({
    name: "Arthur",
    head: "",
    full: "https://i.ibb.co/GphN5Ck/arthur-full.png",
    description_type: "Black and white",
    description_likes: "Sitting on books",
    description_dislikes: "Doctor's visits",
    description_personality:
      "Runs fast and has a strong kick. Arthur is an extremely intelligent cat, but you almost wouldn’t be able to tell for all the danger he seems to run headfirst into except for the fact that there’s no way a normal cat would get himself into such situations in the first place. Dashing away from not one, but five dogs at the same time, balancing precariously on the windowsills of restricted properties, trying to lick suspicious-looking powders… the list goes on. But hey, sometimes he also finds and brings back your lost items when you need them most, so he’s not so bad to have around.",
  });

  Arthur.save();

  let Dana = new Cat({
    name: "Dana",
    head: "",
    full: "https://i.ibb.co/HKm5VBV/dana-full.png",
    description_type: "Calico",
    description_likes: "Rubber bands, snacks",
    description_dislikes: "Canned food",
    description_personality:
      "Likes to play but also gets lazy quickly. A bit of a capricious kitty, Dana comes and goes as she pleases, collecting things she likes and listening intently for the next new exciting thing. She’s curious but skittish around new people, and once she warms up to you, she’ll demand pets but jump out of hugs. There are definitely some constants, though: she loves trying new things, and she loves people. At heart, it seems she’ll always be a kitten, inviting herself into others’ hearts with a refreshing innocence. Watching her frolic, it’s easy to slow down and remember to enjoy simple pleasures, no matter how the world may change.",
  });

  Dana.save();

  let Margaret = new Cat({
    name: "Margaret",
    head: "",
    full: "https://i.ibb.co/X7c5g8J/margaret-full.png",
    description_type: "Orange",
    description_likes: "Fruit, high places",
    description_dislikes: "Male cats",
    description_personality:
      "Holds herself very regally. Margaret can make the most human-looking expressions you’ll ever see on a cat; unfortunately, the only ones you’ll see most of the time are displeasure and reluctant acceptance. She doesn’t bite, but she’s also slow to warm to new people, accepting pets and treats rather dispassionately. Wrong her once and she’ll remember forever, but (although she doesn’t show it) she remembers kindness too. With enough time and devotion, she may just send you a look so happy that you can’t help but fall in love.",
  });

  Margaret.save();

  let Pearl = new Cat({
    name: "Pearl",
    head: "",
    full: "https://i.ibb.co/3mQgMG6/pearl-full.png",
    description_type: "White with gray tips",
    description_likes: "Watching fish swim",
    description_dislikes: "Seafood, butterflies",
    description_personality:
      "Meows a lot and very loudly. Pearl seems to think everything is her personal property, which would be more annoying if she were actually possessive. As it is, she just walks over and sits on whatever she wants with a happy meow. Social and energetic if a bit lacking in restraint, Pearl’s quick to pick fights and drop them too—well, the second is true as long as you don’t mess with her friends, whom she’ll defend with claws and teeth. Many a fight has broken out over perceived insults to honors of those she likes, often to the detriment of everyone involved, but she remains widely beloved for her spirit.",
  });

  Pearl.save();

  let Ritz = new Cat({
    name: "Ritz",
    head: "",
    full: "https://i.ibb.co/XkwZVFN/ritz-full.png",
    description_type: "Blue gray",
    description_likes: "Cutlery, TV dramas",
    description_dislikes: "Laser pointers, catnip",
    description_personality:
      "Easily ruffled by inane things. Master of the silent, judgmental stare, Ritz seems to have everything a cat could be jealous of. Sleek fur, speedy feet, respect from fellow cats, and the intelligence to keep well out of trouble as well as mooch plenty of treats out of servile humans—this is a cat well-tuned to the inner workings of cat society. But for all his popularity, Ritz can be surprisingly standoffish. You won’t be getting his affection with cheap toys or tricks, and he’s basically untamable, but you might be able to get his respect if you’re persistent enough with your offerings.",
  });

  Ritz.save();

  let Cardigan = new Cat({
    name: "Cardigan",
    head: "",
    full: "https://i.ibb.co/1RQkH8R/cardigan-full.png",
    description_type: "Black and brown",
    description_likes: "Bells, hide and seek",
    description_dislikes: "Washing machines",
    description_personality:
      "A gentle, kindhearted kitty, Cardigan always wears his heart on his sleeve. Just look at those wide, sleepy eyes and the sweater-like pattern of the colors on his fur to understand the appeal of living life free of any burdens. Cardigan enjoys tucking himself into any tiny space he can find, whether it's an empty box, the back of a cabinet, or the slender gaps between the backs of furniture and the wall. He can often be found in brand new locations, expanding the frontiers of feline exploration. Just wave a tasty treat around, and Cardigan will come squeezing out of his latest hiding spot.",
  });

  Cardigan.save();

  let Finnegan = new Cat({
    name: "Finnegan",
    head: "",
    full: "https://i.ibb.co/jR6PwpM/finnegan-full.png",
    description_type: "White and brown",
    description_likes: "Royal titles, pampering",
    description_dislikes: "Doorbells, coffee",
    description_personality:
      "Full title Finnegan Bavaria Lysander Pepperoni IV, Esquire. According to the centuries-old oral traditions passed down in her family, Finnegan descends from a long, long line of noble knights and peerless scholars. Chivalrous (in theory), presumptuous, and master of the smug I've-won-yet-again smirk, Finnegan expects and receives only the best. She fancies herself a distinguished lady as well as an expert yodeler, but only one of those is true. An avid fan of leaping across long distances, she is unfortunately prone to misjudging depth and colliding with her intended perches. She might complain a bit, but never for long. Her short-term memory is awful.",
  });

  Finnegan.save();

  let PomPom = new Cat({
    name: "PomPom",
    head: "",
    full: "https://i.ibb.co/555xw24/pompom-full.png",
    description_type: "Gray with white tips",
    description_likes: "Pro-wrestling",
    description_dislikes: "Lamps, shuttlecocks",
    description_personality:
      "PomPom smash! Energetic, observant, and always down to clown, PomPom believes that if life provides lemons, those lemons should be suplexed until they produce lemonade. She faces her problems head-on, and she finds that almost everything can be resolved with a keen eye and a firm smack. A vigilant sentinel, PomPom also maintains a special seat by the window to stare at the birds of the wider world. Hopefully she never learns how to get past glass...",
  });

  PomPom.save();

  let Box = new Cat({
    name: "Box",
    head: "",
    full: "https://i.ibb.co/GHLbcFd/box-full.png",
    description_type: "Brown",
    description_likes: "Cardboard, ambient lighting",
    description_dislikes: "Moths, dust",
    description_personality:
      "Seeks comfort above all. Box possesses a surprising fluidity and can fit into any space with ease. However, he more often uses this ability to find napping spots rather than to pursue a grand adventure. Oftentimes he has been presumed missing only to be found asleep in a closed shoebox, tucked away in a closet. His dark brown fur makes it that much harder to find him, too, but it’s always worth it for the wondrous sensory experience of running fingers through his dense fur. When he’s not napping, Box enjoys making art using nothing but cardboard and his own claws.",
  });

  Box.save();

  let Brioche = new Cat({
    name: "Brioche",
    head: "",
    full: "https://i.ibb.co/T4ZbqMJ/brioche-full.png",
    description_type: "Tuxedo",
    description_likes: "Sudoku, marshmallows",
    description_dislikes: "Nonlinear algebra, heat",
    description_personality:
      "Has aureate eyes that seem to follow you around the room, but it’s somehow comforting rather than creepy. Thoughtful and introspective, Brioche prefers to observe the action until she’s needed. As such, she can often be found perched on a comfortable cushion, tending to her incredibly fluffy fur. Brioche self-identifies as a pacifist, but don’t let that lower your guard. She is always ready to do what’s right, even if it means stepping outside her comfort zone and off her comfort cushion. Although named after a French bread, this cat has never set a paw in Europe.",
  });

  Brioche.save();

  let Lily = new Cat({
    name: "Lily",
    head: "",
    full: "https://i.ibb.co/Ln3fhPh/lily-full.png",
    description_type: "Light brown",
    description_likes: "Blankets, flowers",
    description_dislikes: "Nighttime, loud noises",
    description_personality:
      "An eternal daydreamer with a penchant for the softer things in life. Lily tends to live with her head in the clouds, and has knocked over countless water bowls due to her distracted nature. Her eyes seem to hold an impossible depth of knowledge, yet you’ve also seen her walk into the same wall twice in one minute. When not daydreaming, Lily can be found asleep in a warm patch of sunlight, or a blanket fluffy enough to rival her own fur. Lily is especially fond of pets, and can fall asleep anywhere with the right amount of head rubs.",
  });

  Lily.save();

  res.send("");
});
*/

// anything else falls to this "not found" case
router.all("*", (req, res) => {
  console.log(`API route not found: ${req.method} ${req.url}`);
  res.status(404).send({ msg: "API route not found" });
});

module.exports = router;
