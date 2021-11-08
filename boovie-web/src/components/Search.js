<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
import React from "react";
import LadderBoard from "./LadderBoard";

=======
import React, { useState } from "react";
import BookSource from "./BookSource";
import CardList from "./CardList";
>>>>>>> 5b611b2 (search)

=======
import React, { useState } from "react";
import BookSource from "./BookSource";
import CardList from "./CardList";

>>>>>>> 5b611b2 (search)
=======
import React, { useState } from "react";
import BookSource from "./BookSource";
import CardList from "./CardList";

>>>>>>> 5b611b2 (search)
import SearchBar from "./SearchBar";
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
        console.log(results);
    }
    return (
        <div>
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
            <div>
                Search Page
            </div>
            <div className='LadderBoard'>
                <LadderBoard />
=======
=======
>>>>>>> 5b611b2 (search)
=======
>>>>>>> 5b611b2 (search)
            <div className="container searchApp">
                <h2 className="title is-2 has-text-centered">
                    Search For Books and Movies
                </h2>
                <SearchBar onSearch={onSearch} />
                <CardList results={state.results} /> 
<<<<<<< HEAD
<<<<<<< HEAD
>>>>>>> 5b611b2 (search)
=======
>>>>>>> 5b611b2 (search)
=======
>>>>>>> 5b611b2 (search)
            </div>
        </div>
    )
}

export default Search;