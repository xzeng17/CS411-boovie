import React from "react";
import Axios from 'axios';
import {LOCALHOST_URL} from "../assets/constants.js";
import { Redirect } from 'react-router-dom'

class MovieItem extends React.Component {
    state = {
        movieInfo: {title: "place_holder"},
        added: true
    }
    
    componentDidMount = () => {
        // console.log("component did mount");
        this.fetchHistory();
    }

    fetchHistory = ()=> {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"movie/details?movie_id="+this.props.movie_id,
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };

        Axios(opt)
        .then((res) => {
            
            if (res.status === 200) {
                this.setState({movieInfo: res.data})
                this.getHistory();
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to fetch movie history")
        });
    }

    getHistory = () => {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"movie/changeHistory?movie_id="+this.props.movie_id,
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
          };
       
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                // res.data is token returned from server
                console.log(res.data);
                this.setState({added: true});
            } else {
                this.setState({added: false});
            }
        })
        .catch((err) => {
            console.log("Login failed: ", err.message);
            this.setState({added: false});
        });
    }


    addToHistory = () => {
        const opt = {
            method: "POST",
            url: LOCALHOST_URL+"movie/changeHistory",
            data: {
                movie_id: this.props.movie_id
            },
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
          };
       
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                // res.data is token returned from server
                console.log(res.data);
                this.setState({added: true})
            }
        })
        .catch((err) => {
            console.log("Login failed: ", err.message);

        });
    }

    removeFromHistory = () => {
        const opt = {
            method: "DELETE",
            url: LOCALHOST_URL+"movie/changeHistory",
            data: {
                movie_id: this.props.movie_id
            },
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
          };
       
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                // res.data is token returned from server
                console.log(res.data);
                this.setState({added: false})
            }
        })
        .catch((err) => {
            console.log("Login failed: ", err.message);

        });
    }

    render() {
        if (!this.props.isLoggedIn) {
            return <Redirect to='/Login' />
        }
        
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
                {this.state.added 
                ? <button onClick={this.removeFromHistory}>
                    Remove from list
                </button> 
                : <button onClick={this.addToHistory}>
                    Add to list
                </button> }
            </div>
        ) 
    }
}

export default MovieItem;