import axios from 'axios';
import cors from 'cors';

// Create a new Axios instance
export const axiosInstance = axios.create({
  baseURL: 'http://localhost:8000/api', // Your API base URL
});

// Enable CORS for this Axios instance
axiosInstance.defaults.headers.common['Access-Control-Allow-Origin'] = '*'; // Set the desired origin
axiosInstance.interceptors.request.use(
    config => {
      const token = localStorage.getItem('access_token'); // Retrieve the token from localStorage
      if (token) {
        config.headers.Authorization = `Bearer ${token}`; // Set the Authorization header
      }
      return config;
    },
    error => {
      return Promise.reject(error);
    }
  );
// Now you can use axiosInstance for your requests
// axiosInstance.get('/data')
//   .then(response => {
//     console.log(response.data);
//   })
//   .catch(error => {
//     console.error('Error:', error);
//   });
