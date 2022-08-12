import React, {useState} from 'react'
import { MDBBtn } from 'mdb-react-ui-kit'

import {getNextOrderStatus, getOrderStatus} from '../../utils/index'
import api from '../../api/index'

function OrderCardStatusButton(props) {
    const [nextStatus, setNextStatus] = useState(getNextOrderStatus(getOrderStatus(props.status)))

    const updateOrderStatus = async() => {
        try{
            //try change order status
            const res = (await api.orders.updateOrderStatus({
                from_user_id: window.tgUserId ? window.tgUserId : 0,
                user_id: props.userId,
                status: nextStatus,
                order_id: props.orderId,
            }))
            // on success change status in view
            if(res.status === 200){
                props.changeStatus(nextStatus)
                setNextStatus(getNextOrderStatus(nextStatus))
            }
        }
        catch(ex){
            console.log(ex)
        }
    }

    return (
        <>
            {/* if order not delivered show button to change to the next status */}
            {nextStatus !== ""
            ?
                <MDBBtn onClick={() => updateOrderStatus()}>
                    {nextStatus}
                </MDBBtn>
            :
                null
            }
        </>
    )
}

export default OrderCardStatusButton