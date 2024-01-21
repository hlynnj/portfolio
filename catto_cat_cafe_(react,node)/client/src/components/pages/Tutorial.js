import React, { useState, useEffect } from "react";
import BackButton from "../modules/BackButton.js";
import { Redirect } from "@reach/router";
import LinkButton from "../modules/LinkButton.js";

import "./Tutorial.css";

const Tutorial = () => {
  return (
    <div>
      <div className="tutorialHeader">Tutorial</div>
      <img className="tutorialImg"
           src="https://i.ibb.co/4snWvw8/Screenshot-5339.png" />
      <div className="tutorialBtn">
        <LinkButton link="/new-cafe" text="Create Cafe!"/>
      </div>
    </div>
  );
};

export default Tutorial;