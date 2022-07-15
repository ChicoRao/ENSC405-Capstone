import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Sidebar from './Sidebar';
import Home from './Pages/Home';
import Menu from './Pages/Menu';
import Reservations from './Pages/Reservations';
import LayoutEditor from './Pages/LayoutEditor';
import Settings from './Pages/Settings';
import './css/App.css';
import ReactLoading from "react-loading";
import LoadingScreen from './Component/Preloader'

export default function App() {
	let socket = io('http://localhost:5000');
	const [socketConnected, setSocketConnected] = useState(false);
	const [layoutInfo, updateLayoutInfo] = useState("white");
    const [tableInfo, updateTableID] = useState('e')
    const [loading, setLoading] = useState(true)
	useEffect(() => {
        setTimeout(() => setLoading(false), 3000)
        if (!socketConnected) {
            socket.on("connect", () => {
                console.log(socket.id);
            });
            socket.on("after connect", (msg: Object) => {
                console.log(msg);
                setSocketConnected(true);
            })
        }
        return () => {
            socket.off("after connect", () => {
                setSocketConnected(true);
            }) 
        }
    })

	socket.on("update value", (msg: Object) => {
		let colour = msg.colour;
        let tableID = msg.ID;
		updateLayoutInfo(colour);
        updateTableID(tableID);
		// console.log("COLOUR: ", layoutInfo);
        // console.log("TableID: ", tableInfo);
	})

    // An event handler for a change of value 
    const update = () => {
        console.log("Start Update...")
        socket.emit('Slider value changed', {
            data: "Please update"
        });
    }

    socket.on("connect_error", () => {
        socket.connect();
        setSocketConnected(true);
    })

    socket.on("disconnect", (reason) => {
        console.error("Disconnected due to: ", reason);
        setSocketConnected(false);
        if (reason === "io server disconnect") {
            socket.connect();
            socket.on("after connect", (msg: Object) => {
                console.log(msg);
                setSocketConnected(true);
            })
        }
    })
    const loader = () => {
        return (
          <ReactLoading
            type={"spokes"}
            color={"#5433ff"}
            height={"4%"}
            width={"4%"}
          />
        );
      };
  return (
    <>
    <Router>
            {loading === false ? (
                <div id="app">
                <Sidebar />
                <Routes>
                    <Route path="/" element={<Home update={update} layoutInfo={layoutInfo} tableInfo={tableInfo}/>} />
                    <Route path="/menu" element={<Menu />} />
                    <Route path="/reservations" element={<Reservations />} />
                    <Route path="/layouteditor" element={<LayoutEditor />} />
                    <Route path="/settings" element={<Settings />} />
                </Routes>
                </div>
            ): (
                <div className='Loading'>
                    <LoadingScreen/>
                </div>
                
            )
        }

    </Router>
    </>
    
  );
}
