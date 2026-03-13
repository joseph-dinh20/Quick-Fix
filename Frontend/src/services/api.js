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


export const loadProvider = (id) => {
  return api.get(`/accounts/providers/${id}/`);
};


function getCSRFToken() {
  const value = `; ${document.cookie}`
  const parts = value.split(`; csrftoken=`)
  if (parts.length === 2) return parts.pop().split(';').shift()
}


export const updateProfile = (formData) => {
  return api.put('/accounts/profile/update/',
    formData,
    {
      withCredentials: true,
      headers: {
        "X-CSRFToken": getCSRFToken(),
      }
    }
  );
}


export const updateServiceProvider = (formData) => {
  return api.put('/accounts/provider/update/',
    formData,
    {
      withCredentials: true,
      headers: {
        "X-CSRFToken": getCSRFToken(),
      }
    }
  );
}