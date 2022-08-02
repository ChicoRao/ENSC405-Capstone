import React from 'react';

const PopUp = props => {
    // function that takes boolean as param to conditionally display popup
    const { setAttention,  tableActions } = props 
    console.log(props)
    return (
        <div >
            {/* x close window */}
            <button onClick={()=> setAttention(false)} >X</button>
            <div >
                <h1>Hehehahahoho</h1>
            </div>
            {/* button controls */}
            <div>
                <button onClick={()=> setAttention(false)}> MORE BONES! </button>
                <button onClick={()=> setAttention(false)}> No, thank you. </button>
            </div>
        </div>
    );
}

export default PopUp;