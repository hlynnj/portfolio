import React, { useState, useEffect } from "react";
import { Router } from "@reach/router";
import NotFound from "./pages/NotFound.js";
import Skeleton from "./pages/Skeleton.js";
import Home from "./pages/Home.js";
import Catalog from "./pages/Catalog.js";
import LoadCafes from "./pages/LoadCafes.js";
import NewCafe from "./pages/NewCafe.js";
import Tutorial from "./pages/Tutorial.js";
import Cafe from "./pages/Cafe.js";
import Credits from "./pages/Credits.js";
import SkeletonLogOut from "./pages/SkeletonLogOut.js";

import "../utilities.css";

import { socket } from "../client-socket.js";

import { get, post } from "../utilities";

/**
 * Define the "App" component
 */
const App = () => {
  const [userId, setUserId] = useState(undefined);

  useEffect(() => {
    get("/api/whoami").then((user) => {
      if (user._id) {
        // they are registed in the database, and currently logged in.
        setUserId(user._id);
      }
    });
  }, []);

  const handleLogin = (res) => {
    console.log(`Logged in as ${res.profileObj.name}`);
    const userToken = res.tokenObj.id_token;
    post("/api/login", { token: userToken }).then((user) => {
      setUserId(user._id);
      post("/api/initsocket", { socketid: socket.id });
    });
  };

  const handleLogout = () => {
    setUserId(undefined);
    post("/api/logout");
  };

  return (
    <>
    {userId ?
    (
      <Router>
        <Skeleton path="/" handleLogin={handleLogin} handleLogout={handleLogout} userId={userId}/>
        <NotFound default />
        <Home path="/home" />
        <Catalog path="/catalog" />
        <LoadCafes path="/load-cafes" userId={userId}/>
        <NewCafe path="/new-cafe" userId={userId}/>
        <Tutorial path="/tutorial" userId={userId}/>
        <Cafe path="/cafe" />
        <SkeletonLogOut path="/logout" handleLogin={handleLogin} handleLogout={handleLogout} userId={userId} />
        <Credits path="/credits" />
      </Router>
    ) : (
      <Skeleton path="/" handleLogin={handleLogin} handleLogout={handleLogout} userId={userId}/>
    )}
    </>
  );
};

export default App;
