import React, { useState } from "react";
import './App.css';
import Login from './components/Login';
import Navbar from './components/Navbar';
import Main from './components/Main';
import {TOKEN_KEY} from './assets/constants';


function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(
    localStorage.getItem(TOKEN_KEY) ? true : false
  );
 
  const logout = () => {
    console.log("log out");
    localStorage.removeItem(TOKEN_KEY);
    setIsLoggedIn(false);
  };
 
  const loggedIn = (token) => {
    if (token) {
      localStorage.setItem(TOKEN_KEY, token);
      setIsLoggedIn(true);
    }
  };

  return ( 
    <div className="App">
      <div>
        <Navbar/>
        <Main isLoggedIn={isLoggedIn} handleLogout={logout}/>
      </div>
    </div>
  )
}

export default App;
