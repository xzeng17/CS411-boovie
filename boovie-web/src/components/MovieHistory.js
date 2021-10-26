import React from "react";
import Axios from 'axios';

import {LOCALHOST_URL, MOVIE_IMG_BASE} from "../assets/constants.js";
import { Redirect, Link } from 'react-router-dom'

import MovieItem from "./MovieItem.js";
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
        console.log("component did mount");
        this.props.isLoggedIn ? this.fetchHistory() : this.setState({movies: []});
    }

    fetchHistory = ()=> {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"getMovieHistory",
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
        let movies = this.props.isLoggedIn ? this.state.movies : [];

        if (this.state.toMovieItem) {
            return <Redirect to='/MovieItem' id={this.state.movie_id}/>
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
                        <tr id="movie-item" key={movie.movie_id} onClick= {()=>this.handleRedirect(movie.movie_id)} >
                            <td><img src={MOVIE_IMG_BASE+movie.image_url} alt="Img N/A"/></td>
                            <td>{movie.title}</td>
                            <td>{movie.language}</td>
                            <td>{movie.rating}</td>
                            <td>{movie.description}</td>
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
        )
    }
}

export default MovieHistory;



// function MovieHistory(props) {
//     const [movies, setMovies] = useState([])

//     const fetchHistory = ()=> {

//         const opt = {
//             method: "GET",
//             url: LOCALHOST_URL+"getMovieHistory",
//             headers: {
//                 "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
//                 "Content-Type": "application/json"
//             }
//           };
       
//         Axios(opt)
//         .then((res) => {
//             if (res.status === 200) {
//                 // res.data is token returned from server
//                 console.log("responsed success");
//                 // setMovies(res.data);
//                 console.log(movies)
//             }
//         })
//         .catch((err) => {
//             console.log(err)
//             console.log("fail to fetch movie history")
//         });
//     }

//     return (
//         <div>
//             <h3>Movie History Page</h3>
//             <table className="table table-striped table-bordered">
//                 <thead>
//                     <tr>
//                         <th>Picture</th>
//                         <th>Title</th>
//                         <th>Language</th>
//                         <th>Rating</th>
//                         <th>Description</th>
//                     </tr>
//                 </thead>
//                 <tbody>
//                     {movies && movies.map(movie =>
//                         <tr key={movie.movie_id}>
//                             <td>preview picture</td>
//                             <td>{movie.title}</td>
//                             <td>{movie.language}</td>
//                             <td>{movie.language}</td>
//                             <td>{movie.description}</td>
//                         </tr>
//                     )}
//                 </tbody>
//             </table>
//         </div>
//     )
// }

// export default MovieHistory;