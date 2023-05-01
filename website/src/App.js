import './index.css';

function App() {
  return (
    <>
      <nav className="py-7 px-14 m-0 text-2xl text-white font-leagueSpartan bg-blue-400" >Parking Website</nav>
      <div className="p-14 grid grid-rows-2 grid-flow-col gap-6">
        <div className="bg-red-400 px-auto grid grid-rows-5 ">Parked Vehicles Data
          <div className="flex flex-row flex-wrap">
            <div className="px-auto">S.No</div>
            <div className="px-auto">Car Plate Number</div>
            <div className="px-auto">Time In</div>
          </div>        
          <div>1</div>        
          <div>2</div>        
          <div>3</div>
          <div>4</div>
        </div>
        <div className="bg-red-400 px-auto h-48">Parked Vehicles</div>
        <div className="row-span-2 bg-red-400 px-auto">Scan Me QR</div>
      </div>
    </>
  );
}

export default App;
