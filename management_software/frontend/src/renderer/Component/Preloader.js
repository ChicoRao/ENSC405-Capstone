import React, { useEffect, useState } from "react";
import ReactLoading from "react-loading";

function PreLoader1() {
  const [data, setData] = useState([]);
  const [done, setDone] = useState(undefined);



  return (
    <>
      {!done ? (
        <div style={{position: "fixed", top: "40%", left:"45%"}}>
            <ReactLoading
            type={"spinningBubbles"}
            color={"#2F2F2F"}
            height={100}
            width={100}
            />
        </div>
      ) : (
        <ul>
          {data.map((post) => (
            <li key={post.id}>{post.title}</li>
          ))}
        </ul>
      )}
    </>
  );
}

export default PreLoader1;