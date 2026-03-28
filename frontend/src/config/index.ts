import Constants from 'expo-constants';

/**
 * Config.ts
 * Maneja la detección automática de la IP de desarrollo y la URL de producción.
 */

// URL de producción (Cambiar por tu dominio real al desplegar)
const PRODUCTION_API_URL = 'http://api.tuservidor.com/api/';

// Obtener la IP de la computadora de desarrollo de forma automática
const getDevIp = () => {
  const debuggerHost = Constants.expoConfig?.hostUri;
  if (!debuggerHost) return '127.0.0.1';
  
  // Extrae solo la IP antes de los dos puntos (ej. 192.168.1.5:8081 -> 192.168.1.5)
  return debuggerHost.split(':')[0];
};

const DEV_API_URL = `http://${getDevIp()}:8000/api/`;

export const Config = {
  API_URL: __DEV__ ? DEV_API_URL : PRODUCTION_API_URL,
  IS_DEV: __DEV__,
};

console.log('📡 [API Config]:', Config.API_URL);
