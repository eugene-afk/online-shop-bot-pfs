import React, {useState} from 'react'
import { 
    MDBAccordionItem,
    MDBCard,
    MDBCardBody,
    MDBCardTitle,
    MDBCardText,
    MDBListGroup,
    MDBListGroupItem,
} from 'mdb-react-ui-kit'

import {getOrderStatus} from '../../utils/index'
import OrderCardStatusButton from './OrderCardStatusButton'

function OrderCard(props) {
    const [status, setStatus] = useState(getOrderStatus(props.order.status))

    const changeStatus = (newStatus) => {
        setStatus(newStatus)
    }

    return (
        <>
            <MDBAccordionItem
                collapseId={1} 
                headerTitle={`Order #${props.order.id}, ${props.order.user.name}, ${props.order.created_at}`}>
                <MDBCard className='shadow-0'>
                    <MDBCardBody>
                        
                        {/* main info about order */}
                        <MDBCardTitle>{`Order #${props.order.id}`}</MDBCardTitle>
                        <MDBCardText>
                            <strong>Address: </strong> 
                            {`${props.order.country_code} ${props.order.state} ${props.order.city} ${props.order.street_line1} ${props.order.street_line2} ${props.order.post_code}`}
                            <br/>
                            <strong>Shipping method: </strong> {props.order.shipping_option_id}
                            <br/>
                            <strong>Shipping price: </strong> {props.order.shipping_price} ₴
                            <br/>
                            <strong>Status: </strong> {status}
                            <br/>
                            <strong>Created: </strong> {props.order.created_at}
                            <br/>
                            <strong>Updated: </strong> {props.order.updated_at}
                            <br/>
                            <strong>User: </strong> {props.order.user.name}
                            <br/>
                            <strong>Amount: </strong> <span className='h4'>{props.order.total_amount} ₴</span>
                            <br/>
                        </MDBCardText>

                        {/* order products info */}
                        <MDBListGroup className='mb-2'>
                            {props.order.products.map((orderProduct, index) => (
                                <MDBListGroupItem key={index}>
                                    <div>#{index + 1} <strong>{orderProduct.product.name}</strong></div>
                                    <div><strong>Price: </strong>{orderProduct.product.price} ₴</div>
                                    <div><strong>Qty: </strong>{orderProduct.qty}</div>
                                    <div><strong>Total: </strong>{orderProduct.total_price} ₴</div>
                                </MDBListGroupItem>
                            ))}
                        </MDBListGroup>

                        {/* change status button available only for admins */}
                        {props.isAdmin 
                        ?
                            <OrderCardStatusButton status={props.order.status} changeStatus={changeStatus} userId={props.order.user.id} orderId={props.order.id} />
                        : 
                            null
                        }
                        
                    </MDBCardBody>
                </MDBCard>
            </MDBAccordionItem>
        </>
    )
}

export default OrderCard