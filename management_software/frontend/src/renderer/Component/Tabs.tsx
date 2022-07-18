import React, { useState, useEffect } from 'react';
import Tab from './Tab';
import '../css/Tabs.css';

//Hardcoded array of tabs for now
//Will make it update dynamically later
let tabs: string[] = ["Main Dining", "Outdoor", "Roof"];

//Will need to send as prop the current tabs list

//Used to specify the prop type
interface Tabs {
	isEdit: boolean;
}

const Tabs = ({ isEdit }: Tabs): JSX.Element => {
	// const [tabsList, updateTabsList] = useState(tabs);
	const [tabsList, setTabsList] = useState(tabs);
	const [activeTab, setActiveTab] = useState(0);

	const handleTabs = (name: string, index: number) => {
		if (index < tabsList.length)
			if (tabsList.includes(name)) {
				setActiveTab(index);
			}
			else {
				setActiveTab(0);
			}
	};

	const removeTabs = (index: number) => {
		if (index === 0) {
			console.log("Cannot remove Main Dining");
			return;
		}
		if (index === activeTab) {
			setActiveTab(0);	//Set active tab back to Main Dining if removed tab is active
		}
		let tempList = tabsList.filter(tab => tab !== tabsList[index]);
		setTabsList(tempList);
		tabs = tempList;
	};

	//Dynamically creating all tabs
	//Need to somehow store the list though
	//To prevent deleted tab from reappearing
	return (
		<ul id="layout-tabs">
			{tabsList.map((tab, index) => {
				return (
					<Tab 
						name={tab} 
						index={index} 
						isActive={index === activeTab} 
						isEdit={isEdit} 
						onClickSelect={handleTabs} 
						onClickRemove={removeTabs} />
				);
			})}
		</ul>
	);
};

export default Tabs;