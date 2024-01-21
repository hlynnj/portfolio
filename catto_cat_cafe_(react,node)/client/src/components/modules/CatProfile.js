import React from "react";

import "./CatProfile.css";

/**
 * Profile of cat to be displayed on catalog right side
 *
 * Proptypes
 * @param {string} img link to cat img, either in-cafe sprite or unique portraits
 * @param {string} name of the cat
 * @param {number} description dictionary of four strings: type, likes, dislikes, and personality
 * @param {string} save_time time spent on cafe
 */

const CatProfile = (props) => {
  return (
    <div>
      <div className="catalog-profile-content-container">
        <div className="catalog-profile-top-content-container">
          <div className="catalog-profile-image">
            <img className="image catalog-profile-image" src={props.img} height="160" width="160" />
          </div>
          <div className="catalog-profile-text">
            <p className="catalog-profile-name">{props.name}</p>
            <div className="catalog-profile-top-text-element">Type: {props.description_type}</div>
            <div className="catalog-profile-top-text-element">Likes: {props.description_likes}</div>
            <div className="catalog-profile-top-text-element">
              Dislikes: {props.description_dislikes}
            </div>
          </div>
        </div>
        <div className="catalog-profile-bottom-content-container">
          <div className="catalog-profile-bottom-text-element personality">
            {props.description_personality}
          </div>
        </div>
      </div>
    </div>
  );
};

export default CatProfile;
