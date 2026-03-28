import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Config } from '../config';

const API_URL = Config.API_URL;

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use(
  async (config) => {
    try {
      const token = await AsyncStorage.getItem('access_token');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
    } catch (error) {
      console.error('Error al obtener el token', error);
    }
    return config;
  },
  (error) => Promise.reject(error)
);

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        const refreshToken = await AsyncStorage.getItem('refresh_token');
        if (!refreshToken) throw new Error('No refresh token available');
        
        const response = await axios.post(`${API_URL}token/refresh/`, {
          refresh: refreshToken,
        });
        const { access } = response.data;
        await AsyncStorage.setItem('access_token', access);
        api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
        
        // Update original request header and retry
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        console.error('Token refresh failed:', refreshError);
        await AsyncStorage.removeItem('access_token');
        await AsyncStorage.removeItem('refresh_token');
        // Aquí se debería redirigir al Login o despachar acción de logout
        // router.replace('/login');
        return Promise.reject(refreshError);
      }
    }
    return Promise.reject(error);
  }
);

// Service Endpoints
export const authService = {
  login: (usuario, clave) => api.post('token/', { usuario, password: clave }),
  logout: async () => {
    await AsyncStorage.removeItem('access_token');
    await AsyncStorage.removeItem('refresh_token');
  }
};

export const activityService = {
  list: (params) => api.get('actividades/', { params }),
  detail: (id) => api.get(`actividades/${id}/`),
  save: (data) => data.id_actividad ? api.patch(`actividades/${data.id_actividad}/`, data) : api.post('actividades/', data),
  start: (id, coords) => api.post(`actividades/${id}/start/`, coords),
  addMaterial: (id, data) => api.post(`actividades/${id}/add_material/`, data),
  addPhoto: (id, formData) => api.post(`actividades/${id}/add_photo/`, formData, {
    headers: { 'Content-Type': 'multipart/form-data' }
  }),
  addSignature: (id, data) => api.post(`actividades/${id}/add_signature/`, data),
  finish: (id) => api.post(`actividades/${id}/finish/`)
};

export const masterService = {
  getLuminarias: (params) => api.get('luminarias/', { params }),
  getArticulos: (params) => api.get('articulos/', { params }),
  getParameters: () => api.get('parametros/')
};

export const pqrService = {
  list: (params) => api.get('pqr/', { params }),
  detail: (id) => api.get(`pqr/${id}/`)
};

export default api;
