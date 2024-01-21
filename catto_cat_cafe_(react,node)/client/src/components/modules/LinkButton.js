import React from "react";
import { Link } from "@reach/router";

import "./LinkButton.css";

//TODO: move this into CSS? i think it can stay here tho

const LinkButton = ({ link, text }) => {
  return (
    <div className="link">
      <Link to={link} className="link-text">
        {text}
      </Link>
    </div>
  );
};

export default LinkButton;
