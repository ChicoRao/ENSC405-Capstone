import React from 'react';
import React, { useState, useEffect } from 'react';


// const [action, setAction] = useState(true);
// const [tableID, setTableID] = useState(true);



export default function PopUp({resetActions, tableAction}: PopUp) {
    console.log("props ", Object.keys(tableAction))
    console.log("props value ", Object.values(tableAction))

    return (
        <div >
            {/* x close window */}
            <button onClick={resetActions} >X</button>
            <div >
                <h1>Table {Object.keys(tableAction)[0]} requesting for {Object.values(tableAction)[0]}</h1>
            </div>
            {/* button controls */}
            <div>
                <button onClick={()=> setAttention(false)}> MORE BONES! </button>
                <button onClick={()=> setAttention(false)}> No, thank you. </button>
            </div> 
        </div>
    );
}