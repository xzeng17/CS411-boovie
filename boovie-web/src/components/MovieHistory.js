import React from "react";
import Axios from 'axios';

import {LOCALHOST_URL, MOVIE_IMG_BASE} from "../assets/constants.js";
import { Redirect } from 'react-router-dom'

import "../styles/MovieHistory.css";
import axios from "axios";


class MovieHistory extends React.Component {
    state = {
        movies: [],
        isLoggedIn: this.props.isLoggedIn,
        userRole: this.props.userRole,
        toMovieItem: false
    }

    //comment
    handleRedirect = (id) => {
        console.log("SDA");
            this.props.setId(id);
            this.setState(() => ({ toMovieItem: true }));
        
    }

    deleteItem = (id) => {
        this.props.setId(id);
        console.log(id)
        //this.setState(() => ({ deleteItem: true}));

        console.log(LOCALHOST_URL+"deletemoviereview");
        
        const opt = {
            method: "POST",
            url: LOCALHOST_URL+"deletemoviereview",
            data: {
                movie_id: 5
            },
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
                // "Access-Control-Allow-Origin":  "http://127.0.0.1:3000"
            }
        };

        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                console.log("Worked")
                // console.log(res.data);
                // console.log(this.state.movies);
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to work")
        });

        //this.render()



        // const headers = { 
        //     'Authorization': 'Bearer my-token',
        //     'movieid': "as"
        // };
        
        // const params = new URLSearchParams();
        // params.append('event_id', "12");
        // params.append('item_id', "34");
        // params.append('description', "56");
        // axios.post(LOCALHOST_URL+"deletemoviereview", params)
        // .then(() => console.log('Delete successful'));
    }

    componentDidMount = () => {
        // console.log("component did mount");
        this.props.isLoggedIn ? this.fetchHistory() : this.setState({movies: []});
    }

    fetchHistory = ()=> {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"/movie/history",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };
        
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                this.setState({
                    movies: res.data
                });
                // console.log(res.data);
                // console.log(this.state.movies);
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to fetch movie history")
        });
    }

    render() {
        if (!this.props.isLoggedIn) {
            return <Redirect to='/Login' />
        }

        const movies = this.state.movies;

        // if (this.props.deleteItem) {
        //     console.log("ASD")
        //     return <Redirect to='/UserProfile' />
        // }

        if (this.state.toMovieItem) {
            return <Redirect to='/MovieItem' />
        }



        return (
        <div>
            <h3>Movie History Page</h3>
            <table className="table table-striped table-bordered">
                <thead>
                    <tr>
                        <th>Picture</th>
                        <th>Title</th>
                        <th>Language</th>
                        <th>Rating</th>
                        <th>Description</th>
                    </tr>
                </thead>
                <tbody>
                    {movies && movies.map(movie =>
                        <tr id="movie-item" key={movie.movie_id} >
                            <td><img src={MOVIE_IMG_BASE+movie.image_url} alt="Img N/A" onClick= {()=>this.handleRedirect(movie.movie_id)}/></td>
                            <td>{movie.title}</td>
                            <td>{movie.language}</td>
                            <td>{movie.rating}</td>
                            <td>{movie.description}</td>
                            <td onClick={()=>this.deleteItem(movie.movie_id)}>&#10006;</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
        )
    }
}

export default MovieHistory;
