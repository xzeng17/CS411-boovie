import React from "react";
import Axios from 'axios';

import {LOCALHOST_URL, MOVIE_IMG_BASE} from "../assets/constants.js";
import { Redirect } from 'react-router-dom'

import "../styles/MovieHistory.css";


class MovieHistory extends React.Component {
    state = {
        movies: [],
        isLoggedIn: this.props.isLoggedIn,
        userRole: this.props.userRole,
        toMovieItem: false,
    }

    handleRedirect = (id) => {
        this.props.setId(id);
        this.setState(() => ({ toMovieItem: true }));
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

    deleteItem = (id) => {
        this.props.setId(id);
        console.log(id)

        this.setState(() => ({ deleteItem: true }));

        console.log(LOCALHOST_URL+"deletemoviereview");

        const opt = {
            method: "POST",
            url: LOCALHOST_URL+"deletemoviereview",
            data: {
                movie_id: id
            },
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };

        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                console.log("Worked")
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to work")
        });
    }

    render() {
        if (!this.props.isLoggedIn) {
            return <Redirect to='/Login' />
        }

        const movies = this.state.movies;

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
                {/* <tbody>
                    {movies && movies.map(movie =>
                        <tr id="movie-item" key={movie.movie_id} onClick= {()=>this.handleRedirect(movie.movie_id)} >
                            <td><img src={MOVIE_IMG_BASE+movie.image_url} alt="Img N/A"/></td>
                            <td>{movie.title}</td>
                            <td>{movie.language}</td>
                            <td>{movie.rating}</td>
                            <td>{movie.description}</td>
                        </tr>
                    )}
                </tbody>*/}

                <tbody>
                    {movies && movies.map(movie =>
                        <tr id="movie-item" key={movie.movie_id} >
                            <td><img src={MOVIE_IMG_BASE+movie.image_url} alt="Img N/A" onClick= {()=>this.handleRedirect(movie.movie_id)}/></td>
                            <td>{movie.title}</td>
                            <td>{movie.language}</td>
                            <td>{movie.rating}</td>
                            <td>{movie.description}</td>
                            <td onClick={()=>{
                                    this.deleteItem(movie.movie_id);
                                    // this.setState(() => ({ 
                                    //     movies:movies.filter(function(value, index, arr){ 
                                    //     return value != movie.movie_id;
                                    // })}))
                                    // this.fetchHistory();
                                }
                            }>&#10006;</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
        )
    }
}

export default MovieHistory;
