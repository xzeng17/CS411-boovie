import React, { useState } from "react";
import BookSource from "./BookSource";
import CardList from "./CardList";
import SearchBar from "./SearchBar";
import LadderBoard from "./LadderBoard";


function Search(props) {
    const [state, setState] = useState({
        results: []
    });

    const onSearch = async(text)=> {
        const results = await BookSource.get("", {
            params: {query: text}
        })
        setState(prevState => {
            return {...prevState, results: results}
        })
        // console.log("results are:");
        // console.log(results);
    }
    return (
        <div>
            <div className="container searchApp">
                <h2 className="title is-2 has-text-centered">
                    Search For Books and Movies
                </h2>
                <SearchBar onSearch={onSearch} />
                <CardList results={state.results} /> 
            </div>
            <LadderBoard/>
        </div>
    )
}

export default Search;