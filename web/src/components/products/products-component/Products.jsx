import React, {useState, useEffect} from 'react'
import {useParams} from 'react-router-dom'
import { MDBRow, MDBCol, MDBBtn, MDBInput } from 'mdb-react-ui-kit'

import ProductCard from '../ProductCard'
import api from '../../../api/index'
import './Products.css'

function Products() {
    const params = useParams()
    window.tgUserId = params.id ? params.id : 0 //get tg user id from url params and save as global var
    const [products, setProducts] = useState([])
    const [categories, setCategories] = useState([])
    const [searchText, setSearchText] = useState("")
    const [categoryId, setCategoryId] = useState(0)
    const handleSearchTextChange = (e) => setSearchText(e.target.value)
    const handleCategoryChange = (e) => {setCategoryId(e.target.value); fetchProducts(searchText, e.target.value)}

    const fetchProducts = async(srch=searchText, category=categoryId) => {
        try {
            const res = (await api.products.getProducts({
                search: srch,
                category_id: category, 
            })).data
            setProducts(res)
        } 
        catch(ex) {
            console.log(ex)
        }
    }

    const fetchCategories = async() => {
        try{
            const res = (await api.products.getCategories()).data
            setCategories(res)
        }
        catch(ex){
            console.log(ex)
        }
    }

    useEffect( () => {
        fetchProducts()
        fetchCategories()
        // eslint-disable-next-line react-hooks/exhaustive-deps
    }, [])

    return (
        <MDBRow>
            {/* search input */}
            <MDBCol size="12">
                <div className="d-flex">
                    <MDBInput className="flex-grow-1" label='Search' type='text' value={searchText} onChange={handleSearchTextChange} />
                    <MDBBtn className='ms-2' onClick={() => fetchProducts()}>Search</MDBBtn>
                    {searchText !== "" ? <MDBBtn className='ms-2 bg-danger' 
                        onClick={() => {setSearchText("");fetchProducts("")}}>Clear</MDBBtn> : null} 
                </div>
                <div>
                    <select className="w-100 mt-2" id="fruit" value={categoryId} onChange={handleCategoryChange}>
                        <option value="0" key="0">All categories</option>
                        {categories.map((i) => (
                            <option value={i.id} key={i.id}>{i.name}</option>
                        ))}
                    </select>
                </div>
            </MDBCol>
            
            {(products.length < 1 )
            ?
                <>
                    {/* showing loading if no items, showing nothing found message if the filtered result doesn't contain items */}
                    {searchText === "" && categoryId === 0
                    ?
                        <span className='text-center'>Loading...</span>
                    :
                        <span className='text-center'>Nothing found...</span>
                    }
                </>
            :
                <>
                    {/* products list */}
                    {products.map((i) => (
                        <MDBCol size="6" lg="3" className='p-2' key={i.id}>
                            <ProductCard product={i} />
                        </MDBCol>
                    ))}
                </>
            }
        </MDBRow>
    )
}

export default Products

