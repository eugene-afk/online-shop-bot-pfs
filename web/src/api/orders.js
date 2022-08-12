export default function testModule(instance){
    return{
        getOrders(args){
            return instance.get('orders/', {params: args})
        },

        getExcelDocument(args, filename){
            return instance.get(`orders/excel/${filename}`, {params: args, responseType: "blob"})
        },
        
        updateOrderStatus(payload){
            return instance.patch('orders/update', payload)
        }
    }
}