import React from 'react';
import axios from 'axios';
import Tabs from '../Component/Tabs';
import '../css/Home.css';

//Layout tabs will soon be replaced with dynamic version
export default function Home() {
  const url = "http://127.0.0.1:5000/message";

  function testFn() {
    axios.get(url)
    .then(data => console.log(data))
    .catch(err => console.log(err));
  }

  return (
    <div className="right-content">
      <Tabs isEdit={false} />
      <div id="layout">
        <div id="layout-legend-content">
          <button onClick={testFn}>
            WATER REFILL TEST
          </button>
          <div id="layout-legend">
            <ul id="layout-legend-elements">
              <li>
                <span className="legend-colors">
                </span>
                Free
              </li>
              <li>
                <span className="legend-colors">
                </span>
                Occupied
              </li>
              <li>
                <span className="legend-colors">
                </span>
                Need Cleaning
              </li>
              <li>
                <span className="legend-colors">
                </span>
                Attention
              </li>
            </ul>
          </div>
        </div>
        <div id="layout-content"></div>
      </div>
    </div>
  );
};