import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import React from 'react';
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

	socket.on("connect", () => {
		console.log(socket.id);
	});

	socket.on("after connect", (msg: Object) => {
		console.log(msg);
	});

	socket.on("update button pressed", (msg: string) => {
		console.log(msg);
	})

	const initiateUpdate = () => {
		socket.emit('Slider value changed', {
			data: "Please update"
		});
	}

	// An event handler for a change of value 
	const update = () => {
		setInterval(initiateUpdate, 2000);
	}

  return (
    <Router>
			<div id="app">
				<Sidebar />
				<Routes>
					<Route path="/" element={<Home update={update}/>} />
					<Route path="/menu" element={<Menu />} />
					<Route path="/reservations" element={<Reservations />} />
					<Route path="/layouteditor" element={<LayoutEditor />} />
				</Routes>
			</div>
    </Router>
  );
}
