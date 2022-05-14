import React, { FC, useState, useEffect } from 'react';
import '../css/Layout.css';

interface Layout {
    colour: string
}

const Layout = ({ colour }: Layout) => {
    // const [tableColour, updateTableColour] = useState(colour ? colour : "white");

    // useEffect(() => {
    //     updateTableColour(colour)
    //     console.log("table-->", colour);
    //     console.log("table state -->", tableColour);    
    //   }, [ colour ])
 
    console.log("layout colour: ", colour)
    const style = {
        backgroundColor: colour ? colour : "white"
    }
    return (
        <div>
            <div className="table" style={style}></div>
        </div>
    )
}

export default Layout;