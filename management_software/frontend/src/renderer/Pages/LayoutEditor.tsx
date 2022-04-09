import React from 'react';
import Tabs from '../Component/Tabs';

/*
-Tabs re-use
  -Two modes: edit vs read-only
-Connect Device to corresponding table
*/

export default function LayoutEditor() {
  return (
    <div className="right-content">
      <Tabs isEdit={true} />
    </div>
  );
};