export default function testModule(instance){
    return{
        getProducts(args){
            return instance.get('products/', {params: args})
        },
        
        getCategories(){
            return instance.get('products/categories')
        },
    }
}