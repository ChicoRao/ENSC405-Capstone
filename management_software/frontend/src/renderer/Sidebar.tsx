import { ProSidebar, Menu, MenuItem, SidebarHeader, SidebarContent, SidebarFooter } from 'react-pro-sidebar';
import { Link } from 'react-router-dom';
import 'react-pro-sidebar/dist/css/styles.css';
import './css/Sidebar.css';

export default function Sidebar() {
  return (
    <ProSidebar id="sidebar">
      <SidebarHeader>
        <Menu>
          <MenuItem>
            LocalHost
            <Link to="/" />
          </MenuItem>
        </Menu>
      </SidebarHeader>
      <SidebarContent>
        <Menu>
          <MenuItem>
            🤣 Home
            <Link to="/" />
          </MenuItem>
          <MenuItem>
            🤣 Menu
            <Link to="/menu" />
          </MenuItem>
          <MenuItem>
            🤣 Reservations
            <Link to="/reservations" />
          </MenuItem>
          <MenuItem>
            🤣 Layout Editor
            <Link to="/layouteditor" />
          </MenuItem>
        </Menu>
      </SidebarContent>
      <SidebarFooter>
        <Menu>
          <MenuItem>
            ⚙️ Settings
            <Link to="/settings" />
          </MenuItem>
        </Menu>
      </SidebarFooter>
    </ProSidebar>
  );
}

