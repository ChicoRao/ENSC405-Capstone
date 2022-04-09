import React, { useState } from 'react';
import Tab from './Tab';
import '../css/Tabs.css';

//Hardcoded array of tabs for now
//Will make it update dynamically later
let tabs: string[] = ["Main Dining", "Outdoor"];

//Used to specify the prop type
interface Tabs {
	isEdit: boolean;
}

const Tabs = ({ isEdit }: Tabs): JSX.Element => {
	const [tabsList, updateTabsList] = useState(tabs);
	const [activeTab, setActiveTab] = useState(tabsList[0]);

	const handleTabs = (index: number) => {
		if (index < tabsList.length)
			setActiveTab(tabsList[index]);
	};

	const removeTabs = (index: number) => {
		let tempList = tabsList;
		updateTabsList(tabsList.filter(tab => tab !== tempList[index]))
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
						isActive={tabsList[index] === activeTab} 
						isEdit={isEdit} 
						onClickSelect={handleTabs} 
						onClickRemove={removeTabs} />
				);
			})}
		</ul>
	);
};

export default Tabs;