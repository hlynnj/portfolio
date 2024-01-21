import React, { useState, useEffect } from "react";

import "./MoneyBar.css";

const MoneyBar = (props) => {

  return (
    <div className="money-barContainer">
      <img src="https://media.discordapp.net/attachments/696173220453417030/932864945874411590/IMG_0214.png?width=779&height=779"
           height="45px" width="45px"/>
      <div className="moneyBarText">{Math.floor(props.money * 100) / 100}</div>
    </div>
  );
};

export default MoneyBar;
