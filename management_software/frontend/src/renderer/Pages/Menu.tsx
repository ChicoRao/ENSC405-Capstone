import React from 'react';
import icon from '../../../assets/icon.svg';

export default function Menu() {
  return (
    <div className="right-content">
      <div className="Hello">
          <img width="200px" alt="icon" src={icon} />
        </div>
        <div className="Hello">
          <a
            href="https://electron-react-boilerplate.js.org/"
            target="_blank"
            rel="noreferrer"
          >
            <button type="button">
              <span role="img" aria-label="haha">
                🤣🤣🤣🤣🤣
              </span>
                🤣
            </button>
          </a>
          <a
            href="https://github.com/sponsors/electron-react-boilerplate"
            target="_blank"
            rel="noreferrer"
          >
            <button type="button">
              <span role="img" aria-label="haha">
                🤣
              </span>
              Donate
            </button>
          </a>
        </div>
    </div>
  );
};