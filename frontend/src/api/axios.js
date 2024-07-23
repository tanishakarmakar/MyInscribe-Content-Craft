import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://35.175.132.213/' //'http://localhost:5000', // Updated base URL
});

instance.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

export default instance;
