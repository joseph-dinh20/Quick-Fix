import axios from "axios";

const API = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API,
  withCredentials: true, // REQUIRED for Django session cookies
});

// Fetch CSRF token once and attach it to all future requests
export const initCsrf = async () => {
  const res = await api.get("/accounts/csrf/");
  const token = res.data?.csrfToken;
  if (token) {
    api.defaults.headers.common["X-CSRFToken"] = token;
  }
  return token;
};

export const signup = (data) => {
  return api.post("/accounts/signup/", {
    name: data.name,
    email: data.email,
    password: data.password,
  });
};

export const login = (data) => {
  return api.post("/accounts/login/", {
    email: data.email,
    password: data.password,
  });
};

export const logout = () => {
  return api.post("/accounts/logout/");
};

export const me = () => {
  return api.get("/accounts/me/");
};

// provider fetch helper – returns promise for a single provider by ID
export const loadProvider = (id) => {
  return api.get(`/accounts/providers/${id}/`);
};