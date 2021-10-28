import React from "react";
import {LOCALHOST_URL} from "../assets/constants.js";

import "../styles/LadderBoard.css";
import Axios from 'axios';

class LadderBoard extends React.Component {
    state = {
        top_3_rating: [],
        top_3_rating_recent: []
    }
    
    componentDidMount = () => {
        this.fetchTopUsers();
    }

    fetchTopUsers = () => {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"movie/topusers",
            headers: {
                "Content-Type": "application/json"
            }
        };
       
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                console.log(res.data);
                this.setState({top_3_rating: res.data.top_3_rating});
                this.setState({top_3_rating_recent: res.data.top_3_rating_recent});
            }
        })
        .catch((err) => {
            console.log("Fail to get top users: ", err.message);
        });
    }

    render() {
        const top_3_rating = this.state.top_3_rating;
        const top_3_rating_recent = this.state.top_3_rating_recent;

        return (
            <div>
   
                <div className="Ladder-board">
                <table className="top-3-rating">
                    <thead>
                        <tr>
                            <th>Top Users Who Watched Most High Rating Movies</th>
                        </tr>
                    </thead>
                    <tbody>
                        {top_3_rating && top_3_rating.map(user =>
                            <tr key={user} >
                                <td>{user}</td>
                            </tr>
                        )}
                    </tbody>
                </table>
                <table className="top-3-rating-recent">
                    <thead>
                        <tr>
                            <th>Top Users Who Watched Most Recent High Rating Movies</th>
                        </tr>
                    </thead>
                    <tbody>
                        {top_3_rating_recent && top_3_rating_recent.map(user =>
                            <tr key={user} >
                                <td>{user}</td>
                            </tr>
                        )}
                    </tbody>
                </table>
                </div>
            </div>
        ) 
    }
}

export default LadderBoard;
