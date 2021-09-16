import React, { useState } from "react";
import "../styles/Home.css";
import Axios from 'axios';
import {STAGING_DOMAIN_URL, TEAM_ENDPOINT} from "../assets/constants";

function fetchTeamInfo(setClickCount, clickCount) {
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
        }
    })
    .catch((err) => {
        console.log("fetch team info failed: ", err.message);
        return (
            <div>
                Fetch team info failed!
            </div>
        )
    });
}

function Home() {
    const [clickCount, setClickCount] = useState(0)

    return (
        <div>
            <div>
            Home Page
            </div>
            <button onClick={()=>fetchTeamInfo(setClickCount, clickCount)}>
                Fetch Team Information
            </button>
            <div>
                Button Clicked {clickCount} times!
            </div>
        </div>
    )
}

export default Home;