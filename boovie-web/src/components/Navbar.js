import "../styles/Navbar.css";
import UserProfile from "./UserProfile.js";
import Search from "./Search.js";
import BookHistory from "./BookHistory.js";
import MovieHistory from "./MovieHistory.js";
import MovieItem from "./MovieItem.js";
import BookItem from './BookItem';
import Login from "./Login.js";
import Register from "./Register.js";
import Manager from "./Manager.js";
import React, {useState} from "react";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link,
    Redirect
  } from "react-router-dom";

function Navbar(props) {
    const {handleLogin, isLoggedIn, userRole, handleLogout} = props;
    const [selectedId, setId] = useState(0);

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
            <div id="Top-bar">
                <h1 className="App-title">Boovie</h1>
                <ul className="Top-bar-manu">
                    <Link className="Top-bar-button" to="/Search">Search</Link> 
                    <Link className="Top-bar-button" to="/UserProfile">UserProfile</Link>
                    <Link className="Top-bar-button" to="/BookHistory">BookHistory</Link>
                    <Link className="Top-bar-button" to="/MovieHistory">MovieHistory</Link>
                    {isLoggedIn
                        ? <u className="Top-bar-button" onClick={handleLogout}>Logout</u>
                        : <Link className="Top-bar-button" to="/Login">Login</Link>}
                    {isLoggedIn && userRole === 'manager'
                        ? <Link className="Top-bar-button" to="/Manager">Hello Manager</Link>
                        : <></>
                    }
                </ul>
            </div>
            <Switch>
                <Route path="/UserProfile">
                    <UserProfile isLoggedIn={isLoggedIn} userRole={userRole} handleLogout = {handleLogout}/>
                </Route>
                <Route path="/Search">
                    <Search setId={setId}/>
                </Route>
                <Route path="/BookHistory">
                    <BookHistory isLoggedIn={isLoggedIn} userRole={userRole} setId={setId}/>
                </Route>
                <Route path="/MovieHistory">
                    <MovieHistory isLoggedIn={isLoggedIn} userRole={userRole} setId={setId}/>
                </Route>
                <Route path="/Login" render={showLogin} />
                <Route path="/Manager" render={()=>isLoggedIn && userRole === 'manager' ? <Manager /> : <></>} />
                <Route path="/Register">
                    <Register />
                </Route>
                <Route path="/MovieItem">
                    <MovieItem movie_id={selectedId} isLoggedIn={isLoggedIn}/>
                </Route>
                <Route path="/BookItem">
                    <BookItem book_id={selectedId} isLoggedIn={isLoggedIn}/>
                </Route>
            </Switch>
        </Router>
    );
}

export default Navbar;