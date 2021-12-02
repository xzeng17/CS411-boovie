import React, { useState } from "react";
import Axios from 'axios';
import {LOCALHOST_URL} from "../assets/constants.js";



const updateBadges = ()=> {
    const opt = {
        method: "PUT",
        url: LOCALHOST_URL+"managebadges",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
            "Content-Type": "application/json"
        }
    };

    Axios(opt)
    .then((res) => {
        
        if (res.status === 200) {
            console.log("success")
        }
    })
    .catch((err) => {
        console.log(err)
        console.log("fail to fetch movie history")
    });
}


const deleteBadges = ()=> {
    const opt = {
        method: "DELETE",
        url: LOCALHOST_URL+"managebadges",
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
            "Content-Type": "application/json"
        }
    };

    Axios(opt)
    .then((res) => {
        
        if (res.status === 200) {
            console.log("success")
        }
    })
    .catch((err) => {
        console.log(err)
        console.log("fail to fetch movie history")
    });
}

function Manager(props) {

  return (
    <div>
        Manager Page
        <button type="button" onClick={updateBadges}>
            Assign Badges
        </button>

        <button type="button" onClick={deleteBadges}>
            Remove Badges
        </button>
    </div>
  );
}

export default Manager;