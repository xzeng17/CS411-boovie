import "../styles/Main.css";
import React, { useState } from "react";

import Axios from 'axios';
import {STAGING_DOMAIN_URL, TEAM_ENDPOINT} from "../assets/constants";
import { Route, Switch, Redirect } from "react-router";

import Login from "./Main.js";
import Register from "./Register.js";
import UserProfile from "./UserProfile.js";
import BookHistory from "./BookHistory.js";
import MovieHistory from "./MovieHistory.js";
import Search from "./Search.js";


function fetchTeamInfo(clickCount, setClickCount, teamData, setTeamData) {
    console.log("Clicked");
    setClickCount(clickCount+1);

    const opt = {
        method: "GET",
        url: STAGING_DOMAIN_URL+TEAM_ENDPOINT,
      };
   
    Axios(opt)
    .then((res) => {
        if (res.status === 200) {
            console.log(res.data);
            setTeamData(teamData = res.data);
        }
    })
    .catch((err) => {
        console.log("fetch team info failed: ", err.message);
    });
}

function Main(props) {
    const { isLoggedIn, handleLoggedIn } = props; 
    const [clickCount, setClickCount] = useState(0)
    const [teamData, setTeamData] = useState(null)
    const showLogin = () => {
        return isLoggedIn ? (
            <Redirect to="/UserProfile" />
        ) : (
            <Login handleLoggedIn={handleLoggedIn} />
        );
    };
     
    const showHome = () => {
        return isLoggedIn ? <UserProfile /> : <Redirect to="/login" />;
    };
     
    return (
        <div>

            <div>
            Home Page
            </div>
            <button onClick={()=>fetchTeamInfo(clickCount, setClickCount, teamData, setTeamData)}>
                Fetch Team Information
            </button>
            <div>
                {teamData === null ? '' : JSON.stringify(teamData)}
            </div>
            <div>
                Button Clicked {clickCount} times!
            </div>

            <div className="home">
                <Switch>
                    <Route path="/login" render={Login} />
                    <Route path="/register" render={Register} />
                    <Route path="/UserProfile" render={UserProfile} />
                    <Route path="/BookHistory" render={BookHistory} />
                    <Route path="/MovieHistory" render={MovieHistory} />
                    <Route path="/Search" render={Search} />
                </Switch>
            </div>
        </div>
    );
}

export default Main;