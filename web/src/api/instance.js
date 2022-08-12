import axios from 'axios'
import { baseURL } from './baseUrl';

const instance = axios.create({
    baseURL: baseURL,
})

instance.interceptors.request.use(
  config => {
    config.headers = { 
      accept: 'application/json, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    }
    return config;
  },
  error => {
    Promise.reject(error)
});

instance.interceptors.response.use(function (response) {
    return response
  }, error => {
    if (error.response.status === 401) {

    }
    if (error.response.status === 429) {

    }
    return Promise.reject(error)
  })

export default instance