import React from "react";
import GoogleLogin, { GoogleLogout } from "react-google-login";

import LinkButton from "../modules/LinkButton.js";

import "../../utilities.css";
import "./Skeleton.css";

//TODO: REPLACE WITH YOUR OWN CLIENT_ID
const GOOGLE_CLIENT_ID = "419674631549-0oao1s8qtq7jm3knt38lj7c289nenio5.apps.googleusercontent.com";

const SkeletonLogOut = ({userId, handleLogin, handleLogout}) => {
    return (
        <>
          {userId ? (
            <div className="skeleton-content">
            <div className="skeleton-header">Please click below to logout</div>
            <GoogleLogout
            clientId={GOOGLE_CLIENT_ID}
            buttonText="Logout from Google"
            onLogoutSuccess={handleLogout}
            onFailure={(err) => console.log(err)}
            />
            <div className="skeleton-text">
              <div>Not what you were looking for?</div>
              <div>Click here to return to home.</div>
            </div>
            <div className="skeleton-button">
            <LinkButton link="/home" text="Home" />
            </div>
          </div>
          ) : (
            <div>
            <div>You have been logged out!
                Click here to log back in.
            </div>
            <LinkButton link="/" text="Login"/>
            </div>
          )}
        </>
      );
};

export default SkeletonLogOut;