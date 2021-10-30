import React, { useState }  from "react";

import {LOCALHOST_URL, REGISTER_ENDPOINT} from "../assets/constants.js";

import Axios from 'axios';

function Register(props) {
    const [input_useremail, setUseremail] = useState(null)
    const [input_password, setPassword] = useState(null)
    const [input_repeatPassword, setRepeatPassword] = useState(null)
    const [disabled, setDisabled] = useState(false)

    const validateEmail = (email)=> {
        const re = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
        return re.test(String(email).toLowerCase());
    }

    const showAlert = (text)=> {
        document.querySelector('.register-msg').innerHTML = text;
    }

    const submitRegister = ()=> {
        if (input_useremail===null || input_password===null || input_repeatPassword===null) {
            showAlert("All fileds are required!");
            return;
        }
        if (!validateEmail(input_useremail)) {
            showAlert("Invalid Email!");
            return;
        }
        if (input_password !== input_repeatPassword) {
            showAlert("Passwords do not match!");
            return;
        }

        const opt = {
            method: "POST",
            url: LOCALHOST_URL+REGISTER_ENDPOINT,
            data: {
                Email: input_useremail,
                Password: input_password,
                Role: "user"
            },
            headers: {
                "Content-Type": "application/json"
            }
          };
        
        setDisabled(true);
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                showAlert("Registeration Successful!");
            } else {
                showAlert("Registeration failed.");
                setDisabled(false);
            }
        })
        .catch((err) => {
            console.log("Registeration failed: ", err.message);
            showAlert("Registeration failed.");
            setDisabled(false);
        });
    }

    return (
        <div>
            Register Page

            <div>
                <label for="name">User Email: 
                    <input type="text" onChange={(event)=>setUseremail(event.target.value)}/>
                </label>
                <label for="name">Password: 
                    <input type="password" onChange={(event)=>setPassword(event.target.value)} />
                </label>
                <label for="name">Repeat Password: 
                    <input type="password" onChange={(event)=>setRepeatPassword(event.target.value)} />
                </label>
                <button disabled={disabled} onClick={submitRegister}>
                    Register
                </button>
                <div class="register-msg">
                </div>
            </div>

        </div>
    )
}

export default Register;