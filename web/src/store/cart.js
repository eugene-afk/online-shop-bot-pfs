import { createSlice } from '@reduxjs/toolkit'
import { isValidJsObject } from '../utils/index'

const cartSlice = createSlice({
  name: 'cart',

  initialState: {
    products: [],
  },

  reducers: {
    addProductToCart: (state, action) => {
        if(isValidJsObject(action.payload)){
            action.payload.price = parseFloat(action.payload.price).toFixed(2)
            return { ...state, products: [{
                ...action.payload,
                qty: 1,
                total: action.payload.price,
                outOfStock: false,
            }, ...state.products] }
        }
        return state
    },

    incrementProductQty: (state, action) => {
        const products = state.products.map(x => {
            if(x.id === action.payload){
                var newObj = JSON.parse(JSON.stringify(x))
                newObj.qty += 1
                if(newObj.stock_qty <= newObj.qty){
                    newObj.outOfStock = true
                    newObj.qty = newObj.stock_qty
                }
                newObj.total = parseFloat(newObj.price * newObj.qty).toFixed(2)
                return newObj
            }
            return x
        })

        return {...state, products: [...products]}
    },

    decrementProductQty: (state, action) => {
        const products = state.products.map(x => {
            if(x.id === action.payload){
                var newObj = JSON.parse(JSON.stringify(x))
                if(newObj.outOfStock === true){
                    newObj.outOfStock = false
                }
                newObj.qty -= 1
                if(newObj.qty < 1){
                    newObj.qty = 1
                }
                newObj.total = parseFloat(newObj.price * newObj.qty).toFixed(2)
                return newObj
            }
            return x
        })

        return {...state, products: [...products]}
    },

    setProductQtyByValue: (state, {qty, id}) => {
        const products = state.products.map(x => {
            if(x.id === id){
                var newObj = JSON.parse(JSON.stringify(x))
                newObj.qty = qty
                if(newObj.stock_qty <= newObj.qty){
                    newObj.qty = newObj.stock_qty
                    newObj.outOfStock = true
                }
                if(newObj.qty < 1){
                    newObj.qty = 1
                }
                newObj.total = parseFloat(newObj.price * newObj.qty).toFixed(2)
                return newObj
            }
            return x
        })

        return {...state, products: [...products]}
    },

    removeProductFromCart: (state, action) => {
        const products = state.products.filter(x => x.id !== action.payload)
        return { ...state, products: [...products] }
    },

    clearCartProducts: state => {
        return { ...state, products: [] }
    }

  }
})

export const { getCartAmount, 
                isProductInCart, 
                addProductToCart, 
                incrementProductQty, 
                decrementProductQty, 
                setProductQtyByValue,
                removeProductFromCart,
                clearCartProducts,
             } = cartSlice.actions

export const selectProductInCart = id => state => {
    const product = state.cart.products.find(x => x.id === id) 
    if(product){
        return true
    }
    return false
}

export const selectProductQty = id => state => {
    const product = state.cart.products.find(x => x.id === id) 
    if(product){
        return product.qty
    }
    return 1
}

export const selectCartAmount = state => {    
    if(state.cart.products.length > 1){
        return state.cart.products.reduce((accumulator, object) => {
            return parseFloat(parseFloat(accumulator) + parseFloat(object.total)).toFixed(2)
        }, 0)
    }
    try { return state.cart.products[0].total }
    catch { return 0 }
}

export const selectOutOfStock = id => state =>  state.cart.products.find(x => x.id === id).outOfStock 

export const selectCartItemsQty = state => state.cart.products.length

export const selectCartItems = state => state.cart.products

export default cartSlice.reducer