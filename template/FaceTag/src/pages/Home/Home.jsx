import React, { useState, useEffect, useRef } from "react";
import "./Home.css";
import Navbar from "../../components/Navbar/Navbar";
import Landing from "../../components/Landing/Landing";

function Home() {
  return(
    <>
    <div className="home-page-main">
      <Navbar />
      <Landing />
    </div>
    </>
  )
}

export default Home;