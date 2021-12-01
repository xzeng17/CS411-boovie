import React from "react";
import Axios from 'axios';

import {LOCALHOST_URL, MOVIE_IMG_BASE} from "../assets/constants.js";
import { Redirect } from 'react-router-dom'

import "../styles/MovieHistory.css";


class BookHistory extends React.Component {
    state = {
        books: [],
        isLoggedIn: this.props.isLoggedIn,
        userRole: this.props.userRole,
        toBookItem: false,
    }

    handleRedirect = (id) => {
        this.props.setId(id);
        this.setState(() => ({ toBookItem: true }));
    }

    componentDidMount = () => {
        // console.log("component did mount");
        this.props.isLoggedIn ? this.fetchHistory() : this.setState({books: []});
    }

    fetchHistory = ()=> {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"/book/history",
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };
        
        Axios(opt)
        .then((res) => {
            if (res.status === 200) {
                this.setState({
                    books: res.data
                });
                // console.log(res.data);
                // console.log(this.state.books);
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to fetch book history")
        });
    }

    deleteItem = (id) => {
        this.props.setId(id);
        console.log(id)

        this.setState(() => ({ deleteItem: true }));

        console.log(LOCALHOST_URL+"deletebookreview");

        const opt = {
            method: "POST",
            url: LOCALHOST_URL+"deletebookreview",
            data: {
                book_id: id
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

        const books = this.state.books;

        if (this.state.toBookItem) {
            return <Redirect to='/BookItem' />
        }

        return (
        <div>
            <h3>Book History Page</h3>
            <table className="table table-striped table-bordered">
                <thead>
                    <tr >
                        <th>Title</th>
                        <th>Language</th>
                        <th>Author</th>
                    </tr>
                </thead>
                {/* <tbody>
                    {books && books.map(book =>
                        <tr id="book-item" key={book.book_id} onClick= {()=>this.handleRedirect(book.book_id)} >
                            <td><img src={MOVIE_IMG_BASE+book.image_url} alt="Img N/A"/></td>
                            <td>{book.title}</td>
                            <td>{book.language}</td>
                            <td>{book.rating}</td>
                            <td>{book.description}</td>
                        </tr>
                    )}
                </tbody>*/}

                <tbody>
                    {books && books.map(book =>
                        <tr id="book-item" key={book.book_id} onClick= {()=>this.handleRedirect(book.book_id)}>
                            <td>{book.title}</td>
                            <td>{book.language}</td>
                            <td>{book.author}</td>
                            <td>{book.description}</td>
                            {/* <td onClick={()=>{
                                    this.deleteItem(book.book_id);
                                    // this.setState(() => ({ 
                                    //     books:books.filter(function(value, index, arr){ 
                                    //     return value != book.book_id;
                                    // })}))
                                    // this.fetchHistory();
                                }
                            }>&#10006;</td> */}
                        </tr>
                    )}
                </tbody>
            </table>
        </div>
        )
    }
}

export default BookHistory;
