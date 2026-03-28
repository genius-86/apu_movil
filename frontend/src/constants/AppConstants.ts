/**
 * AppConstants.ts
 * Centraliza todos los literales y estados de la aplicación para evitar hardcoding.
 */

export const APP_CONSTANTS = {
  // Estados de Materiales
  MATERIAL_TYPES: [
    { value: 'INSTALADO', label: 'Instalado' },
    { value: 'DESMONTADO', label: 'Desmontado' },
  ],

  // Estados de Actividad (Mapeo de lógica interna)
  ACTIVITY_STATUS: {
    PENDING: 'Pendiente',
    IN_PROGRESS: 'En Proceso',
    COMPLETED: 'Completado',
  },

  // Tipos de Fotos
  PHOTO_TYPES: {
    BEFORE: 'ANTES',
    AFTER: 'DESPUES',
  },

  // Mensajes de UI
  MESSAGES: {
    OFFLINE_MODE: "Modo Fuera de Línea",
    OFFLINE_SAVED: "Su actividad se guardó localmente. Sincronice cuando regrese a una zona con red.",
    SAVE_SUCCESS: "Actividad finalizada correctamente",
    NETWORK_ERROR: "No se pudo conectar con el servidor. Verifique su conexión o intente entrar de nuevo.",
    REQUIRED_PHOTO: "Debe capturar el registro fotográfico final para poder guardar.",
    REQUIRED_SIGNATURE: "Debe firmar la actividad para poder guardarla.",
    CRITICAL_ERROR: "Error Crítico",
    QUEUE_ERROR: "No se pudo encolar localmente la actividad.",
  }
};
