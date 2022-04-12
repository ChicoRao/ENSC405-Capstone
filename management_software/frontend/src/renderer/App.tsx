import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import Sidebar from './Sidebar';
import Home from './Pages/Home';
import Menu from './Pages/Menu';
import Reservations from './Pages/Reservations';
import LayoutEditor from './Pages/LayoutEditor';
// import Settings from './Pages/Settings';
import './css/App.css';

export default function App() {
	let socket = io('http://localhost:5000');
	const [layoutInfo, updateLayoutInfo] = useState("white");

	socket.on("connect", () => {
		console.log(socket.id);
	});

	socket.on("after connect", (msg: Object) => {
		console.log(msg);
	});

	socket.on("update value", (msg: Object) => {
		let colour = msg.colour;
		updateLayoutInfo(colour);
		console.log("COLOUR: ", layoutInfo);
		console.log("Layout type: ", typeof(layoutInfo));
	})

	// An event handler for a change of value 
	const update = () => {
		console.log("Start Update...")
		socket.emit('Slider value changed', {
			data: "Please update"
		});
	}

  return (
    <Router>
			<div id="app">
				<Sidebar />
				<Routes>
					<Route path="/" element={<Home update={update} layoutInfo={layoutInfo}/>} />
					<Route path="/menu" element={<Menu />} />
					<Route path="/reservations" element={<Reservations />} />
					<Route path="/layouteditor" element={<LayoutEditor />} />
				</Routes>
			</div>
    </Router>
  );
}
