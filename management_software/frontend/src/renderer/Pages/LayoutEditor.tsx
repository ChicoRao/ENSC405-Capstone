import React, { useState, useEffect } from 'react';
import ReactDOM from 'react-dom';
import Draggable from 'react-draggable';
import axios from 'axios';
import Tabs from '../Component/Tabs';
import tableLogo from '../../../assets/icons/editor/table.svg';
//import chairLogo from '../../../assets/icons/editor/chair.svg';
import cashierLogo from '../../../assets/icons/editor/cashier.png';
import tableLogo1 from '../../../assets/icons/editor/Table1.svg';
import boothTableLogo from '../../../assets/icons/editor/booth_table.png';
import circular_table from '../../../assets/icons/editor/Circular_table.svg';

import dividerLogo from '../../../assets/icons/editor/divider.png';
import doorLogo from '../../../assets/icons/editor/door.png';
import '../css/LayoutEditor.css';
import { isNumberObject } from 'util/types';

/*
-Tabs re-use
  -Two modes: edit vs read-only
-Connect Device to corresponding table

-Should have a max of 50 items in one layout editor at once
  -Assign custom unique id to each of them
*/

/*
  Layout Storing Method Example (excluding specifying which selected layout is it):

  2 chairs and 1 table:
  layoutData = [
    {
      type: "chair",
      icon: chairLogo,
      x-pos: 100,
      y-pos: 100
    },
    {
      type: "chair",
      icon: chairLogo,
      x-pos: 300,
      y-pos: 100
    },
    {
      type: "table",
      icon: tableLogo,
      x-pos: 200,
      y-pos: 100
    }
  ]
*/

//-Rotate right now causes misalginment in items

interface LayoutDataCell {
  id: string,
  type: string,
  icon: string,
  top: number,
  left: number,
  rotation: string,
}

const symbolsList = [
  {
    name: "Table",
    icon: tableLogo1
  },
  {
    name: "circular_table",
    icon: circular_table
  },
]

export default function LayoutEditor() {
  let [layoutData, updateLayout] = useState<LayoutDataCell[]>([])
  let [tempData, updateTempData] = useState<LayoutDataCell[]>([])
  const urlLayout = "http://127.0.0.1:5000/GetLayout";

  useEffect(() => {
    axios.get(urlLayout)
    .then(data => {
      if (data.data.length)
        updateLayout(data.data)
        updateTempData(JSON.parse(JSON.stringify((data.data))))
    })
    .catch(err => console.log(err));
  }, []);

  // Function that creates the symbol and includes it in the layout data
  let createSymbolData = (name: string, icon: string) => {
    let dataList: LayoutDataCell[] = [];

    console.log(layoutData);
    console.log(layoutData.length);

    let data: LayoutDataCell = {
      id: 'e' + (isNaN(layoutData.length) ? '0' : layoutData.length.toString()),
      type: name,
      icon: icon,
      top: 0,
      left: 0,
      rotation: 'rotate-north'
    }

    //To-do: id naming should be improved

    if (layoutData.length <= 100) {
      dataList = [...layoutData, data];
      updateLayout(dataList);
      updateTempData(JSON.parse(JSON.stringify((dataList))));
    }
  }

  let rotateFunction = (id: string,e:any) => {
    let idTag = '#' + id;
    let el = document.querySelector(idTag + ' img');
    if (el) {
      if (e.detail == 1) {
        let rotation = '';
        if (el.classList.contains('rotate-north')) {
          el.classList.remove('rotate-north');
          el.classList.add('rotate-west');
          rotation = 'rotate-west';
        }else if (el.classList.contains('rotate-west')) {
          el.classList.remove('rotate-west');
          el.classList.add('rotate-south');
          rotation = 'rotate-south';
        }else if (el.classList.contains('rotate-south')) {
          el.classList.remove('rotate-south');
          el.classList.add('rotate-east');
          rotation = 'rotate-east';
        }else if (el.classList.contains('rotate-east')) {
          el.classList.remove('rotate-east');
          el.classList.add('rotate-north');
          rotation = 'rotate-north';
        }
        layoutData.forEach(each => {
          if (each.id === id) {
            each.rotation = rotation;
          }
        })
        updateTempData(layoutData);
        // updateLayout(layoutData);
      } else {
        el.remove();
        updateLayout(current => current.filter(rm => {
          return rm.id !== id;
        }));
        updateTempData(current => current.filter(rm => {
          return rm.id !== id;
        }));
      }
    }
  }


  function handleStop(e, data){
    let index:number = layoutData.findIndex(a => a.id === data.node.id)
    console.log("Dragged Left " + data.x)
    console.log("Dragged Top " + data.y)
    layoutData[index].left = tempData[index].left + data.x
    layoutData[index].top =  tempData[index].top + data.y
    console.log("Layout Data Left" + layoutData[index].left)
    console.log("Layout Data Right " + layoutData[index].top)
  }

  function SaveLayout(e, data){
    fetch('http://127.0.0.1:5000/SaveLayout', {
      method: 'POST',
      mode: 'cors',
      body: JSON.stringify(layoutData)
    })
  }

  return (
    <div className="layout-editor">
      <div className="editor-sidetools">
        <h3 className="sidetool-title">Symbols</h3>
        <div className="sidetool-grid">
          {symbolsList.map((obj, index) => {
            return (
              <div key={index}
                onClick={() => createSymbolData(obj.name, obj.icon,)}
              >
                <img
                  src={obj.icon}
                />
                <h5>
                  {obj.name}
                </h5>
              </div>
            )
          })}
        </div>
      </div>
      <div className="right-content layout-editor-right">
        <Tabs isEdit={true} />
        <div className="layout-editor-content">
          {Array.isArray(layoutData) && layoutData.map((data: LayoutDataCell) => {
            // console.log(data.type)

            return (
              <Draggable key={data.id}
                grid={[25,25]}
                bounds="parent"
                onStop={handleStop}
              >
                
                <div
                  style={{position: 'absolute', top: data.top + 'px', left: data.left + 'px'}}
                  id={data.id}
                >
                  <div 
                    className="rotate-icon no-cursor"
                    onClick={(e) => rotateFunction(data.id,e)}
                    // onMouseUp={()=> console.log()}
                    // onMouseUp={()=> console.log(layoutData)}
                  >
                    <h6 className="rotateDelete">Rotate/Delete</h6>
                  </div>
                  <div 
                    className = "logo"
                  >
                    <h4 className = "TableNumber">Table {data.id}</h4>
                    <img
                      
                      src={data.icon}
                      className={"editor-item cursor " + data.rotation}
                      draggable="false"
                      />
                      
                  </div>
                </div>
              </Draggable>
            )
            
          })}
        </div>
        <div class="space"></div>
        <button onClick={SaveLayout} class="button">Save Layout </button>
      </div>
    </div>
  );
};