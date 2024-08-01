import React from "react";
import "./Landing.css";
import { Link } from "react-router-dom";

function Landing() {
  return (
    <div id="land" className="landing">
      <h1 className="name">FaceTag</h1>
      <p className="position">Face-based Recognition System</p>
      <div className="desc">
        <p className="about">FaceTag is an advanced face recognition system designed to identify individuals by scanning an entire database of images. Utilizing cutting-edge machine learning algorithms, FaceTag accurately matches a person's face against a comprehensive repository, ensuring precise identification. This system is ideal for applications requiring robust security, efficient attendance tracking, or seamless access control, providing a reliable and user-friendly solution for modern facial recognition needs.</p>
      </div>
      <div className="button-container">
        <Link to="/page1">
          <button className="nav-button">Add New Entry</button>
        </Link>
        <Link to="/page2">
          <button className="nav-button">Face Recognition</button>
        </Link>
      </div>
    </div>
  );
}

export default Landing;