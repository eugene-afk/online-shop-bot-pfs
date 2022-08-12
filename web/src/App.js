import { BrowserRouter, Route, Routes } from "react-router-dom"
import { useEffect } from 'react'

import Layout from './components/base/Layout'
import HomePage from './pages/HomePage'
import CheckoutPage from "./pages/CheckoutPage"
import CartPage from "./pages/CartPage"
import OrdersPage from "./pages/OrdersPage"

function App() {
    useEffect(() => {
      try{
          window.Telegram.WebApp.ready()
      }
      catch(ex){
          console.log(ex)
      }
    })
    return (
      <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<HomePage />} />
          <Route path="tg/:id" element={<HomePage />} />
          <Route path="checkout" element={<CheckoutPage />} />
          <Route path="cart" element={<CartPage />} />
          <Route path="orders" element={<OrdersPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
    )
}

export default App
