import React from "react";

export default function Card(props) {
  const { movie } = props;
  console.log("https://image.tmdb.org/t/p/w500/" + movie.image_url);
  return (
    <div class="resultCard">
      <figure className="image is-48x48">
        <img
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
          src={movie.image_url}
        />
      </figure>
      <h4 class="bolder">{movie.title}</h4>
      {/* <span><b>Year:</b>{movie.published_date}</span> */}
=======
=======
>>>>>>> 5b611b2 (search)
          src={"https://image.tmdb.org/t/p/w500/" + movie.image_url}
        />
      </figure>
      <h4 class="bolder">{movie.title}</h4>
      <span><b>Year:</b>{movie.published_date}</span>
<<<<<<< HEAD
>>>>>>> 5b611b2 (search)
=======
          src={movie.image_url}
        />
      </figure>
      <h4 class="bolder">{movie.title}</h4>
      {/* <span><b>Year:</b>{movie.published_date}</span> */}
>>>>>>> b8f4ed3 (added search:)
=======
>>>>>>> 5b611b2 (search)
=======
          src={movie.image_url}
        />
      </figure>
      <h4 class="bolder">{movie.title}</h4>
      {/* <span><b>Year:</b>{movie.published_date}</span> */}
>>>>>>> b8f4ed3 (added search:)
    </div>
  );
}