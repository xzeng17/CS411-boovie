import React, { useState } from "react";
import { Redirect } from 'react-router-dom';

export default function Card(props) {
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const movie = props.movie;
  // console.log(movie.image_url);

  const handleRedirect = (movie, setId) => {
    if ("movie_id" in movie) {
      console.log(movie);
      setId(movie.movie_id);
      setShouldRedirect(true);
    }
    if ("isbn" in movie) {
      // handle bookitem redirection
    }
  }
  
  if (shouldRedirect) {
    return <Redirect to='/MovieItem' />
  }

  return (
    <div className="resultCard" onClick= {()=>handleRedirect(movie, props.setId)}>
      <figure className="image is-48x48">
        <img src={movie.image_url} />
      </figure>
      <h4 className="bolder">{movie.title}</h4>
    </div>
  );
}