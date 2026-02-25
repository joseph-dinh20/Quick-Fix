import axios from "axios"

const API = "http://localhost:8000/api"

export const signup = (data) => {
  return axios.post(`${API}/accounts/signup/`, {
    name: data.name,
    email: data.email,
    password: data.password
  })
}