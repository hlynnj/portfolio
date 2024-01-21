import React from "react";
import LinkButton from "../modules/LinkButton.js";
import { Link } from "@reach/router";

import "./BackButton.css";

const BackButton = ({ link, text }) => {
  return (
    <Link to={link} className="back-link-text">
      {text}
    </Link>
  );
};

export default BackButton;
