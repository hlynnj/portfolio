import React, { Component } from "react";
import GoogleLogin, { GoogleLogout } from "react-google-login";
import { Redirect } from "@reach/router";

import "../../utilities.css";
import "./Skeleton.css";

//TODO: REPLACE WITH YOUR OWN CLIENT_ID
const GOOGLE_CLIENT_ID = "419674631549-0oao1s8qtq7jm3knt38lj7c289nenio5.apps.googleusercontent.com";

const Skeleton = ({ userId, handleLogin, handleLogout }) => {
  return (
    <>
      {userId ? (
        <Redirect to="/home" />
      ) : (
        <div className="skeleton-content">
          <div className="skeleton-header">
            <img className="skeleton-card" src="https://i.ibb.co/gVz97yQ/title-card-unspace.png" height="400" />
          </div>
          <div className="skeleton-text">
            <div>where your cat cafe dreams come true.</div>
            <br></br>
            <div>You are currently logged out.</div>
            <div>Please log in to access your cafes and more!</div>
            <GoogleLogin
              clientId={GOOGLE_CLIENT_ID}
              buttonText="Login with Google"
              onSuccess={handleLogin}
              onFailure={(err) => console.log(err)}
            />
          </div>
        </div>
      )}
    </>
  );
};

export default Skeleton;
