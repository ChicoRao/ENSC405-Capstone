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
        const NewAction = ['Table ' + Object.keys(this.props.tableAction) + " " +  Object.values(this.props.tableAction)]
        if (this.props.tableAction !== prevProps.tableAction){
            if (!this.state.list.includes(NewAction[0])){
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