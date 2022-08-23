import React from 'react';
import React, { useState, useEffect } from 'react';
import '../css/PopUp.css';
import { Button } from 'antd';

// const [action, setAction] = useState(true);
// const [tableID, setTableID] = useState(true);



export default function PopUp({resetActions, tableAction}: PopUp) {
    console.log("props ", Object.keys(tableAction))
    console.log("props value ", Object.values(tableAction))

    return (
        <div className="PopupWindow">
            <div >
                <h2>Table {Object.keys(tableAction)[0]} {Object.values(tableAction)[0]}</h2>
            </div>
            {/* button controls */}
            <div>
                <Button type="primary" onClick={resetActions}> Dismiss </Button>
            </div> 
        </div>
    );
}