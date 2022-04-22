import React, { Component } from 'react';
import '../css/Menu.css';
//import * as fs from 'fs';
//import '../../../assets/defaultImage.png';

export class Menu extends Component {
  state={
    menuImg:''
  }
  imageHandler = (e: { target: { files: File[]; }; }) => {
    const reader = new FileReader();
    reader.onload = () =>{
      if(reader.readyState === 2){
        this.setState({menuImg: reader.result})
      }
    }
    reader.readAsDataURL(e.target.files[0])

    // write the file path into file
    // var fs = require('fs');
    // fs.writeFile('Output.txt', e.target.files[0].path, () => {});
  };
	render() {
    const {menuImg} = this.state
		return (
			<div className="page">
				<div className="container">
					<h1 className="heading">Add menu</h1>
					<div className="img-holder">
						<img src={menuImg} alt="" id="img" className="img" />
					</div>
					<input type="file" accept="image/*" name="image-upload" id="input" onChange={this.imageHandler} />
					<div className="label">
          <label className="image-upload" htmlFor="input">
						<i className="material-icons">Select an image</i>
					</label>
          </div>
				</div>
			</div>
		);
	}
}

export default Menu;