import './index.css';
import {ParkedData} from "./ParkedDetails/ParkedData.js"
import {ParkingAreaData} from "./ParkingArea/ParkingAreaData.js"

function App() {
  return (
    <>
      <nav className="py-7 px-14 m-0 text-2xl text-white font-leagueSpartan bg-blue-400" >Parking Website</nav>
      <div className="p-14 grid grid-rows-2 grid-flow-col gap-12">
        {/* <div className="bg-red-400 px-auto h-48">Hi</div> */}
        <div><ParkedData/></div>
        <ParkingAreaData />
        <div className="row-span-2  bg-red-400 px-auto">Scan Me QR</div>
      </div>
    </>
  );
}

export default App;
