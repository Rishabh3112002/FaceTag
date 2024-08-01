import React, { useState } from "react";
import "./Navbar.css";

function Navbar() {

  return (
    <nav className="navbar1">
      <ul className="navbar-nav1">
      <li className="nav-item-first1">
        <a href="/" className="logo">
          <img src="/src/assets/logo.png" alt="Logo" className="nav-logo" />
        </a>
        </li>
        <li className="nav-item1">
          <a href="https://github.com/Rishabh3112002" target="_blank" className="nav-link1">
            GitHub
          </a>
        </li>
        <li className="nav-item1">
          <a href="https://www.linkedin.com/in/rishabhk31/" target="_blank" className="nav-link1">
            LinkedIn
          </a>
        </li>
        <li className="nav-item1">
          <a href="https://rishabhkathiravan.pythonanywhere.com/" target="_blank" className="nav-link1">
            Website
          </a>
        </li>
        <li className="nav-item1">
          <a href="https://rishabhkathiravan.pythonanywhere.com/" target="_blank" className="nav-link1">
            Code
          </a>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;