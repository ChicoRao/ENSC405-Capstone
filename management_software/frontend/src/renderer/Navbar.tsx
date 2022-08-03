import {
    BookOutlined,
    CoffeeOutlined,
    FormOutlined,
    MenuOutlined,
    HomeOutlined,
    SettingOutlined,
  } from '@ant-design/icons';
  import type { MenuProps } from 'antd';
  import { Link } from 'react-router-dom';
  import { Button, Menu } from 'antd';
  import React, { useState } from 'react';
  import './css/Navbar.css';
  
  type MenuItem = Required<MenuProps>['items'][number];
  
  function getItem( label: React.ReactNode, key: React.Key, icon: React.ReactNode) {
    return {
      key,
      icon,
      label,
    } as MenuItem;
  }
  
  const items: MenuItem[] = [
    getItem(<Link to="/">Home</Link>, '1', <HomeOutlined />),
    getItem(<Link to="/menu">Menu</Link>, '2', <CoffeeOutlined />),
    getItem(<Link to="/reservations">Reservations</Link>, '3', <BookOutlined />),
    getItem(<Link to="/layouteditor">Layout Editor</Link>, '4', <FormOutlined />),
    getItem("" , '5', null),
    getItem("" , '6', null),
    getItem("" , '7', null),
    getItem("" , '8', null),
    getItem("" , '9', null),
    getItem("" , '10', null),
    getItem("" , '11', null),
    getItem("" , '12', null),
    getItem("" , '13', null),
    getItem("" , '14', null),
    // getItem("" , '15', null),
    // getItem("" , '16', null),
    // getItem("" , '17', null),
    // getItem("" , '18', null),
    getItem(<Link to="/Settings">Settings</Link> , '20', <SettingOutlined />),
  ];
  
  export default function Navbar() {
    const [collapsed, setCollapsed] = useState(false);
  
    const toggleCollapsed = () => {
      setCollapsed(!collapsed);
    };

    return (
        <div className="navbar">
          <Button type="primary" onClick={toggleCollapsed} style={{ marginBottom: 16 }}>
            {collapsed ? <MenuOutlined /> : <MenuOutlined />}
          </Button>
          <Menu
            defaultSelectedKeys={['1']}
            mode="inline"
            theme="dark"
            inlineCollapsed={collapsed}
            items={items}
          />
        </div>
      );
  }