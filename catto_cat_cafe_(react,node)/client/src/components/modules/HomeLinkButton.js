import React from "react";
import LinkButton from "./LinkButton.js";

import "./HomeLinkButton.css";

// props should have
// img: link to image src
// text: text to put on button
// link: link to redirect to
const HomeLinkButton = (props) => {
  return (
    <div className="u-flexColumn u-flex-alignCenter box">
      <div className="topMargin image-container">
        <img className="image" src={props.img} width="250" height="250" />
      </div>
      <div className="button">
        <LinkButton link={props.link} text={props.text} />
      </div>
      <p className="explanation ">{props.exp}</p>
    </div>
  );
};

export default HomeLinkButton;
