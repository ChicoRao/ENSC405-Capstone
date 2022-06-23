import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Tabs from '../Component/Tabs';
import Layout from '../Component/Layout';
import '../css/Home.css';
import tableLogo from '../../../assets/icons/editor/table.svg';
import chairLogo from '../../../assets/icons/editor/chair.svg';
import cashierLogo from '../../../assets/icons/editor/cashier.png';
import tableLogo1 from '../../../assets/icons/editor/Table1.svg';
import boothTableLogo from '../../../assets/icons/editor/booth_table.png';
import dividerLogo from '../../../assets/icons/editor/divider.png';
import doorLogo from '../../../assets/icons/editor/door.png';

interface LayoutDataCell {
  id: string,
  type: string,
  icon: string,
  top: string,
  left: string
}

const symbolsList = [
  {
    name: "Table",
    icon: tableLogo1
  },
  {
    name: "Chair",
    icon: chairLogo
  },
  {
    name: "Booth Table",
    icon: boothTableLogo
  },
  {
    name: "Divider",
    icon: dividerLogo
  },
  {
    name: "Cashier",
    icon: cashierLogo
  },
  {
    name: "Door",
    icon: doorLogo
  }
]

interface Home {
  update: () => void
  layoutInfo: string
}

//Layout tabs will soon be replaced with dynamic version
export default function Home({ update, layoutInfo }: Home) {
  const urlLayout = "http://127.0.0.1:5000/GetLayout";

  const [GetLayout, setLayout] = useState()
  function UpdateLayout() {

    axios.get(urlLayout)
    .then(data => {
      setLayout(data.data)
      console.log(data.data)
    })
    .catch(err => console.log(err));
    console.log(GetLayout)
  }


  return (
    <div className="right-content">
      <Tabs isEdit={false} />
      <div id="layout">
        <div id="layout-legend-content">
          <button id="triggerr" onClick={UpdateLayout}>
            Update Layout
          </button>
          <button 
            id="trigger" 
            onClick={update}>
            Update
          </button>
          {/* <div id="layout-legend">
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
          </div> */}
          <div className="layout-editor-content">
          {(GetLayout) && GetLayout.map((data: LayoutDataCell) => {
            console.log(data.type)

            return (
                <div
                  style={{position: 'absolute', top: data.top, left: data.left}}
                  id={data.id}
                >
                  <div 
                    className = "logo"
                  >
                    <img
                      src={data.icon}
                      className="editor-item cursor rotate-north"
                      draggable="false"
                      />
                  </div>
                </div>
            )
            
          })}
        </div>
        </div>
        <div id="layout-content">
          <Layout colour={layoutInfo} />
        </div>
      </div>
    </div>
  );
};