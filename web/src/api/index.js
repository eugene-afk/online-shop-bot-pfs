import productsModule from './products'
import instance from './instance'
import ordersModule from './orders'

const api = {
    products: productsModule(instance),
    orders: ordersModule(instance),
}

export default api