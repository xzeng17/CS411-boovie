import React from "react";
import Axios from 'axios';
import {LOCALHOST_URL, MOVIE_VIDEO_BASE} from "../assets/constants.js";

class MovieItem extends React.Component {
    state = {
        movieInfo: {title: "place_holder"}
    }
    
    componentDidMount = () => {
        console.log("component did mount");
        this.fetchHistory();
    }

    fetchHistory = ()=> {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+MOVIE_VIDEO_BASE+this.props.movie_id,
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };
        
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                this.setState({movieInfo: res.data})
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to fetch movie history")
        });
    }

    render() {
        return (
        <div>
            <h3>{this.state.movieInfo.title}</h3>
            {
                this.state.movieInfo.video_url === "N/A" ? <p>No Preview Video</p> : 
                <iframe
                    width="450"
                    height="300"
                    src={`https://www.youtube.com/embed/${this.state.movieInfo.video_url}`}
                    frameBorder="0"
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    title="Embedded youtube"
                />
            }
            
            <p>Description: {this.state.movieInfo.description}</p>
            <p>Published date: {this.state.movieInfo.published_date}</p>
            <p>Rating: {this.state.movieInfo.rating}</p>
            <p>Original Language: {this.state.movieInfo.language}</p>
        </div>
        )
    }
}

export default MovieItem;