import axios from "axios";

const API = "http://localhost:8000/api";

const api = axios.create({
  baseURL: API,
  withCredentials: true,
});

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
  const value = `; ${document.cookie}`;
  const parts = value.split(`; csrftoken=`);
  if (parts.length === 2) return parts.pop().split(";").shift();
  return null;
}

export const updateProfile = (formData) => {
  return api.put("/accounts/profile/update/", formData, {
    withCredentials: true,
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  });
};

export const updateServiceProvider = (formData) => {
  return api.put("/accounts/provider/update/", formData, {
    withCredentials: true,
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  });
};

export const deleteWorkImage = (id) => {
  return api.delete(`/accounts/provider/work-images/${id}/delete/`, {
    withCredentials: true,
    headers: {
      "X-CSRFToken": getCSRFToken(),
    },
  });
};

export const loadMyProvider = () => {
  return api.get("/accounts/provider/me/");
};

export const getServices = () => {
  return api.get("/accounts/services/");
};

export const updateProviderServices = (services) => {
  return api.put("/accounts/provider/services/update/", {
    services,
  });
};

export default api;