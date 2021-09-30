import React from "react";
import "./Crop.css";
import Header from "../layout/Header";
export default function Crop() {
  return (
    <>
      {/* <Header navPosition="right" className="reveal-from-bottom" /> */}

      <div class="form-container">
        <form class="register-form">
          {/* <div class="success-message">Success! Thank you for registering</div> */}
          <input
            id="phosphorous"
            class="form-field"
            type="text"
            placeholder="Phosphorous"
            name="phosphorous"
          />

          {/* <span id="first-name-error">Please enter a first name</span> */}
          <input
            id="pottasium"
            class="form-field"
            type="text"
            placeholder="Pottasium"
            name="pottasium"
          />

          {/* <span id="last-name-error">Please enter a last name</span> */}
          <input
            id="ph"
            class="form-field"
            type="text"
            placeholder="ph level"
            name="ph"
          />
          <input
            id="rainfall"
            class="form-field"
            type="text"
            placeholder="Rainfall (in mm)"
            name="rainfall"
          />
          <input
            id="state"
            class="form-field"
            type="text"
            placeholder="State"
            name="state"
          />

          {/* <span id="email-error">Please enter an email address</span> */}
          <button class="form-field" type="submit">
            Predict
          </button>
        </form>
      </div>
    </>
  );
}
