const isValidJsObject = (obj) => {
    
    if(typeof obj === 'object' &&
        obj !== null &&
        !Array.isArray(obj) &&
        obj !== undefined){
            return true
    }
    
    return false
}

const getOrderStatus = (num) => {
    switch(num){
        case 0:
            return "Unpaid"
        case 1:
            return "Pending"
        case 2:
            return "Sended"
        case 3:
            return "Delivered"
        default:
            return "Unknown"
    }
}

const getNextOrderStatus = (str) => {
    switch(str){
        case "Pending":
            return "Sended"
        case "Sended":
            return "Delivered"
        default:
            return ""

    }
}

export { isValidJsObject, getOrderStatus, getNextOrderStatus }