import React, { Fragment } from "react";
import Header from "../layout/Header";
import axios from "axios";

const News = () => {
  const getNews = async () => {
    console.log("working getnews");
    const res = await axios.get(
      `https://farmers-assistant-backend.herokuapp.com/news`
    );
    console.log("news", res.data);
  };
  getNews();
  return (
    <Fragment>
      <Header />
      <h1>About this app</h1>
      <p>search github user</p>
      <small>version: 1.0.0</small>
    </Fragment>
  );
};
export default News;
