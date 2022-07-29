import React from 'react';
import '../css/Reservations.css';
import {CalendarComponent} from '@syncfusion/ej2-react-calendars';

function App() {
  const dateValue: Date = new Date(new Date().getFullYear(), new Date().getMonth(), 20);
  const minDate: Date = new Date(new Date().getFullYear(), new Date().getMonth(), 6);
  const maxDate: Date = new Date(new Date().getFullYear(), new Date().getMonth(), 25);
  return (
  <div>
    //To check calendar views paste start="Decade" and depth="Year" in below code. Also remove range restriction i.e. min and max properties
    <CalendarComponent value={dateValue} 
    min={minDate} 
    max={maxDate}
    isMultiSelection={true}
    start="Decade"
    depth="Year"></CalendarComponent>
  </div>
  );
}

export default App;