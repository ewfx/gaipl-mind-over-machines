/* eslint-disable prettier/prettier */
const API_URL = 'http://localhost:8000/api/push-record'

class ApiService {
    static postIncident(payload) {
      console.log(JSON.stringify(payload))
      fetch(API_URL , {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(payload),
      }).catch((error) => console.error('Error posting record:', error));
    }
  }
export default ApiService
