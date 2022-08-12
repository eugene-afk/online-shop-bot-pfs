import React from 'react'
import {
    MDBIcon,
} from 'mdb-react-ui-kit'
import { useSelector, useDispatch } from 'react-redux'
import { incrementProductQty, decrementProductQty, selectProductQty, selectOutOfStock } from '../../store/cart'

function ProductQty(props) {
    const productQty = useSelector(selectProductQty(props.id))
    const productOutOfStock = useSelector(selectOutOfStock(props.id))
    const dispatch = useDispatch()

    return (
        <>
            <div className={`d-flex ${props.center === false ? '' : 'justify-content-center'} ${props.margin}`}>
                <MDBIcon fas icon="minus"
                        className='align-self-center text-primary'
                        style={{cursor: 'pointer'}}
                        size='lg'
                        onClick={() => dispatch(decrementProductQty(props.id))} />
                        
                <span className='mx-4'>{productQty}</span>

                <MDBIcon fas icon="plus" 
                        className='align-self-center text-primary'
                        style={{cursor: 'pointer'}}
                        size='lg' 
                        onClick={() => dispatch(incrementProductQty(props.id))} />
            </div>
            {productOutOfStock ? <div className='text-danger'>Out of stock</div> : null}
        </>        
    )
}

export default ProductQty