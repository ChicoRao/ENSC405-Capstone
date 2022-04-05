import { MemoryRouter as Router, Routes, Route } from 'react-router-dom';
import Sidebar from './Sidebar';
import Home from './Pages/Home';
import Menu from './Pages/Menu';
import Reservations from './Pages/Reservations';
import LayoutEditor from './Pages/LayoutEditor';
// import Settings from './Pages/Settings';
import './css/App.css';

export default function App() {
  return (
    <Router>
			<div id="app">
				<Sidebar />
				<Routes>
					<Route path="/" element={<Home />} />
					<Route path="/menu" element={<Menu />} />
					<Route path="/reservations" element={<Reservations />} />
					<Route path="/layouteditor" element={<LayoutEditor />} />
				</Routes>
			</div>
    </Router>
  );
}
