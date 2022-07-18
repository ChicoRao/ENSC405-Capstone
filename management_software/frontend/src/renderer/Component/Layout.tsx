import React, { FC, useState, useEffect } from 'react';
import '../css/Layout.css';

interface Layout {
    ID: string
    colour: string
}

const Layout = ({ID, colour }: Layout) => { 
    console.log("layout colour: ", colour)
    console.log("Table ID ", ID)
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