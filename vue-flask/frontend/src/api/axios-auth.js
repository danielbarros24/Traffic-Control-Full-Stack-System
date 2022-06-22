import axios from 'axios'

let urlDesktop =  "127.0.0.1:5000"
let urlRasp = "192.168.1.216:5000"

const instance = axios.create({
    baseURL: 'http://192.168.1.216:5000',
    headers: {
        'Authorization': {
            toString() {
                return `Bearer ${localStorage.getItem('token')}`
            }
        }
    }
});

export default instance