import React, { useState } from "react";
import "../styles/Home.css";
import Axios from 'axios';
import {STAGING_DOMAIN_URL, TEAM_ENDPOINT} from "../assets/constants";


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

function Home() {
    const [clickCount, setClickCount] = useState(0)
    const [teamData, setTeamData] = useState(null)

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
        </div>
    )
}

export default Home;