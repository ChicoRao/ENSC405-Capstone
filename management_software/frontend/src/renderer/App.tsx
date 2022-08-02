import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Sidebar from './Sidebar';
import Navbar from './Navbar';
import Home from './Pages/Home';
import Menu from './Pages/Menu';
import Reservations from './Pages/Reservations';
import LayoutEditor from './Pages/LayoutEditor';
import Settings from './Pages/Settings';
import './css/App.css';

export default function App() {
	let socket = io("http://localhost:5000/", { transports: ["websocket"] });;
	const [socketConnected, setSocketConnected] = useState(false);
    const initialObject = {'e0': 'green', 'e1': 'green'}
    const [tableInfo, updateTable] = useState(initialObject)
    const [attention, setAttention] = useState(false);
    const [tableAction, updateAction] = useState(new Map())

	useEffect(() => {

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

	socket.on("update value", (msg: string) => {
        console.log(msg)
        updateTable(msg)
	})

    socket.on("Action", (handGestures: string) => {
        console.log(handGestures)
        setAttention(true);
        updateAction(handGestures)
	})

    // An event handler for a change of value 
    const update = () => {
        console.log("Starting Stream")
        socket.emit('start stream', {
            data: "Please update"
        });
    }

    const resetActions = () => {
        console.log("Resetting Actions")
        setAttention(false);
        updateAction(new Map());
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

  return (
    <Router>
			<div id="app">
				{/* <Sidebar /> */}
                <Navbar />
				<Routes>
					<Route path="/" element={<Home update={update} tableInfo={tableInfo} tableAction={tableAction} attention={attention} resetActions={resetActions}/>} />
					<Route path="/menu" element={<Menu />} />
					<Route path="/reservations" element={<Reservations />} />
					<Route path="/layouteditor" element={<LayoutEditor />} />
                    <Route path="/settings" element={<Settings />} />
				</Routes>
			</div>
    </Router>
  );
}
