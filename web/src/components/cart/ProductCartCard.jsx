import React from 'react'
import { 
    MDBCard,
    MDBCardBody,
    MDBCardTitle,
    MDBBtn,
    MDBIcon,
} from 'mdb-react-ui-kit'
import { useDispatch } from 'react-redux'

import ProductCardQty from '../products/ProductQty'
import { removeProductFromCart } from '../../store/cart'

function ProductCartCard({product}) {
    const dispatch = useDispatch()
    return (
        <MDBCard className='shadow-0 my-2'>
            <MDBCardBody>
                <MDBCardTitle>
                    <img src={product.image_url} alt={product.name} width="44" height="44" />
                    <span>{product.name}</span>
                </MDBCardTitle>
                <ProductCardQty id={product.id} center={false} />
                <div><strong>Price: {product.price} ₴</strong></div>
                <div><strong>Total: {product.total} ₴</strong></div>
                <MDBBtn className='bg-danger' onClick={() => dispatch(removeProductFromCart(product.id))}>
                    <MDBIcon fas icon="trash-alt" />
                </MDBBtn>
            </MDBCardBody>
        </MDBCard>
    )
}

export default ProductCartCard