import React, { useState } from "react";
import './App.css';
import Navbar from './components/Navbar';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(localStorage.getItem("TOKEN_KEY") ? true : false);
  const [userRole, setRole] = useState(null);
 
  const logout = () => {
    console.log("log out");
    localStorage.removeItem("TOKEN_KEY");
    setIsLoggedIn(false);
    setRole(null);
  };
 
  const loggedIn = (response) => {
    if (response["TOKEN"]) {
      localStorage.setItem("TOKEN_KEY", response["TOKEN"]);
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
