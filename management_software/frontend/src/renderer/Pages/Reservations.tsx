import React from 'react';
import '../css/Reservations.css';
import {CalendarComponent} from '@syncfusion/ej2-react-calendars';

function App() {
  const dateValue: Date = new Date(new Date().getFullYear(), new Date().getMonth(), 20);
  const minDate: Date = new Date(new Date().getFullYear(), new Date().getMonth(), 6);
  const maxDate: Date = new Date(new Date().getFullYear(), new Date().getMonth(), 25);
  return (
  <div>
    <div id="layout-test">
      <CalendarComponent value={dateValue} 
      min={minDate} 
      max={maxDate}
      //isMultiSelection={true}
      // start="Decade"
      // depth="Year">
      ></CalendarComponent>
    </div>
  </div>
  );
}

export default App;