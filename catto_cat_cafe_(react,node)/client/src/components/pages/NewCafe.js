import React, { useState, useEffect } from "react";
import { Redirect } from "react-router";
import Cafe from "./Cafe.js";
import BackButton from "../modules/BackButton.js";
import { post } from "../../utilities";

import "../modules/LinkButton.css";

import "./NewCafe.css";

const NewCafe = (props) => {
  const [newCafe, setNewCafe] = useState(null);
  /* not sure about this one, chief. the url probably wont be staying as newcafe
    need to create a new cafe instance (to store cats, cafe id, cafe summary, etc.)--should this also only be 
    saved upon hitting save or should the instance just be created? I think this can just be created. 
    Perhaps hitting newcafe could redirect to a fixed tutorial page that you click through
    after which you enter a cafe name and then you are finally redirected towards a new cafe instance to interact with
    */

    const handleSubmit = (event) => {
      //TODO: in future, send post request to generate new cafe with given name (make sure submission isn't empty, or if it is just set default name New Cafe?)
      //and save to database, then pull all necessary cafe info and boot up an actual new cafe
      //for now just takes user to new cafe page without actually creating a new cafe or doing anything with the name
      
      const name = document.getElementById("nameInput").value;

      if (name === "" || name.length > 15) {
        alert("Please enter a name between 1-15 characters!");
        return;
      }

      var today = new Date();
      var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
      var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
      var dateTime = date+' '+time;

      const body = {
          save_time: dateTime,
          cafeName: name,
          creator_id: props.userId,
      };

      post("/api/newcafe", body).then((cafe) => {
        setNewCafe(cafe);});
    };

  return (
    <>
    {!newCafe ?
    (
    <div>
      <BackButton link="/home" text="<Back"/>
      <div className="newCafeBox u-flex u-flex-alignCenter u-flex-justifyCenter">
        <div className="newCafeHeader">Enter a name for your cafe!</div>
        <div className="newCafeText">Enter name in the box below and hit submit!</div>
          <div className="new-cafe-input">
            <input
              type="text"
              id="nameInput"
              placeholder="Enter a name for your cafe"
              className="newNameInput"
            />
            <button type="submit" className="link-text submit-button" onClick={(props) => {handleSubmit(props);}}>Submit</button>
          </div>
      </div>
    </div>
    ) : (
      <Cafe name={newCafe.cafeName} money={newCafe.money} activeCats={newCafe.active_cats} cafeId={newCafe._id}/>
    )}
  </>
  );
};

export default NewCafe;
