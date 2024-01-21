import React from "react";
import LinkButton from "../modules/LinkButton.js";
import HomeLinkButton from "../modules/HomeLinkButton.js";
import { post } from "../../utilities";

import "./Home.css";

const exp = {
  load: "Browse previously saved cafes",
  new: "Create a new cafe",
  catalog: "Read about the cats you see",
};

const GOOGLE_CLIENT_ID = "419674631549-0oao1s8qtq7jm3knt38lj7c289nenio5.apps.googleusercontent.com";

const Home = () => {
  return (
    <div>
      <div className="home-header header-name-withoutback">Home</div>
      <div className="logout-button" >
      <LinkButton link="/logout" text="Logout" />
      </div>
      <div className="home-links-container">
        <HomeLinkButton
          img="https://i.ibb.co/zHxQmyZ/home-load.png"
          link="/load-cafes"
          text="    Load Cafes    "
          exp={exp.load}
        />
        <HomeLinkButton
          img="https://i.ibb.co/QNqNJYv/home-new.png"
          link="/tutorial"
          text="New Cafe"
          exp={exp.new}
        />
        <HomeLinkButton
          img="https://i.ibb.co/s2RW2QS/home-catalog.png"
          link="/catalog"
          text="Catalog"
          exp={exp.catalog}
        />
      </div>
    </div>
  );
};

export default Home;
