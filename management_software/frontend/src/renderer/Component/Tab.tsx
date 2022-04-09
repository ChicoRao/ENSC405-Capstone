import React, { useState } from 'react';
import closeLogo from '../../../assets/icons/close.png';
import '../css/Tabs.css';

//Used to specify the prop type
interface Tab {
	name: string,
	index: number,
	isActive: boolean,
	isEdit: boolean,
	onClickSelect: (i: number) => void
	onClickRemove: (i: number) => void
}

const Tab = ({ name, index, isActive, isEdit, onClickSelect, onClickRemove }: Tab): JSX.Element => {

	//Dynamically create single tab
	return (
		<li
			value={index}
			className={isActive === true ? "active-tab" : ""}
			onClick={() => onClickSelect(index)}
		>
			<span>
			<img 
					className={isEdit === false ? "read-tab" : "edit-tab"} 
					src={closeLogo}
					onClick={(e) => {
						console.log(e);
						onClickRemove(index);
					}}
			/>
			</span>
			{name}
	</li>
	);
};

export default Tab;