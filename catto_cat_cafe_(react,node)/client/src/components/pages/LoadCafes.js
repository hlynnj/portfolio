import React, { useState, useEffect } from "react";

import BackButton from "../modules/BackButton.js";
import CafeCard from "../modules/CafeCard.js";
import Cafe from "./Cafe.js";

import LinkButton from "../modules/LinkButton.js";

import { get } from "../../utilities";

import "./LoadCafes.css";

const LoadCafes = (props) => {
  const [cafes, setCafes] = useState([]);
  const [selected, setSelected] = useState(null);

  // TODO: set up database connection for cafe
  // TODO: (more like a question) - api get request upon button click on cafe card? different URL for different cafe-id?
  // TODO: discuss cafes state var logistics (updates when active cats updates?)

  //get user's previous cafe data, probably not full info bc we don't want to load all info from every cafe
  //but more like the summary info of each cafe, like time played, name?, cafe id (like 1 2 3, might just be stored)
  //this summary info could be an element under each cafe, or an array under user? probably former
  //generate each cafe as a clickable element that will then load all the info for that particular cafe (for this particular user)
  //and 'open up' the given cafe

  useEffect(() => {
    setSelected(null);
  }, []);

  useEffect(() => {
    get("/api/allcafes", { creator_id: props.userId }).then((cafeObjs) => {
      setCafes(cafeObjs);
    });
  }, []);

  const clickHandler = (cafeObj) => {
    setSelected(cafeObj);
    setCafes(null);
  };

  if (selected) {
    return <Cafe cafeId={selected._id} activeCats={selected.active_cats} money={selected.money} />;
  }
  let cafeList = null;
  const hasCafes = cafes.length !== 0;
  if (hasCafes) {
    cafeList = cafes.map((cafeObj) => (
      <CafeCard
        key={`Card_${cafeObj._id}`}
        name={cafeObj.cafeName}
        save_time={cafeObj.save_time}
        money={cafeObj.money}
        img="https://i.ibb.co/zHxQmyZ/home-load.png"
        onClick={(event) => clickHandler(cafeObj)}
      />
    ));
  } else {
    cafeList = (
      <div>
        <div>No cafes!</div>
        <div>Expected cafes? Click here:</div>
        <LinkButton link="/" text="return to home" />
      </div>
    );
  }

  return (
    <div>
      <div className="background">
        <div className="load-header">
          <div className="load-backbutton">
            <BackButton link="/home" text="<Back" />
          </div>
          <div className="load-header-name">Load Cafes </div>
        </div>
        <div className="load-list-border1">
          <div className="load-list-container">{cafeList}</div>
        </div>
      </div>
    </div>
  );
};

export default LoadCafes;
