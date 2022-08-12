import React from 'react'
import { 
    MDBBtn,
} from 'mdb-react-ui-kit'
import { useSelector } from 'react-redux'
import {Link} from 'react-router-dom'

import { selectCartItems, selectCartAmount } from '../../store/cart'
import ProductCartCard from './ProductCartCard'

function Cart() {
    const cartProducts = useSelector(selectCartItems)
    const cartAmount = useSelector(selectCartAmount)

    return (
            <>
                {/* if cart doesn't have items show empty cart message */}
                {cartProducts.length > 0 
                    ?
                        <>
                            <div>
                                {cartProducts.map((i, index) => (
                                    <ProductCartCard product={i} key={index} />
                                ))}
                            </div>

                            <div className='h4'>
                                <span>Amount: </span> {cartAmount} ₴
                            </div>

                            <div className='w-100 text-center mt-4'>
                                <Link to="/checkout">
                                    <MDBBtn>
                                        Checkout
                                    </MDBBtn>
                                </Link>
                            </div>
                        </>
                    :
                        <div className='w-100 text-center'>Cart empty.</div>
                }

            </>
    )
}

export default Cart