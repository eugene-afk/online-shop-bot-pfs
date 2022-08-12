import React from 'react'
import { Link } from "react-router-dom"
import { useSelector } from 'react-redux'
import {
    MDBNavbar,
    MDBContainer,
    MDBIcon,
    MDBBtn,
    MDBBadge,
} from 'mdb-react-ui-kit'

import "./Header.css"
import { selectCartItemsQty } from '../../../store/cart'
import logo from '../../../logo.png'
function Header() {
    const cartItemsQty = useSelector(selectCartItemsQty)

    return (
        <header>
            <MDBNavbar fixed='top' expand='lg' light bgColor='white'>
                <MDBContainer fluid>

                    <Link to="/" className="navbar-brand">
                        <img src={logo} alt="Logo" width="38" height="38" />
                    </Link>

                    <div>
                        <Link to="/orders">
                            <MDBBtn floating size='lg' className='me-2'>
                                <MDBIcon fas icon="list-alt fa-lg" />
                            </MDBBtn>
                        </Link>

                        <Link to="/cart">
                            <MDBBtn floating size='lg'>
                                <MDBIcon fas icon="shopping-cart fa-lg" />
                                {/* if cart has items - show badge with items count */}
                                {cartItemsQty > 0 ? 
                                    <MDBBadge color='danger' notification pill>
                                        {cartItemsQty}
                                    </MDBBadge>
                                    :
                                    null
                                }
                                
                            </MDBBtn>
                        </Link>

                    </div>
                </MDBContainer>
            </MDBNavbar>
        </header>
    )
}

export default Header