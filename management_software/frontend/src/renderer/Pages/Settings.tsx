import React from 'react';
import { Button } from 'antd';
import '../css/Settings.css';

export default function Settings() {

    function save(){
        document.getElementById('wifiName').value = "";
        document.getElementById('wifiPassword').value = "";
    }

	return(
        // <div className='WifiInput'>
        //     <div>
        //         <form>
        //             <label>
        //                 Wifi Name:
        //                 <input id="wifiName" type="text" name="WifiName" />
        //             </label>
        //         </form>
        //     </div>
        //     <div>
        //         <form>
        //             <label>
        //                 Password:
        //                 <input id="wifiPassword" type="text" name="Password" />
        //             </label>
        //         </form>
        //     </div>
        //     <div className="saveWifiButtonDiv">
        //         <button className="saveWifiButton" onClick={save}> Save </button>
        //     </div>
            <div className="updatebutton">
                <Button type="primary"> Update </Button>
            </div>
        // </div>
    );
};