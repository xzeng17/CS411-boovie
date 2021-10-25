import "../styles/Navbar.css";
import UserProfile from "./UserProfile.js";
import Search from "./Search.js";
import BookHistory from "./BookHistory.js";
import MovieHistory from "./MovieHistory.js";
import Login from "./Login.js";
import Register from "./Register.js";
import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
  } from "react-router-dom";

function Navbar(props) {
    const {handleLogin, isLoggedIn, userRole, handleLogout } = props;

    const showLogin = ()=> {
        return (
            isLoggedIn ?
                <Redirect to="/UserProfile" />
            :
                <Login handleLogin={handleLogin} />
        )
    }

    return (
        <Router>
        <div>
            <div className="App-title">Boovie</div>
            <ul>
                <Link to="/UserProfile">UserProfile</Link>
                <Link to="/Search">Search</Link>
                <Link to="/BookHistory">BookHistory</Link>
                <Link to="/MovieHistory">MovieHistory</Link>
                {isLoggedIn
                    ? <button type="button" onClick={handleLogout}> Logout </button>
                    : <Link to="/Login">Login</Link>}
            </ul>
        </div>
        <Switch>
            <Route path="/UserProfile">
                <UserProfile isLoggedIn={isLoggedIn} userRole={userRole}/>
            </Route>
            <Route path="/Search">
                <Search />
            </Route>
            <Route path="/BookHistory">
                <BookHistory />
            </Route>
            <Route path="/MovieHistory">
                <MovieHistory />
            </Route>
            <Route path="/Login" render={showLogin} />
            <Route path="/Register">
                <Register />
            </Route>
        </Switch>
        </Router>
    );
}

export default Navbar;