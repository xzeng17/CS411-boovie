import React, { useState } from "react";
import './App.css';
import { Switch, Route } from "react-router-dom";
import Login from './components/Login';
import Navbar from './components/Navbar';
import Main from './components/Main';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem("TOKEN_KEY") ? true : false);
  const [userRole, setRole] = useState(localStorage.getItem("ROLE") ? localStorage.getItem("ROLE") : null);
 
  const logout = () => {
    console.log("log out");
    localStorage.removeItem("TOKEN_KEY");
    localStorage.removeItem("ROLE");
    setIsLoggedIn(false);
    setRole(null);
  };
 
  const loggedIn = (response) => {
    if (response["TOKEN"]) {
      console.log("response");
      localStorage.setItem("TOKEN_KEY", response["TOKEN"]);
      localStorage.setItem("ROLE", response["ROLE"]);
      localStorage.setItem("USEREMAIL", response["User_email"]);
      setIsLoggedIn(true);
      setRole(response["ROLE"]);
    }
  };

  return (
    <div className="App">
      <div>
        <Navbar handleLogin={loggedIn} isLoggedIn={isLoggedIn} userRole={userRole} handleLogout={logout}/>
      </div>
    </div>
  )
}

export default App;
