import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Tabs from '../Component/Tabs';
import Layout from '../Component/Layout';
import Popup from '../Component/Popup';
import PlaceHolder from '../Component/PlaceHolder';


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

let colourDeg = new Map<string, string>([
  ['red', '(0deg)'],
  ['yellow', '(0deg)'],
  ['blue', '(240deg)'],
  ['green', '(120deg)']
]);

interface Home {
  update: () => void
  tableInfo: Map<string,string>
  tableAction: Map<string,string>
  attention: Boolean
  resetActions: () => void
}

//Layout tabs will soon be replaced with dynamic version
export default function Home({ update, tableInfo, tableAction, attention, resetActions }: Home) {
  const urlLayout = "http://127.0.0.1:5000/GetLayout";
  // const recalibrateURL = "http://127.0.0.1:5000/capture";


  const [GetLayout, setLayout] = useState()
  const numbers = [1,2,3,4,5]
  const listItems = numbers.map((number) =>
  <li>Table {number} needs attention</li>
  );
  function UpdateLayout() {
    axios.get(urlLayout)
    .then(data => {
      setLayout(data.data)
    })
    .catch(err => console.log(err));
    console.log(GetLayout)
  }
  function recalibrate(){
    console.log("Recalibrating")
    axios.put("http://127.0.0.1:5000/capture")
    // fetch('http://127.0.0.1:5000/capture', {
    //   method: 'PUT',
    //   mode: 'cors',
      
    // })
  }

  return (
    <div style={{display: 'grid', gridTemplateColumns: "repeat(2,1fr)"}}>
    <div className="right-content">
    {/* <img src="/icon.jpg" alt="My_Logo"></img> */}
      <Tabs isEdit={false} />
      <div id="layout">
        <div id="layout-legend-content">
          <div id="layout-legend">
            <ul id="layout-legend-elements">
              <li>
                <span className="legend-colors">
                </span>
                Free
                <div>
                </div>
              </li>
              <li>
                <span className="legend-colors">
                </span>
                Occupied
                <div>
                </div>
              </li>
              <li>
                <span className="legend-colors">
                </span>
                Dirty
              </li>
            </ul>
          </div>
          <div>
            {attention ? <Popup resetActions={resetActions} tableAction={tableAction} /> : <PlaceHolder/> }
          </div>
          <div className = "center">
          <div className="layout-editor-content">
          {(GetLayout) && GetLayout.map((data: LayoutDataCell) => {
            console.log(attention)
            if(data.id in tableInfo){
              console.log(tableInfo[data.id])
              let tablecolour = colourDeg.get(tableInfo[data.id])
              const styleTable = {
                filter: 'invert(.5) sepia(1) saturate(100) hue-rotate'+ tablecolour
              }
              return (
                  <div
                  style={{position: 'absolute', top: data.top, left: data.left}}
                  id={data.id}

                >
                  <div 
                    className = "logo"
                  
                  >
                    <h4 className = "TableNumber">Table {data.id}</h4>
                    <img 
                      style = {styleTable}
                      src={data.icon}
                      className="editor-item cursor rotate-north"
                      draggable="false"
                      
                      />
                  </div>
                </div>
              )
            }
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
          <div class="space"></div>
          <button id="triggerr" onClick={UpdateLayout} class="button">
            Update Layout
          </button>
          <div class="space">
           </div>
          <button
            id="trigger" 
            onClick={update} class="button">
            Sync
          </button>
          <button
            id="trigger" 
            onClick={recalibrate} class="button">
            Recalibrate
          </button>
        </div>
        
        </div>
      </div>
    
    </div>
    <div className='left-content'>
      <div className='ActionList'>
            <ul className='List'>
            {/* <div>
              {attention ? <Popup resetActions={resetActions} tableAction={tableAction} /> : <PlaceHolder/> }
            </div> */}
            {listItems}
            </ul>
      </div>
    </div>
    </div>
  );
};