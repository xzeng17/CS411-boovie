import React from "react";

export default function Card(props) {
  const { movie } = props;
  // console.log(movie.image_url);
  return (
    <div className="resultCard">
      <figure className="image is-48x48">
        <img src={movie.image_url} />
      </figure>
      <h4 className="bolder">{movie.title}</h4>
    </div>
  );
}