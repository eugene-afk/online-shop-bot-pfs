import React from 'react'
import {
    MDBCard,
    MDBCardBody,
    MDBCardImage,
    MDBCardTitle,
    MDBCardSubTitle,
    MDBBtn,
    MDBIcon,
  } from 'mdb-react-ui-kit'
import { useSelector, useDispatch } from 'react-redux'
import { addProductToCart, selectProductInCart, removeProductFromCart, clearCartProducts } from '../../store/cart'
import { useNavigate } from "react-router-dom"

import ProductQty from './ProductQty'

function ProductCard({product}) {
    const isInCart = useSelector(selectProductInCart(product.id))
    const dispatch = useDispatch()
    const navigate = useNavigate()

    const fastBuy = (product) => {
        dispatch(clearCartProducts())
        dispatch(addProductToCart(product))
        navigate("/checkout")
    }

    return (
        <MDBCard className='h-100'>
            <MDBCardImage src={product.image_url} alt={product.name} position='top' />
            <MDBCardBody className='p-2'>
                <MDBCardTitle>{product.name}</MDBCardTitle>
                <MDBCardSubTitle>{parseFloat(product.price).toFixed(2)} ₴</MDBCardSubTitle>
                <div className="text-center">
                    {isInCart === true ? 
                        <div>
                            <MDBBtn onClick={() => dispatch(removeProductFromCart(product.id))} className='m-1 bg-danger w-100'>
                                <MDBIcon fas icon="trash-alt" /> Remove
                            </MDBBtn> 
                            
                            <ProductQty margin="mt-2" id={product.id} />
                        </div>
                        :
                        <>
                            {product.stock_qty === 0
                            ?
                                <div className='text-center w-100'>Not in stock</div>
                            :
                                <div className='w-100 d-lg-flex'>
                                    <MDBBtn onClick={() => dispatch(addProductToCart(product))} className='m-1 bg-primary w-100'>
                                        <MDBIcon fas icon="cart-plus" /> Add
                                    </MDBBtn> 

                                    <MDBBtn className='m-1 bg-secondary w-100' onClick={() => fastBuy(product)}>
                                        <MDBIcon fas icon="shipping-fast" /> Buy it now!
                                    </MDBBtn>
                                </div>
                            }
                        </>
                        
                    }
                </div>
            </MDBCardBody>
        </MDBCard>
    )
}

export default ProductCard