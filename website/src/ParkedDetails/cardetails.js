import React from 'react'

export const Car = (props)=>{
  return (
    <div className="flex flex-row flex-wrap h-12 leading-3"> 
        <div className="w-1/6 text-center  border-black border-2 border-t-0">{props.slot}</div>
        <div className="w-1/3 text-center  border-black border-b-2">{props.plate}</div>
        <div className="w-1/2 text-center  border-black border-2 border-t-0">{props.timeIn}</div>
    </div> 
  )
}
