import React from 'react';
import React, { useState, useEffect } from 'react';
import '../css/PopUp.css';
import { Button } from 'antd';

// const [action, setAction] = useState(true);
// const [tableID, setTableID] = useState(true);



// export default function PopUp({resetActions, tableAction}: PopUp) {
//     console.log("props ", Object.keys(tableAction))
//     console.log("props value ", Object.values(tableAction))

//     return (
//         <div className="PopupWindow">
//             <div >
//                 <h2>Table {Object.keys(tableAction)[0]} {Object.values(tableAction)[0]}</h2>
//             </div>
//             {/* button controls */}
//             <div>
//                 <Button type="primary" onClick={resetActions}> Dismiss </Button>
//             </div> 
//         </div>
//     );
// }

// export default function PopUp({tableId, content, buttonAction, buttonText, handleClose}: PopUp) {
//     console.log("tableId: ", tableId)

//     return (
//         <div className="PopupWindow">
//             <div >
//                 <h2>Table {tableId} {content}</h2>
//             </div>
//             {/* button controls */}
//             <div>
//                 <Button type="primary" onClick={buttonAction}> {buttonText} </Button>
//                 <Button type="primary" onClick={handleClose}> Close </Button>
//             </div> 
//         </div>
//     );
// }

//If want to generalize popup, then can change it
export default function PopUp({tableId, buttonAction, handleClose}: PopUp) {
    console.log("tableId: ", tableId)

    return (
        <div className="PopupWindow">
            <div >
                <h2>Are you sure you want to recalibrate Table {tableId}</h2>
            </div>
            {/* button controls */}
            <div>
                <Button style={{margin: "10px"}} type="primary" onClick={buttonAction}> Yes </Button>
                <Button style={{margin: "10px"}} type="primary" onClick={handleClose}> Cancel </Button>
            </div> 
        </div>
    );
}