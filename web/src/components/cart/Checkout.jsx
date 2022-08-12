import { useEffect } from 'react'
import { 
    MDBTable,
    MDBTableHead,
    MDBTableBody,
} from 'mdb-react-ui-kit'
import { useSelector, useDispatch } from 'react-redux'
import { selectCartItems, clearCartProducts, selectCartAmount } from '../../store/cart'

const telegram = window.Telegram.WebApp

function Checkout() {
    const cartProducts = useSelector(selectCartItems)
    const cartAmount = useSelector(selectCartAmount)
    const dispatch = useDispatch()

    useEffect(() => {
        try{
            telegram.onEvent('mainButtonClicked', sendInvoice)
            telegram.MainButton.text = "Confirm and pay"
            telegram.MainButton.show()
        }
        catch(ex){
            console.log(ex)
        }

        return () => {
            telegram.MainButton.hide()
        }
      })

    const sendInvoice = () => {
        try{
            //TODO: here we can check string size to pervent tg limits: new Blob([JSON.stringify(cartProducts)]).size > 4096
            telegram.sendData(JSON.stringify(cartProducts))
            dispatch(clearCartProducts())
        }
        catch(ex){
            console.log(ex)
        }
    }

    return (
        <>
            {/* if cart doesn't have items show empty cart message */}
            {cartProducts.length > 0 
            ?
                <div className="responsive-x">
                    <MDBTable>
                        <MDBTableHead>
                            <tr>
                                <th scope='col'>#</th>
                                <th scope='col'>Name</th>
                                <th scope='col' className='text-center'>Qty</th>
                                <th scope='col'>Total</th>
                            </tr>
                        </MDBTableHead>
                        <MDBTableBody>
                            {cartProducts.map((i, index) => (
                                <tr key={i.id}>
                                    <th scope='row'>{index + 1}</th>
                                    <td>{i.name}</td>
                                    <td className='text-center'>{i.qty}</td>
                                    <td>{i.total} ₴</td>
                                </tr>
                            ))}
                            <tr>
                                <td colSpan="3" className='h4'>
                                    Amount:
                                </td>
                                <td className='h4'>
                                    {cartAmount} ₴
                                </td>
                            </tr>
                        </MDBTableBody>
                    </MDBTable>
                </div>
            :
                <div className='w-100 text-center'>Cart empty.</div> 
            }
        </>
    )
}

export default Checkout