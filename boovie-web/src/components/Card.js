import React, { useState } from "react";
import { Redirect } from 'react-router-dom';

export default function Card(props) {
  const [shouldRedirect, setShouldRedirect] = useState(false);
  const [shouldRedirectBook, setShouldRedirectBook] = useState(false);
  const movie = props.movie;

  const handleRedirect = (movie, setId) => {
    if ("movie_id" in movie) {
      console.log(movie);
      setId(movie.movie_id);
      setShouldRedirect(true);
    }
    if ("isbn" in movie) {
      setId(movie.id);
      setShouldRedirectBook(true);
    }
  }
  
  if (shouldRedirect) {
    return <Redirect to='/MovieItem' />
  }
  if(shouldRedirectBook) {
    return <Redirect to='/BookItem' />
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