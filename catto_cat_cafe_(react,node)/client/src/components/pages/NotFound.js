import React from "react";
import LinkButton from "../modules/LinkButton.js";

import "./Skeleton.css";

const NotFound = () => {
  return (
    <div className="skeleton-content">
      <div className="skeleton-header">404 Not Found</div>
      <div className="skeleton-text">The page you requested couldn't be found.</div>
      <div className="skeleton-text">To return to home, click here.</div>
      <div className="skeleton-button">
      <LinkButton link="/home" text="Home" />
      </div>
    </div>
  );
};

export default NotFound;
