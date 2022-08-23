import { table } from "console";
import { Action } from "history";
import React, { Component } from "react";
import React, { useState, useEffect } from 'react';
import '../css/ActionList.css';


export default class ActionList extends Component{
    constructor(props){
        super(props)
        this.state = {
            list:[],
            tableAction: this.props.tableAction,
            itemList: [],
        }
    }
    componentDidUpdate(prevProps){
        console.log(Object.keys(this.props.tableAction)[0])
        const tableNumber = ['Table' + Object.keys(this.props.tableAction)]
        const NewAction = ['Table ' + Object.keys(this.props.tableAction) + " " +  Object.values(this.props.tableAction)]
        console.log(NewAction)
        if (this.props.tableAction !== prevProps.tableAction){
            if (this.state.list.includes(NewAction[0])){
                console.log("already here")
            }
            // else if(this.state.list.includes(tableNumber[0])){
            //     console.log("Table already request service")

            // }
            else{
                this.setState(previousState => ({
                    list:[...previousState.list, NewAction[0]]
                }))
            }
   
        }
    }
    deleteItem(item){
        this.setState(prevState => ({
            list: prevState.list.filter(ListItems => ListItems != item)
        }))
    }
    render(){
        const listItems = this.state.list.map((ListItem) => <li className="ListItem">{ListItem} <button className="dismissbutton" onClick={this.deleteItem.bind(this, ListItem)}>x</button></li>);
        return(
            <ul>
                {listItems}
            </ul>
                
        )
    }
}