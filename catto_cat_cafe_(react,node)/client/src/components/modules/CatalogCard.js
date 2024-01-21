import React from "react";
import ProfilePic from "./ProfilePic.js";

import "./CatalogCard.css";

// assume we are passing in the data for each cat from the database, which we assume has:
// link: link to picture
// name: name of cat
// text: description of cat
// TODO: get the cat data from database
/**
 * CatalogCard is a component that holds information about one cat to be displayed in the catalog
 *
 * Proptypes
 * @param {string} link to cat picture
 * @param {string} name of cat
 * @param {string} loadCatProfile function that takes cat name and sets profile upon click
 *
 */

const CatalogCard = (props) => {
  return (
    <div
      className="catalog-card-container"
      onClick={() => {
        props.loadCatProfile(props.name);
      }}
    >
      <img src={props.img} className="catalog-card-image" />
      <div>{props.name}</div>
    </div>
  );
};

export default CatalogCard;
