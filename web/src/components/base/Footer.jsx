import React from 'react'
import { MDBFooter } from 'mdb-react-ui-kit';

function Footer() {
  return (
    <MDBFooter bgColor='light' className='text-lg-left text-white fixed-bottom'>
      <div className='text-left p-3' style={{ backgroundColor: 'rgba(0, 0, 0, 0.2)' }}>
        {new Date().getFullYear()} — Test task for PayForSay
      </div>
    </MDBFooter>
  )
}

export default Footer