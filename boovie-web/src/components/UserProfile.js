import React, { useEffect, useState } from "react";
import { Redirect } from 'react-router-dom'
import Axios from 'axios';

import {LOCALHOST_URL} from "../assets/constants.js";


function UserProfile(props) {
    const {isLoggedIn, userRole, handleLogout} = props;
    const [old_password, setOldPW] = useState('')
    const [new_password, setNewPW] = useState('')
    const [new_repeatpassword, setNewRepeatPW] = useState('')
    const [disabled, setDisabled] = useState(false)
    const [badgeInfo, setBadgeInfo] = useState('')
    const [userEmail, setEmail] = useState(localStorage.getItem("USEREMAIL") ? localStorage.getItem("USEREMAIL") : null);

    const fetchBadge = ()=> {
        console.log(userEmail)
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"user/badge?user_email="+ userEmail,
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };

        Axios(opt)
        .then((res) => {
            
            if (res.status === 200) {
                setBadgeInfo(res.data)
                console.log("BADGE INFO =====>")
                console.log(res.data)
                console.log(badgeInfo)
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to fetch user badge")
        });
    }

    useEffect(() => {
        fetchBadge()
    }, [0])

    const submitChange = () => {
        if (old_password==='' || new_password==='' || new_repeatpassword==='') {
            showAlert("All fileds are required!");
            return;
        }

        if (new_password !== new_repeatpassword) {
            showAlert("New passwords do not match!");
            return;
        }

        const opt = {
            method: "POST",
            url: LOCALHOST_URL+"passwordchange",
            data: {
                old_password: old_password,
                new_password: new_password,
            },
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
          };
        
        setDisabled(true);
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                showAlert("Change Successful!");
                handleLogout();
            } else {
                showAlert("Request failed.");
                setDisabled(false);
            }
        })
        .catch((err) => {
            console.log("Request failed: ", err.message);
            showAlert("Request failed.");
            setDisabled(false);
        });
    }

    const showAlert = (text)=> {
        document.querySelector('.alert-msg').innerHTML = text;
    }

    if (!isLoggedIn) {
        return <Redirect to='/Login' />
    }

    return (
        <div>
            <div>
                User Profile Page
            </div>

            {isLoggedIn ? 
                <div>
                    <p> You are logged in as {userRole}! </p>
                    {
                        badgeInfo.classic_badge === "Yes" &&
                        <p> You like many old movies, we grant you an Old School Badge ! </p>
                    }
                    {
                        badgeInfo.fashion_badge === "Yes" &&
                        <p> You like many new movies, we grant you a Fashion Badge ! </p>
                    }
                    {
                        badgeInfo.keeper_badge === "Yes" &&
                        <p> You've collected many movies, we grant you a Keeper Badge ! </p>
                    }
                </div>
                :
                <div>
                    Please Login first!
                </div>
            }


            <div>
                <p>change password</p>
                <label for="name">Old Password: 
                    <input type="password" onChange={(event)=>setOldPW(event.target.value)}/>
                </label>
                <label for="name">New Password: 
                    <input type="password" onChange={(event)=>setNewPW(event.target.value)} />
                </label>
                <label for="name">New Repeat Password: 
                    <input type="password" onChange={(event)=>setNewRepeatPW(event.target.value)} />
                </label>
                <button disabled={disabled} onClick={submitChange}>
                    Submit
                </button>
                <div class="alert-msg">
                </div>
            </div>
            
        </div>
    )
}

export default UserProfile;