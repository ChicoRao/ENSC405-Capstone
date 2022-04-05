import React from 'react';
import icon from '../../../assets/icon.svg';

export default function Home() {
    return (
      <div className="right-content">
        <div id="layout-tabs">
          <ul>
            <li>
              🤣🤣Main Dining
            </li>
            <li>
              🤣🤣Outdoor
            </li>
          </ul>
        </div>
        <div id="layout">
          <div id="layout-legend"></div>
          <div id="layout-content"></div>
        </div>
      </div>
    );
  };