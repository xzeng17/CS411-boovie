import "../styles/Navbar.css";
import UserProfile from "./UserProfile.js";
import Search from "./Search.js";
import BookHistory from "./BookHistory.js";
import MovieHistory from "./MovieHistory.js";
import React from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

function Navbar(props) {
    const { isLoggedIn, handleLogout } = props;
    return (
        <Router>
        <div>
            <div className="App-title">Boovie</div>
            <ul>
                <Link to="/UserProfile">UserProfile</Link>
                <Link to="/Search">Search</Link>
                <Link to="/BookHistory">BookHistory</Link>
                <Link to="/MovieHistory">MovieHistory</Link>
            </ul>
        </div>
        <Switch>
            <Route exact path="/UserProfile">
                <UserProfile />
            </Route>
            <Route exact path="/Search">
                <Search />
            </Route>
            <Route exact path="/BookHistory">
                <BookHistory />
            </Route>
            <Route exact path="/MovieHistory">
                <MovieHistory />
            </Route>
        </Switch>
        </Router>
    );
}

export default Navbar;