// imports for frontend
import React, { useState, useEffect } from "react";
import MoneyBar from "../modules/MoneyBar";
import HappinessBar from "../modules/HappinessBar.js";
import LinkButton from "../modules/LinkButton.js";
import "../../utilities.css";
import "./Cafe.css";
import { Redirect } from "@reach/router";

// imports for backend
import { socket } from "../../client-socket";
import { drawCanvas, getAspectRatio } from "../../canvasManager";
import { post } from "../../utilities";

const Cafe = (props) => {

  /** STATE VARIABLES */  

  // total money in cafe
  const [totalMoney, setTotalMoney] = useState(props.money);

  // total active cats
  // can (should) include all possible active cats
  const [activeCats, setActiveCats] = useState(props.activeCats);

  const getDateTime = () => {
    var today = new Date();
    var date = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate();
    var time = today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    return date+' '+time;
  };

  /** SOCKET CALLS FROM SERVER */

  // updating location of active cats
  useEffect(() => {
    socket.on("addActiveCat", (update) => {
      setActiveCats(prevState => {
        Object.values(update.cats).forEach((cat) => {
          prevState[cat.catName].zoneNum = cat.zoneNum;
        });
        return prevState;
      });
    });
  }, []);

  // drawing canvas
  useEffect(() => {
    socket.on("update", (update) => {
      processUpdate(update);
    });
  }, []);

  const processUpdate = (update) => {
    drawCanvas(update);
  };

  // decrement cat Happiness
  useEffect(() => {
    socket.on("decrementHappiness", () => {
      setActiveCats(prevState => {
        Object.values(prevState).forEach((cat) => {
          if (cat.catHappiness > 0) cat.catHappiness -= 0.5;
        });
        return prevState;
      });
    });
  }, []);

  // updating total money
  useEffect(() => {
    socket.on("addMoney", (update) => {
    let extraMoney = 0;
    Object.keys(activeCats).forEach((cat) => {
      extraMoney += (activeCats[cat].baseMoney + activeCats[cat].catHappiness * 0.1) * 0.1;
    });

    setTotalMoney(prevState => {
      prevState = prevState + extraMoney;
      return prevState;
    });
    });
  }, []);

  useEffect(() => {
    Object.keys(activeCats).forEach((cat) => {
      document.getElementById('bar'+cat).setAttribute("style","width:"+Math.ceil(activeCats[cat].catHappiness * 2)+"px");
    });
  });

  let canvas;
  let context;
  useEffect(() => {
    canvas = document.getElementById("game-canvas");
    context = canvas.getContext("2d");
  })

  /** process user click */
  const clickHandler = (event) => {

    // setting up canvas
    const canvas = document.getElementById("game-canvas");
    let rect = canvas.getBoundingClientRect();

    // determine current ratio of canvas (based on window size)
    var ratios = getAspectRatio();
    const ratio = ratios.factor;
    const topleft = ratios.topleft;

    // determine user's click location
    let x = event.clientX - rect.left;
    let y = event.clientY - rect.top;
    var mousePosition = {drawX: x, drawY: y};

    // convert user click location to corresponding zone
    let zoneClicked = "";

    if ((mousePosition.drawX > 90 * ratio && mousePosition.drawX < 150 * ratio) && (mousePosition.drawY > 20 * ratio && mousePosition.drawY < 80 * ratio)) {
      zoneClicked = "1";
    }
    else if ((mousePosition.drawX > 55 * ratio && mousePosition.drawX < 105 * ratio) && (mousePosition.drawY > 105 * ratio && mousePosition.drawY < 165 * ratio)) {
      zoneClicked = "2";
    }
    else if ((mousePosition.drawX > 185 * ratio && mousePosition.drawX < 245 * ratio) && (mousePosition.drawY > 145 * ratio && mousePosition.drawY < 205 * ratio)) {
      zoneClicked = "3";
    }
    else if ((mousePosition.drawX > 230 * ratio && mousePosition.drawX < 290 * ratio) && (mousePosition.drawY > 40 * ratio && mousePosition.drawY < 100 * ratio)) {
      zoneClicked = "4";
    }
    else if ((mousePosition.drawX > 320 * ratio && mousePosition.drawX < 380 * ratio) && (mousePosition.drawY > 110 * ratio && mousePosition.drawY < 170 * ratio)) {
      zoneClicked = "5";
    }
    else if ((mousePosition.drawX > 215 * ratio && mousePosition.drawX < 275 * ratio) && (mousePosition.drawY > 240 * ratio && mousePosition.drawY < 300 * ratio)) {
      zoneClicked = "6";
    }
    else if ((mousePosition.drawX > 105 * ratio && mousePosition.drawX < 165 * ratio) && (mousePosition.drawY > 305 * ratio && mousePosition.drawY < 365 * ratio)) {
      zoneClicked = "7";
    }
    else if ((mousePosition.drawX > 250 * ratio && mousePosition.drawX < 310 * ratio) && (mousePosition.drawY > 285 * ratio && mousePosition.drawY < 345 * ratio)) {
      zoneClicked = "8";
    }
    else if ((mousePosition.drawX > 450 * ratio && mousePosition.drawX < 510 * ratio) && (mousePosition.drawY > 235 * ratio && mousePosition.drawY < 295 * ratio)) {
      zoneClicked = "9";
    }
    else if ((mousePosition.drawX > 400 * ratio && mousePosition.drawX < 460 * ratio) && (mousePosition.drawY > 300 * ratio && mousePosition.drawY < 360 * ratio)) {
      zoneClicked = "10";
    }
    else if ((mousePosition.drawX > 545 * ratio && mousePosition.drawX < 605 * ratio) && (mousePosition.drawY > 305 * ratio && mousePosition.drawY < 365 * ratio)) {
      zoneClicked = "11";
    }
    else if ((mousePosition.drawX > 580 * ratio && mousePosition.drawX < 640 * ratio) && (mousePosition.drawY > 130 * ratio && mousePosition.drawY < 190 * ratio)) {
      zoneClicked = "12";
    }
    else if ((mousePosition.drawX > 65 * ratio && mousePosition.drawX < 125 * ratio) && (mousePosition.drawY > 245 * ratio && mousePosition.drawY < 305 * ratio)) {
      zoneClicked = "13";
    }

    // increment happiness of clicked cat by 1
    setActiveCats(prevState => {
      Object.keys(prevState).forEach((cat) => {
        if (prevState[cat].zoneNum == zoneClicked) {
          if (prevState[cat].catHappiness <= 99) prevState[cat].catHappiness += 1;
          else prevState[cat].catHappiness = 100;
        }
      });
      return prevState;
    });
  };

  const saveHandler = () => {
    const dateTime = getDateTime();
      const body = {
        _id: props.cafeId,
        active_cats: activeCats,
        money: totalMoney,
        save_time: dateTime,
      };

    post("/api/updateCafe", body);
  };

  if (totalMoney >= 27755) {
    saveHandler();
    return (
      <Redirect to="/credits"/>
    );
  }
      
  return (
    <>
    <div className="cafeScreen u-inlineBlock">
      <div className="money-bar">
        <MoneyBar money={totalMoney} />
      </div>
      <div className="saveButton">
        <button className="link link-text" onClick={saveHandler}>Save!</button>
      </div>
      <div className="homeButton">
        <LinkButton link="/home" text="To Home" />
      </div>

      <img id="imgArthur" src="https://i.ibb.co/dPkSJmr/arthur-head.png"
             width="40px" height="40px" />
        <div id="bar1">
          <HappinessBar />
          <div id="barArthur"></div>
        </div>

      <img id="imgBox" src="https://i.ibb.co/QC7sYgm/box-head.png"
            width="40px" height="40px" />
      <div id="bar2">
        <HappinessBar />
        <div id="barBox"></div>
      </div>

      <img id="imgBrioche" src="https://i.ibb.co/ZLYX62q/brioche-head.png"
            width="40px" height="40px" />
      <div id="bar3">
        <HappinessBar />
        <div id="barBrioche"></div>
      </div>

      <img id="imgCardigan" src="https://i.ibb.co/LnC7sxy/cardigan-head.png"
            width="40px" height="40px" />
      <div id="bar4">
        <HappinessBar />
        <div id="barCardigan"></div>
      </div>

      <img id="imgClover" src="https://i.ibb.co/3hVCyvM/clover-head.png"
            width="40px" height="40px" />
      <div id="bar5">
        <HappinessBar />
        <div id="barClover"></div>
      </div>

      <img id="imgDana" src="https://i.ibb.co/NnzcjPF/dana-head.png"
            width="40px" height="40px" />
      <div id="bar6">
        <HappinessBar />
        <div id="barDana"></div>
      </div>

      <img id="imgFinnegan" src="https://i.ibb.co/JQV6SmK/finnegan-head.png"
            width="40px" height="40px" />
      <div id="bar7">
        <HappinessBar />
        <div id="barFinnegan"></div>
      </div>

      <img id="imgLily" src="https://i.ibb.co/NKFqFWv/lily-head.png"
           width="40px" height="40px" />
      <div id="bar8">
        <HappinessBar />
        <div id="barLily"></div>
      </div>

      <img id="imgMargaret" src="https://i.ibb.co/m6WV15h/margaret-head.png"
            width="40px" height="40px" />
      <div id="bar9">
        <HappinessBar />
        <div id="barMargaret"></div>
      </div>

      <img id="imgPearl" src="https://i.ibb.co/5sgjcTV/pearl-head.png"
            width="40px" height="40px" />
      <div id="bar10">
        <HappinessBar />
        <div id="barPearl"></div>
      </div>

      <img id="imgPompom" src="https://i.ibb.co/PFD00Vp/pompom-head.png"
            width="40px" height="40px" />
      <div id="bar11">
        <HappinessBar />
        <div id="barPompom"></div>
      </div>

      <img id="imgRitz" src="https://i.ibb.co/7JtNh5g/ritz-head.png"
            width="40px" height="40px" />
      <div id="bar12">
        <HappinessBar />
        <div id="barRitz"></div>
      </div>

      <div className="Game-body">
        <canvas id="game-canvas" onClick={(event) => {clickHandler(event);}}/>
      </div>
    </div>
    </>
  );
};

export default Cafe;
