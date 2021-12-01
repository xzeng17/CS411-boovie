import React from "react";
import Axios from 'axios';
import {LOCALHOST_URL} from "../assets/constants.js";
import { Redirect } from 'react-router-dom'

class BookItem extends React.Component {
    state = {
        bookInfo: {title: "place_holder"},
        added: true
    }
    componentDidMount = () => {
        // console.log("component did mount");
        this.fetchHistory();
    }

    fetchHistory = ()=> {
        console.log(this.props)
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"book/details?book_id="+this.props.book_id,
            headers: {
                "Authorization": "Bearer " + localStorage.getItem("TOKEN_KEY"),
                "Content-Type": "application/json"
            }
        };

        Axios(opt)
        .then((res) => {
            
            if (res.status === 200) {
                this.setState({bookInfo: res.data})
                this.getHistory();
            }
        })
        .catch((err) => {
            console.log(err)
            console.log("fail to fetch book history")
        });
    }

    getHistory = () => {
        const opt = {
            method: "GET",
            url: LOCALHOST_URL+"book/changeHistory?book_id="+this.props.book_id,
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
           
            url: LOCALHOST_URL+"book/changeHistory",
            data: {
                book_id: this.props.book_id
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
            url: LOCALHOST_URL+"book/changeHistory",
            data: {
                book_id: this.props.book_id
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
                <h3>{this.state.bookInfo.title}</h3>          
                <p>Author: {this.state.bookInfo.author}</p>      
                <p>Publisher: {this.state.bookInfo.publisher}</p>
                <p>Published date: {this.state.bookInfo.published_date}</p>
                <p>Language: {this.state.bookInfo.language}</p>
                <p>Page count: {this.state.bookInfo.page_count}</p>
                <p>Description: {this.state.bookInfo.description}</p>
                
               
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

export default BookItem;