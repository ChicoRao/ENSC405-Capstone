import React, { FC, useState, useEffect } from 'react';
import '../css/Layout.css';

interface Layout {
    colour: string
}

const Layout = ({ colour }: Layout) => { 
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