import React from 'react';
import '../css/Home.css';

export default function Home() {
    return (
      <div className="right-content">
        <ul id="layout-tabs">
          <li>
            Main Dining
          </li>
          <li>
            Outdoor
          </li>
        </ul>
        <div id="layout">
          <div id="layout-legend-content">
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