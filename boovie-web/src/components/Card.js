import React from "react";

export default function Card(props) {
  const { movie } = props;
  console.log("https://image.tmdb.org/t/p/w500/" + movie.image_url);
  return (
    <div class="resultCard">
      <figure className="image is-48x48">
        <img
          src={"https://image.tmdb.org/t/p/w500/" + movie.image_url}
        />
      </figure>
      <h4 class="bolder">{movie.title}</h4>
      <span><b>Year:</b>{movie.published_date}</span>
    </div>
  );
}