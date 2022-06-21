// api/index.js

//
// omitting stuff ... skipping to the bottom of the file


const urlDesktop = "127.0.0.1:5000"
const urlRasp = "192.168.1.216:8080"


export function authenticate (userData) {  
    const response = await fetch(`http://${urlDesktop}/login`, {
        method: "POST",
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify(userData),
      })
}
  