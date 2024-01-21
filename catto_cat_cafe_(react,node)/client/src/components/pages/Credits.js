import React, { useState, useEffect } from "react";
import BackButton from "../modules/BackButton.js";
import LinkButton from "../modules/LinkButton.js";

import { Link } from "@reach/router";

import "./Credits.css";

const Credits = () => {
  return (
    <div className="credits-page-container">
      <div className="credits-header">Congratulations!</div>
      <div className="credits-sub-header">(don't worry, your progress has been saved)</div>
      <div className="credits-title-card">
        <img src="https://i.ibb.co/gVz97yQ/title-card-unspace.png" height="200" />
      </div>
      <div className="credits-content-container">
        <div className="credits-content-text">
          You've made 27,555 cephalocoins! If those were dollars, you would have enough money to pay
          for one semester of MIT tuition.
          <br />
          <br />
          Thank you so much for playing Catto! We hope you enjoyed and were able to imagine a cat
          cafe of your very own. Feel free to go back and continue making more money, create a new
          cafe, read more about your cats in the catalog, or even visit a real (ethical) cat cafe
          near you. It's never too late to enjoy things or try something new, and we hope our little
          site has given you the opportunity to do at least one of the two. Have a purrfect rest of
          your day!
          <br />
          <br />
          Site developed by Lynn Jung and Angelina Wu, including all the illustrations. Special
          thanks to the MIT web.lab staff and Joy Hu, Lahari Thati, and Susan Zhang. If you have any
          questions, concerns, or comments, please direct them towards lynnjung@mit.edu or
          atripleu@mit.edu.
        </div>
      </div>
      <div className="credits-home">
        <Link to="/home" className="credits-link-text">
          Take me Home
        </Link>
      </div>
    </div>
  );
};

export default Credits;
