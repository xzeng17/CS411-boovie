import React from "react";
import Card from "./Card";

function CardList(props) {
  const results = props.results;
  let data = [];
  if (results.data) {
    data = results.data || [];
  }
  console.log(data);
  return (
    <div className="result">
      {data.map((item) => (
        <Card key={"movie_id" in item ? item.movie_id : item.isbn} movie={item} setId={props.setId}/>
      ))}
    </div>
  );
}

export default CardList;