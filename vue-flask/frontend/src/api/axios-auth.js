import axios from 'axios'

let urlDesktop =  "127.0.0.1:5000"
let urlRasp = "192.168.1.216:5000"

const instance = axios.create({
    baseURL: `http://${urlRasp}`,
    headers: {
        'Authorization': {
            toString() {
                return `Bearer ${localStorage.getItem('token')}`
            }
        }
    }
});

export default instance