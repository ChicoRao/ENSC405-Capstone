import React, { FC, useState } from 'react';
import closeLogo from '../../../assets/icons/close.png';
import '../css/Tabs.css';

//Hardcoded array of tabs for now
//Will make it update dynamically later
let tabs: string[] = ["Main Dining", "Outdoor"];

//Used to specify the prop type
interface Tabs {
	isEdit: boolean;
}

const Tabs: FC<Tabs> = (props): JSX.Element => {
	const [activeTab, setActiveTab] = useState(tabs[0]);

	const handleTabs = (index: number) => {
			setActiveTab(tabs[index]);
	};

	//When we dynamically create tabs
	//Will move className check & onClick to create dynamically too
	//Close/Remove button will dynamically alter tabs array
	return (
		<ul id="layout-tabs">
			<li
				value={tabs[0]}
				className={activeTab === tabs[0] ? "active-tab" : ""}
				onClick={() => handleTabs(0)}
			>
				<span>
				<img className={props.isEdit === false ? "read-tab" : "edit-tab"} src={closeLogo} />
				</span>
				Main Dining
			</li>
			<li
				value={tabs[1]}
				className={activeTab === tabs[1] ? "active-tab" : ""}
				onClick={() => handleTabs(1)}
			>
				<span>
					<img className={props.isEdit === false ? "read-tab" : "edit-tab"} src={closeLogo} />
				</span>
				Outdoor
			</li>
			<li className={props.isEdit === false ? "read-tab" : ""}>
				Add layout
			</li>
		</ul>
	);
};

export default Tabs;