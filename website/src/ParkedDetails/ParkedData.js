import React, { useEffect, useState } from 'react'
import {Car} from './cardetails.js'
export const ParkedData = ()=>{

    const [products, setProducts]=useState("");
    useEffect(()=>{
        const interval = setInterval(()=>{
          const fetchData = async ()=>{
            const res= await fetch("http://localhost:5000/users");
            const data =await res.json();
            setProducts(data);
          }
          fetchData();
        },1000);
        return ()=>clearInterval(interval); 
    }, []);
      if(products.length>0) 
      return (
      <div className={`box-content border-solid border-black px-auto grid grid-rows-${products.length+1}`}>
        <div className="flex flex-row flex-wrap h-12 text-center"> 
          <div className="w-1/6 border-black py-2 border-2">Slot No</div>
          <div className="w-1/3 border-black py-2 border-y-2">Plate Number</div>
          <div className="w-1/2 border-black py-2 border-2">Time In</div> 
        </div>
        {
          products.map(eachProduct=>{
            return <Car slot={eachProduct.slot} plate={eachProduct.plate} timeIn={eachProduct.in_time}/>
          })
        }        
      </div>
  )
};

