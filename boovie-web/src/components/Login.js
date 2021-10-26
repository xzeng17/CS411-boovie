import React, { useState } from "react";
import {LOCALHOST_URL, LOGIN_ENDPOINT} from "../assets/constants.js";
import Register from "./Register.js";

import Popup from 'reactjs-popup';
import 'reactjs-popup/dist/index.css';

import Axios from 'axios';

function Login(props) {
    const {handleLogin} = props;
    const [input_useremail, setUseremail] = useState(null)
    const [input_password, setPassword] = useState(null)

    const submitLogin = ()=> {
        const opt = {
            method: "POST",
            url: LOCALHOST_URL+LOGIN_ENDPOINT,
            data: {
                Email: input_useremail,
                Password: input_password
            },
            headers: {
                "Content-Type": "application/json"
            }
          };
       
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                // res.data is token returned from server
                console.log(res.data);
                handleLogin(res.data);
            }
        })
        .catch((err) => {
            console.log("Login failed: ", err.message);
            showMessage("Login failed.");
        });
    }

    const showMessage = (text)=> {
        document.querySelector('.login-msg').innerHTML = text;
    }

    return (
        <div>
            <div>
                Login page
            </div>
            <div>
                <label htmlFor="name">User Email: 
                    <input type="text" onChange={(event)=>setUseremail(event.target.value)}/>
                </label>
                <label htmlFor="name">User Password: 
                    <input type="password" onChange={(event)=>setPassword(event.target.value)} />
                </label>
                <button type="button" onClick={submitLogin}>
                    Login
                </button>
            </div>
            <div className="login-msg" />

            <Popup trigger={<button> New User? Register Here! </button>} position="center">
                <Register />
            </Popup>
        </div>
    );
}

export default Login;