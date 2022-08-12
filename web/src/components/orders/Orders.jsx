import React, {useState, useEffect} from 'react'
import { 
    MDBBtn, 
    MDBRow, 
    MDBAccordion, 
    MDBCol,
    MDBInput,
} from 'mdb-react-ui-kit'

import api from '../../api/index'
import OrderCard from './OrderCard'

function Orders() {
    const [file, setFile] = useState(null)
    const [busy, setBusy] = useState(false)
    const [fileName, setFileName] = useState("")
    const [orders, setOrders] = useState([])
    const [isAdmin, setIsAdmin] = useState(false)
    const [filters, setFilters] = useState({
        user_id: window.tgUserId ? window.tgUserId : 0,
        desc: 1,
        search_user_name: "",
        status: "",
    })

    useEffect( () => { 
        fetchOrders()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    // on filters update - fetch filtered result
    const handleChangeFilter = async(e, key) => {
        let updatedValue = {}
        updatedValue[key] = e.target.value
        
        let localFilters = {
            ...filters,
            ...updatedValue
        }
        setFilters(localFilters)
        // orders update by search filter have separate btn
        if(key !== "search_user_name"){
            await fetchOrders(localFilters)
        }
    }

    const clearSearchFilter = async() => {
        let updatedValue = {search_user_name: ""}
        let localFilters = {...filters, ...updatedValue}
        setFilters(localFilters)
        await fetchOrders(localFilters)
    }

    const fetchOrders = async(localFilters=null) => {
        try {
            const res = (await api.orders.getOrders(localFilters !== null ? localFilters : filters)).data
            setOrders(res.orders)
            setIsAdmin(res.is_admin)
        } 
        catch(ex) {
            console.log(ex)
        }
    }

    const createFile = async() => {
        try{
            const fileNameStr = `orders_report_${(new Date().toJSON())}`
            setFileName(fileNameStr)
            setBusy(true)
            const response = (await api.orders.getExcelDocument(filters, fileNameStr)).data
            setFile(response)
        }
        catch(ex){
            console.log(ex)
        }
        finally{
            setBusy(false)
        }
    }

    const downloadFile = () => {
        let filename = `${fileName}.xlsx`
        filename = decodeURI(filename)
        const url = window.URL.createObjectURL(file)
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', filename)
        document.body.appendChild(link)
        link.click()
        window.URL.revokeObjectURL(url)
        link.remove()
    }

  return (

    <MDBRow className='justify-content-center'>
        <MDBCol size="12">
            {/* search by user name input available only for admins */}
            <div className="d-flex">
                {isAdmin
                ?
                    <>
                        <MDBInput className="flex-grow-1" label='Search' type='text' 
                            value={filters.search_user_name} 
                            onChange={(e) => handleChangeFilter(e, "search_user_name")} />
                        <MDBBtn className='ms-2' onClick={() => fetchOrders()}>Search</MDBBtn>
                        {filters.search_user_name !== "" ? <MDBBtn className='ms-2 bg-danger' 
                            onClick={() => clearSearchFilter()}>Clear</MDBBtn> : null} 
                    </>
                :
                    null
                }                
            </div>

            <div className="d-flex">
                <div className='flex-grow-1 mt-2 me-2'>
                    <select className="w-100" id="fruit" value={filters.status} onChange={(e) => handleChangeFilter(e, "status")}>
                        <option value="">All statuses</option>
                        <option value="Pending">Pending</option>
                        <option value="Sended">Sended</option>
                        <option value="Delivered">Delivered</option>
                    </select>
                </div>

                <div className='mt-2'>
                    {filters.desc === 1
                    ?
                        <MDBBtn onClick={() => handleChangeFilter({target:{value: 0}}, "desc")}>
                            Sort by date ascending
                        </MDBBtn>
                    :
                        <MDBBtn onClick={() => handleChangeFilter({target:{value: 1}}, "desc")}>
                            Sort by date descending
                        </MDBBtn>
                    }
                </div>
            </div>
        </MDBCol>

        {orders.length < 1 
        ?
            <>
                {/* showing loading if no items, showing nothing found message if the filtered result doesn't contain items */}
                {filters.status === "" && filters.search_user_name === ""
                ?
                    <div className="text-center">Loading...</div>
                :
                    <div className="text-center">Nothing found...</div>
                }
            </>
        :
            <>
                {/* excel buttons showing if user is admin */}
                <MDBCol size="12" className="my-1">
                    {orders.length > 0 && isAdmin
                    ?
                        <>
                            <MDBBtn className='bg-success me-2' onClick={() => createFile()} disabled={busy ? true : false}>
                                Create excel document
                            </MDBBtn>

                            {/* download button showing when file downloaded from api */}
                            {file !== null 
                            ?
                                <MDBBtn onClick={() => downloadFile()}>
                                    Download
                                </MDBBtn>
                            :
                                null
                            }
                        </>
                    :
                        null
                    }
                </MDBCol>

                {/* orders list */}
                <MDBCol size="12">
                    <MDBAccordion alwaysOpen className='my-2'>
                        {orders.map((i) => (
                            <OrderCard order={i} isAdmin={isAdmin} key={i.id} />
                        ))}
                    </MDBAccordion>
                </MDBCol>
            </>
        }
    </MDBRow>
  )
}

export default Orders