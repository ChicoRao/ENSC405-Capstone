import React, { useState } from 'react';
import ReactDOM from 'react-dom';
import Draggable from 'react-draggable';
import Tabs from '../Component/Tabs';
import tableLogo from '../../../assets/icons/editor/table.png';
import chairLogo from '../../../assets/icons/editor/chair.png';
// import boothTableLogo from '../../../assets/icons/editor/booth_table.png';
// import dividerLogo from '../../../assets/icons/editor/divider.png';
import '../css/LayoutEditor.css';

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
  top: string,
  left: string
}

const symbolsList = [
  {
    name: "Table",
    icon: tableLogo
  },
  {
    name: "Chair",
    icon: chairLogo
  },
  {
    name: "Booth Table",
    icon: ""
  },
  {
    name: "Divider",
    icon: ""
  },
  {
    name: "Cashier",
    icon: ""
  },
  {
    name: "Door",
    icon: ""
  }
]

export default function LayoutEditor() {
  let [layoutData, updateLayout] = useState<LayoutDataCell[]>([])

  // Function that creates the symbol and includes it in the layout data
  let createSymbolData = (name: string, icon: string) => {
    let dataList: LayoutDataCell[] = [];

    console.log(layoutData);
    console.log(layoutData.length);

    let data: LayoutDataCell = {
      id: 'e' + layoutData.length.toString(),
      type: name,
      icon: icon,
      top: '115px',
      left: '565px'
    }

    //To-do: id naming should be improved

    if (layoutData.length <= 100) {
      dataList = [...layoutData, data];
      updateLayout(dataList);
    }
  }

  let rotateFunction = (id: string) => {
    let idTag = '#' + id;
    let el = document.querySelector(idTag + ' img');
    if (el) {
      if (el.classList.contains('rotate-north')) {
        el.classList.remove('rotate-north');
        el.classList.add('rotate-west');
      }else if (el.classList.contains('rotate-west')) {
        el.classList.remove('rotate-west');
        el.classList.add('rotate-south');
      }else if (el.classList.contains('rotate-south')) {
        el.classList.remove('rotate-south');
        el.classList.add('rotate-east');
      }else if (el.classList.contains('rotate-east')) {
        el.classList.remove('rotate-east');
        el.classList.add('rotate-north');
      }
    }
  }

  return (
    <div className="layout-editor">
      <div className="editor-sidetools">
        <h3 className="sidetool-title">Symbol</h3>
        <hr/>
        <div className="sidetool-grid">
          {symbolsList.map((obj) => {
            return (
              <div
                onClick={() => createSymbolData(obj.name, obj.icon)}
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
          {layoutData.map((data: LayoutDataCell) => {
            console.log(data.type)

            return (
              <Draggable
                grid={[25,25]}
                bounds="parent"
              >
                <div
                  style={{position: 'absolute', top: '0px', left: '0px'}}
                  id={data.id}
                >
                  <div 
                    className="rotate-icon no-cursor"
                    onClick={() => rotateFunction(data.id)}
                  >
                    <h6>Rotate</h6>
                  </div>
                  <img
                    src={data.icon}
                    className="editor-item cursor rotate-north"
                    draggable="false"
                    />
                </div>
              </Draggable>
            )
          })}
        </div>
      </div>
    </div>
  );
};