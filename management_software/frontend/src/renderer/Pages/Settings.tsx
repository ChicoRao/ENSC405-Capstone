import React from 'react';
import '../css/Settings.css';

export default function Settings() {

    function save(){
        const name = document.getElementById('wifiName').value;
        const password = document.getElementById('wifiPassword').value;
        fetch('http://127.0.0.1:5000/SavePassword', {
            method: 'POST',
            mode: 'cors',
            body: JSON.stringify(JSON.parse('{"username": "'+ name + '", "password": "' + password + '"}'))
        })
    }

	return(
        <div className='WifiInput'>
            <div>
                <form>
                    <label>
                        Wifi Name:
                        <input id="wifiName" type="text" name="WifiName" />
                    </label>
                </form>
            </div>
            <div>
                <form>
                    <label>
                        Password:
                        <input id="wifiPassword" type="text" name="Password" />
                    </label>
                </form>
            </div>
            <div className="saveWifiButtonDiv">
                <button className="saveWifiButton" onClick={save}> Save </button>
            </div>
        </div>
    );
};