import React, { Fragment } from "react";
import Header from "../layout/Header";
import axios from "axios";

const News = ({news}) => {
  var news=Object.values(news);
  return (

    <div>
      { news.map((item) => (
        <>
          <h4>{item.image}</h4>
          <h4>{item.link}</h4>
          <h4>{item.summary}</h4>
          <br></br>
          </>

))}
    </div>
   
    
  )
}
export default News



   
