import './index.css';
import {ParkedData} from "./ParkedDetails/ParkedData.js"
import {ParkingAreaData} from "./ParkingArea/ParkingAreaData.js"

function App() {
  return (
    <>
      <nav className="py-0 px-14 m-0 text-2xl text-white font-leagueSpartan bg-blue-400" >
        <div className="w-20 h-20 my-auto mx-auto">
          <img src="mainlogo.png"></img>
        </div>
      </nav>
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
