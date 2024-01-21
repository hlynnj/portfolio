import React from "react";

import "./CafeCard.css";

// assume we get cafe data from the database containing the following:
// name: user-created name of cafe
// save_time: time of last save

/**
 * CafeCard is a component for displaying a saved cafe (in LoadCafes)
 * Contains summary of cafe. When clicked takes you to said cafe and gets cafe data.
 *
 * Proptypes
 * @param {string} img of the cafe
 * @param {string} name of the cafe
 * @param {number} money currently held in this cafe
 * @param {string} save_time time spent on cafe
 */

const CafeCard = (props) => {
  return (
    <div className="cafe-card-border1" onClick={props.onClick}>
      <div className="cafe-card-container">
        <div className="cafe-card-image">
          <img className="image cafe-card-image" src={props.img} height="160" width="160" />
        </div>
        <div className="cafe-card-text">
          <p className="cafe-card-text-name">{props.name}</p>
          <p className="cafe-card-text-element">Money: {props.money}</p>
          <div className="cafe-card-text-element">Time: {props.save_time}</div>
        </div>
      </div>
    </div>
  );
};

export default CafeCard;
