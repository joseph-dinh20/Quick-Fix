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

export const loadProviders = () => {
  return api.get(`/accounts/providers/`, params);
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

export const favoriteProvider = (id) => {
  return api.post(`/accounts/providers/${id}/favorite/`)
}

export const unfavoriteProvider = (id) => {
  return api.delete(`/accounts/providers/${id}/favorite/remove/`)
}

export const getFavorites = () => {
  return api.get(`/accounts/providers/favorites/`)
}

export const isFavoriteProvider = (id) => {
  return api.get(`/accounts/providers/${id}/is-favorite/`)
}

export const getNearbyProviders = (userLat = 33.7816133, userLng = -118.1084064, milesRadius = 5) => {
  return api.get("accounts/providers/nearby/", {
    params: {
      lat: userLat,
      lng: userLng,
      max_distance: milesRadius
    }
  })
}

export const searchProviders = (params) => {
  return axios.get("/accounts/search_providers", {
    params
  })
}

export const createJob = (data) => {
  const formData = new FormData();

  formData.append("title", data.title);
  formData.append("description", data.description);
  formData.append("budget", data.budget || "");
  formData.append("deadline", data.deadline);
  formData.append("request_type", data.request_type);

  // services (IDs)
  data.services.forEach(id => {
    formData.append("services", id);
  });

  // images
  if (data.images) {
    data.images.forEach(file => {
      formData.append("images", file);
    });
  }

  return api.post("/jobs/create/", formData, {
    headers: {
      "Content-Type": "multipart/form-data"
    }
  });
};

export const getMyJobs = () => {
  return api.get("/jobs/mine/");
};


export function toggleFavoriteJob(jobId) {
  return api.post(`/jobs/${jobId}/favorite/`);
}


export function getAllJobs() {
  return api.get("/jobs/");
}


export function deleteJob(jobId) {
  return api.delete(`/jobs/${jobId}/delete/`);
}


export function toggleFavoriteProvider(providerId) {
  return api.post(`/accounts/providers/${providerId}/favorite/`);
}


export function fetchReviews(id) {
  return api.get(`/reviews/${id}/reviews/`)
}


export function deleteReview(id) {
  return api.delete(`/reviews/delete/${id}/`)
}


export function updateReview(id, formData) {
  return api.put(`/reviews/update/${id}/`, formData)
}

export function deleteReviewImage(id) {
  return api.delete(`/reviews/images/${id}/delete/`)
}

export default api;
