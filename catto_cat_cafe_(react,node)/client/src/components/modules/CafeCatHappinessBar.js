import React from "react";
import HappinessBar from "./HappinessBar.js";

import "./CafeCatHappinessBar.css";

/**
 * Displays the happiness of (one) active cat
    Proptypes
    @param {string} image url of cat headshot
    @param {string} name of cat
    @param {string} happiness
 * */

const CafeCatHappinessBar = (props) => {
  return (
    <div className="cat-happiness-barContainer">
      <div className="cat-happiness-bar-pictureContainer">
        <img className="cat-happiness-bar-picture" src={props.image} />
      </div>
      <span className="cat-happiness-bar-name">{props.name}'s Happiness: </span>
      <HappinessBar happiness={props.happiness} />
    </div>
  );
};

export default CafeCatHappinessBar;
