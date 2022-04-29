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

interface LayoutDataCell {
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
    let data: LayoutDataCell = {
      type: name,
      icon: icon,
      top: '115px',
      left: '565px'
    }
    let dataList: LayoutDataCell[] = [];

    console.log(layoutData);

    if (layoutData.length <= 100) {
      dataList = [...layoutData, data];
      updateLayout(dataList);
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
              >
                <div
                  style={{position: 'absolute', top: data.top, left: data.left}}
                >
                  <img
                    src={data.icon}
                    className="editor-item"
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