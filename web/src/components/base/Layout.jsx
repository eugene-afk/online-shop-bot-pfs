import React from 'react'
import { Outlet } from "react-router-dom"
import {
    MDBContainer,
} from 'mdb-react-ui-kit'

import Header from './header/Header'
import Footer from './Footer'

function Layout() {
    return (
        <>
            <Header />
            <MDBContainer className='main my-4'>
                <Outlet />
            </MDBContainer>
            <Footer />
        </>
    )
}

export default Layout