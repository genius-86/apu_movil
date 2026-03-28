import React, { useState, useEffect, useCallback } from 'react';
import { View, Text, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, Alert, Modal, TextInput, Image } from 'react-native';
import { useAuth } from '../src/context/AuthContext';
import { activityService } from '../src/services/api';
import { syncService } from '../src/services/SyncService';
import { FontAwesome5, Feather } from '@expo/vector-icons';
import * as Location from 'expo-location';
import * as ImagePicker from 'expo-image-picker';
import { useRouter, useFocusEffect } from 'expo-router';

export default function ActivitiesScreen() {
    const router = useRouter();
    const { user, logout } = useAuth() as any;
    const [activities, setActivities] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const [filter, setFilter] = useState('Pendientes');

    // Modal State Matches React implementation
    const [showStartModal, setShowStartModal] = useState(false);
    const [selectedActivity, setSelectedActivity] = useState<any>(null);
    const [startFormData, setStartFormData] = useState<any>({
        observacion: '',
        latitud: '',
        longitud: '',
        foto_antes: null
    });
    const [startError, setStartError] = useState('');
    const [gettingLocation, setGettingLocation] = useState(false);
    const [submitting, setSubmitting] = useState(false);
    const [syncQueueCount, setSyncQueueCount] = useState(0);
    const [syncing, setSyncing] = useState(false);

    // Auto-refresh when screen is focused
    useFocusEffect(
        useCallback(() => {
            if (user) {
                fetchActivities();
                checkSyncQueue();
            }
        }, [user])
    );

    const checkSyncQueue = async () => {
        const queue = await syncService.getQueue();
        setSyncQueueCount(queue.length);
    };

    const handleSync = async () => {
        setSyncing(true);
        try {
            const result = await syncService.syncAll();
            Alert.alert(
                "Sincronización Completada", 
                `Se subieron ${result.success} actividades al servidor.\nFallaron ${result.failed}.`
            );
            await checkSyncQueue();
            fetchActivities();
        } catch (error) {
            Alert.alert("Error", "Ocurrió un problema de red durante la sincronización.");
        } finally {
            setSyncing(false);
        }
    };

    const fetchActivities = async () => {
        try {
            const params: any = {};
            if (user?.es_tecnico) {
                params.id_tercero = user.id_tercero;
            }
            const response = await activityService.list(params);
            setActivities(response.data.results || response.data);
        } catch (error) {
            console.error('Error fetching activities:', error);
            Alert.alert("Error", "No se pudieron cargar las actividades");
        } finally {
            setLoading(false);
        }
    };

    const handleOpenStartModal = (activity: any) => {
        setSelectedActivity(activity);
        setStartFormData({
            observacion: '',
            latitud: activity.latitud ? activity.latitud.toString() : '',
            longitud: activity.longitud ? activity.longitud.toString() : '',
            foto_antes: null
        });
        setStartError('');
        setShowStartModal(true);
    };

    const handleCloseStartModal = () => {
        setShowStartModal(false);
        setSelectedActivity(null);
    };

    const handleLocationClick = async () => {
        setStartError('');
        setGettingLocation(true);
        try {
            let { status } = await Location.requestForegroundPermissionsAsync();
            if (status !== 'granted') {
                setStartError('Permiso de ubicación denegado.');
                setGettingLocation(false);
                return;
            }

            let location = await Location.getCurrentPositionAsync({ accuracy: Location.Accuracy.High });
            setStartFormData((prev: any) => ({
                ...prev,
                latitud: location.coords.latitude.toString(),
                longitud: location.coords.longitude.toString()
            }));
        } catch (error) {
            console.error(error);
            setStartError('No se pudo obtener la ubicación GPS.');
        } finally {
            setGettingLocation(false);
        }
    };

    const pickImage = async () => {
        try {
            const { status } = await ImagePicker.requestCameraPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Permiso Denegado', 'Lo sentimos, necesitamos permisos de cámara para continuar.');
                return;
            }

            let result = await ImagePicker.launchCameraAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: false,
                quality: 0.7,
            });

            if (!result.canceled) {
                setStartFormData((prev: any) => ({ ...prev, foto_antes: result.assets[0] }));
            }
        } catch (error) {
            setStartError('No se pudo abrir la cámara.');
        }
    };

    const confirmStartActivity = async () => {
        if (!selectedActivity) return;
        setStartError('');

        if (!startFormData.foto_antes) {
            setStartError("Debe capturar el registro fotográfico inicial.");
            return;
        }

        setSubmitting(true);
        try {
            const payload = {
                observacion: startFormData.observacion,
                latitud: startFormData.latitud,
                longitud: startFormData.longitud
            };

            await activityService.start(selectedActivity.id_actividad, payload);

            if (startFormData.foto_antes) {
                const formData = new FormData();
                formData.append('foto', {
                    uri: startFormData.foto_antes.uri,
                    name: `antes_${selectedActivity.id_actividad}.jpg`,
                    type: 'image/jpeg'
                } as any);
                formData.append('tipo', 'ANTES');
                try {
                    await activityService.addPhoto(selectedActivity.id_actividad, formData);
                } catch (photoError) {
                    console.error("No se pudo subir la foto inicial:", photoError);
                }
            }

            // Update local state instead of fetching to mimic original exactly
            setActivities((prev: any[]) => prev.map(act =>
                act.id_actividad === selectedActivity.id_actividad
                    ? {
                        ...act,
                        estado: 'En Progreso',
                        started: true,
                        ...startFormData
                    }
                    : act
            ));

            Alert.alert("Éxito", "Actividad iniciada correctamente.");
            handleCloseStartModal();
        } catch (error) {
            console.error("Error starting activity", error);
            Alert.alert("Error", "Hubo un error al iniciar la actividad.");
        } finally {
            setSubmitting(false);
        }
    };

    const handleLogout = () => {
        logout();
    };

    const handleFinishActivity = async (id: any) => {
        Alert.alert(
            "Finalizar Actividad",
            "¿Desea finalizar esta actividad rápidamente?",
            [
                { text: "Cancelar", style: "cancel" },
                { 
                    text: "Finalizar", 
                    onPress: async () => {
                        try {
                            await activityService.finish(id);
                            setActivities((prev: any[]) => prev.map(act =>
                                act.id_actividad === id
                                    ? { ...act, estado: 'Completado', finished: true }
                                    : act
                            ));
                            Alert.alert("¡Éxito!", "Actividad finalizada y PQR cerrada.");
                        } catch (error) {
                            console.error("Error finishing activity", error);
                            Alert.alert("Error", "No se pudo finalizar la actividad.");
                        }
                    }
                }
            ]
        );
    };

    const getCardStyle = (act: any) => {
        const statusStr = (act.estado_actividad_desc || act.estado || '').toLowerCase();
        const isCompleted = statusStr.includes('completado') || statusStr.includes('finaliz') || act.finished;
        if (isCompleted) return { borderLeftColor: '#10b981' };
        return { borderLeftColor: '#f59e0b' }; // priority-high
    };

    const getStatusBadge = (act: any) => {
        const statusStr = (act.estado_actividad_desc || act.estado || '').toLowerCase();
        const isCompleted = statusStr.includes('completad') || statusStr.includes('finaliz') || statusStr.includes('terminad') || statusStr.includes('ejecutad') || act.finished;
        const isInProgress = statusStr.includes('proceso') || statusStr.includes('curso') || !!act.mobile_data?.fch_inicio;

        if (isCompleted) {
            return (
                <View style={[styles.badge, styles.badgeSuccess]}>
                    <Text style={styles.badgeSuccessText}>COMPLETADO</Text>
                </View>
            );
        }
        if (isInProgress) {
            return (
                <View style={[styles.badge, styles.badgeWarning, { backgroundColor: '#e0e7ff', borderColor: '#c7d2fe' }]}>
                    <Text style={[styles.badgeWarningText, { color: '#4338ca' }]}>EN PROCESO</Text>
                </View>
            );
        }
        return (
            <View style={[styles.badge, styles.badgeWarning]}>
                <Text style={styles.badgeWarningText}>PENDIENTE</Text>
            </View>
        );
    };

    return (
        <View style={styles.container}>
            <View style={styles.webWrapper}>
                {/* Header / MobileLayout Ops Header */}
                <View style={styles.header}>
                <View style={styles.userInfo}>
                    <View style={styles.avatarRing}>
                        <View style={styles.avatar}>
                            <Text style={styles.avatarText}>
                                {user?.nombre ? user.nombre.substring(0, 1).toUpperCase() : 'T'}
                            </Text>
                        </View>
                    </View>
                    <View>
                        <Text style={styles.greeting}>Hola, {user?.nombre || 'Técnico'}</Text>
                        <Text style={styles.statusOnline}>🟢 En línea</Text>
                    </View>
                </View>
                <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
                    <Text style={styles.logoutText}>Salir</Text>
                </TouchableOpacity>
            </View>

            {/* Page Title & Filters (Sticky in web, scrollable top here) */}
            <View style={styles.pageHeader}>
                <Text style={styles.pageTitle}>📋 Mis Actividades</Text>
                <View style={styles.segmentedControl}>
                    <TouchableOpacity 
                        style={[styles.segment, filter === 'Pendientes' && styles.segmentActive]}
                        onPress={() => setFilter('Pendientes')}
                    >
                        <Text style={[styles.segmentText, filter === 'Pendientes' && styles.segmentTextActive]}>Pendientes</Text>
                    </TouchableOpacity>
                    <TouchableOpacity 
                        style={[styles.segment, filter === 'Completadas' && styles.segmentActive]}
                        onPress={() => setFilter('Completadas')}
                    >
                        <Text style={[styles.segmentText, filter === 'Completadas' && styles.segmentTextActive]}>Completadas</Text>
                    </TouchableOpacity>
                </View>
            </View>

            {/* Sync Banner */}
            {syncQueueCount > 0 && (
                <View style={styles.syncBanner}>
                    <Feather name="cloud-off" size={24} color="#b45309" style={{ marginTop: 4 }} />
                    <View style={{ flex: 1, paddingLeft: 12 }}>
                        <Text style={styles.syncTitle}>Modo Fuera de Línea</Text>
                        <Text style={styles.syncText}>Tienes {syncQueueCount} actividades pendientes por subir al servidor.</Text>
                    </View>
                    <TouchableOpacity 
                        style={styles.syncBtn} 
                        onPress={handleSync}
                        disabled={syncing}
                    >
                        {syncing ? (
                            <ActivityIndicator size="small" color="#fff" />
                        ) : (
                            <>
                                <Feather name="refresh-cw" size={14} color="#fff" />
                                <Text style={styles.syncBtnText}>Sincronizar</Text>
                            </>
                        )}
                    </TouchableOpacity>
                </View>
            )}

            {/* Activities List */}
            <ScrollView contentContainerStyle={styles.listContainer}>
                {loading ? (
                    <ActivityIndicator size="large" color="#4f46e5" style={{ marginTop: 40 }} />
                ) : activities.length > 0 ? (
                    activities
                    .filter((act) => {
                        const statusStr = (act.estado_actividad_desc || act.estado || '').toLowerCase();
                        const isCompleted = statusStr.includes('completad') || statusStr.includes('finaliz') || statusStr.includes('terminad') || statusStr.includes('ejecutad') || !!act.finished;
                        return filter === 'Completadas' ? isCompleted : !isCompleted;
                    })
                    .map((act) => (
                        <View key={act.id_actividad} style={[styles.card, getCardStyle(act)]}>
                            <View style={styles.cardHeader}>
                                {getStatusBadge(act)}
                                <View style={styles.dateContainer}>
                                    <Feather name="calendar" size={14} color="#94a3b8" />
                                    <Text style={styles.dateText}>
                                        {new Date(act.fch_actividad).toLocaleDateString()}
                                    </Text>
                                </View>
                            </View>

                            <Text style={styles.cardTitle}>{act.tipo_actividad_desc || 'Mantenimiento General'}</Text>

                            {/* PQR Origin Badge */}
                            {act.id_pqr && (
                                <View style={styles.pqrBadge}>
                                    <Feather name="alert-triangle" size={12} color="#e11d48" />
                                    <Text style={styles.pqrBadgeText}>Reporte #{act.id_pqr}</Text>
                                </View>
                            )}

                            <View style={styles.locationContainer}>
                                <Feather name="map-pin" size={14} color="#94a3b8" />
                                <Text style={styles.locationText}>{act.direccion}</Text>
                            </View>

                            <View style={styles.cardFooter}>
                                <Text style={styles.neighborhoodText}>{act.barrio || 'Sin Barrio'}</Text>
                                
                                {/* Action Buttons Logic */}
                                {(() => {
                                    const statusStr = (act.estado_actividad_desc || act.estado || '').toLowerCase();
                                    const isCompleted = statusStr.includes('completad') || statusStr.includes('finaliz') || statusStr.includes('terminad') || statusStr.includes('ejecutad') || act.finished;
                                    const isInProgress = statusStr.includes('proceso') || statusStr.includes('curso') || !!act.mobile_data?.fch_inicio || act.started;

                                    if (isCompleted) {
                                        return (
                                            <TouchableOpacity style={[styles.btnSm, styles.btnSuccess]} disabled>
                                                <Feather name="check-circle" size={14} color="#166534" />
                                                <Text style={styles.btnSuccessText}>Completado</Text>
                                            </TouchableOpacity>
                                        );
                                    } else if (isInProgress) {
                                        return (
                                            <View style={{ flexDirection: 'row', gap: 8 }}>
                                                <TouchableOpacity 
                                                    style={[styles.btnSm, styles.btnWarning]}
                                                    onPress={() => router.push({ pathname: '/manage-activity', params: { id: act.id_actividad } })}
                                                >
                                                    <Feather name="clipboard" size={14} color="#a16207" />
                                                    <Text style={styles.btnWarningText}>Gestionar</Text>
                                                </TouchableOpacity>
                                                
                                                <TouchableOpacity 
                                                    style={[styles.btnSm, { backgroundColor: 'transparent' }]}
                                                    onPress={() => handleFinishActivity(act.id_actividad)}
                                                >
                                                    <Text style={{ color: '#64748b', fontSize: 13, fontWeight: '600' }}>Finalizar</Text>
                                                </TouchableOpacity>
                                            </View>
                                        );
                                    } else {
                                        return (
                                            <TouchableOpacity 
                                                style={[styles.btnSm, styles.btnPrimary]}
                                                onPress={() => handleOpenStartModal(act)}
                                            >
                                                <Text style={styles.btnPrimaryText}>Iniciar</Text>
                                                <Feather name="arrow-right" size={14} color="#fff" />
                                            </TouchableOpacity>
                                        );
                                    }
                                })()}
                            </View>
                        </View>
                    ))
                ) : (
                    <View style={styles.emptyContainer}>
                        <Feather name="info" size={48} color="#cbd5e1" />
                        <Text style={styles.emptyText}>No hay actividades {filter.toLowerCase()} en este momento.</Text>
                    </View>
                )}
            </ScrollView>
            </View>

            {/* Start Activity Modal */}
            <Modal
                animationType="slide"
                transparent={true}
                visible={showStartModal}
                onRequestClose={handleCloseStartModal}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.modalContent}>
                        <View style={styles.modalHeader}>
                            <Text style={styles.modalTitle}>Iniciar Actividad</Text>
                            <TouchableOpacity onPress={handleCloseStartModal} style={styles.closeBtn}>
                                <Feather name="x" size={24} color="#64748b" />
                            </TouchableOpacity>
                        </View>

                        <ScrollView style={styles.modalBody}>
                            {startError ? (
                                <View style={styles.errorAlert}>
                                    <Feather name="alert-circle" size={18} color="#b91c1c" />
                                    <Text style={styles.errorText}>{startError}</Text>
                                </View>
                            ) : null}

                            <View style={styles.activitySummary}>
                                <View style={styles.summaryItem}>
                                    <Text style={styles.summaryLabel}>Tipo</Text>
                                    <Text style={styles.summaryValue}>{selectedActivity?.tipo_actividad_desc || 'Mantenimiento'}</Text>
                                </View>
                                <View style={styles.summaryItem}>
                                    <Text style={styles.summaryLabel}>Dirección</Text>
                                    <Text style={styles.summaryValue}>{selectedActivity?.direccion}</Text>
                                </View>
                            </View>

                            <View style={styles.formGroup}>
                                <Text style={styles.formLabel}>
                                    <Feather name="alert-circle" size={14} /> Observación Inicial
                                </Text>
                                <TextInput
                                    style={styles.textArea}
                                    multiline
                                    numberOfLines={3}
                                    placeholder="Ingrese detalles iniciales..."
                                    value={startFormData.observacion}
                                    onChangeText={(text) => setStartFormData({...startFormData, observacion: text})}
                                />
                            </View>

                            <View style={styles.formGroup}>
                                <Text style={styles.formLabel}>
                                    <Feather name="camera" size={14} /> Registro fotográfico (Antes) <Text style={{color:'red'}}>*</Text>
                                </Text>
                                
                                {startFormData.foto_antes ? (
                                    <View style={styles.imagePreviewContainer}>
                                        <Image source={{ uri: startFormData.foto_antes.uri }} style={styles.imagePreview} />
                                        <TouchableOpacity 
                                            style={styles.removeImageBtn}
                                            onPress={() => setStartFormData({...startFormData, foto_antes: null})}
                                        >
                                            <Feather name="x" size={16} color="#fff" />
                                        </TouchableOpacity>
                                    </View>
                                ) : (
                                    <TouchableOpacity style={styles.cameraBtn} onPress={pickImage}>
                                        <Feather name="camera" size={20} color="#64748b" />
                                        <Text style={styles.cameraBtnText}>Tomar Fotografía</Text>
                                    </TouchableOpacity>
                                )}
                            </View>

                            <View style={styles.formGroup}>
                                <Text style={styles.formLabel}>Ubicación Actual</Text>
                                <View style={styles.locationControl}>
                                    <View style={styles.coordsDisplay}>
                                        {startFormData.latitud ? (
                                            <Text style={styles.coordsText}>
                                                {parseFloat(startFormData.latitud).toFixed(6)}, {parseFloat(startFormData.longitud).toFixed(6)}
                                            </Text>
                                        ) : (
                                            <Text style={styles.coordsPlaceholder}>Sin ubicación</Text>
                                        )}
                                    </View>
                                    <TouchableOpacity 
                                        style={[styles.locationBtn, gettingLocation && { opacity: 0.6 }]} 
                                        onPress={handleLocationClick}
                                        disabled={gettingLocation}
                                    >
                                        {gettingLocation ? (
                                            <ActivityIndicator size="small" color="#fff" />
                                        ) : (
                                            <Feather name="navigation" size={20} color="#fff" />
                                        )}
                                    </TouchableOpacity>
                                </View>
                            </View>
                        </ScrollView>

                        <View style={styles.modalFooter}>
                            <TouchableOpacity style={styles.btnGhost} onPress={handleCloseStartModal}>
                                <Text style={styles.btnGhostText}>Cancelar</Text>
                            </TouchableOpacity>
                            <TouchableOpacity 
                                style={[styles.btnBlock, submitting && { opacity: 0.7 }]} 
                                onPress={confirmStartActivity}
                                disabled={submitting}
                            >
                                {submitting ? (
                                    <ActivityIndicator size="small" color="#fff" />
                                ) : (
                                    <Text style={styles.btnBlockText}>Confirmar Inicio</Text>
                                )}
                            </TouchableOpacity>
                        </View>
                    </View>
                </View>
            </Modal>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8fafc',
    },
    webWrapper: {
        flex: 1,
        width: '100%',
        maxWidth: 600,
        alignSelf: 'center',
        backgroundColor: '#f8fafc',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 0 },
        shadowOpacity: 0.05,
        elevation: 1,
    },
    header: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        paddingHorizontal: 20,
        paddingTop: 50, // SafeArea substitute
        paddingBottom: 16,
        backgroundColor: 'rgba(255, 255, 255, 0.85)',
        borderBottomWidth: 1,
        borderBottomColor: '#e2e8f0',
    },
    userInfo: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12,
    },
    avatarRing: {
        padding: 2,
        borderRadius: 50,
        backgroundColor: '#4f46e5', // Placeholder for gradient
    },
    avatar: {
        width: 40,
        height: 40,
        backgroundColor: '#fff',
        borderRadius: 20,
        alignItems: 'center',
        justifyContent: 'center',
    },
    avatarText: {
        color: '#4f46e5',
        fontWeight: 'bold',
        fontSize: 16,
    },
    greeting: {
        fontSize: 16,
        fontWeight: '700',
        color: '#0f172a',
    },
    statusOnline: {
        fontSize: 12,
        color: '#10b981',
        fontWeight: '500',
    },
    logoutBtn: {
        backgroundColor: 'rgba(239, 68, 68, 0.1)',
        paddingVertical: 8,
        paddingHorizontal: 12,
        borderRadius: 10,
    },
    logoutText: {
        color: '#ef4444',
        fontWeight: '600',
        fontSize: 14,
    },
    pageHeader: {
        padding: 20,
        backgroundColor: '#fff',
        borderBottomWidth: 1,
        borderBottomColor: '#f1f5f9',
    },
    pageTitle: {
        fontSize: 22,
        fontWeight: '800',
        color: '#0f172a',
        marginBottom: 16,
    },
    segmentedControl: {
        flexDirection: 'row',
        backgroundColor: '#f1f5f9',
        borderRadius: 30,
        padding: 4,
    },
    segment: {
        flex: 1,
        paddingVertical: 8,
        alignItems: 'center',
        borderRadius: 30,
    },
    segmentActive: {
        backgroundColor: '#fff',
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 1 },
        shadowOpacity: 0.1,
        elevation: 2,
    },
    segmentText: {
        fontWeight: '600',
        color: '#64748b',
    },
    segmentTextActive: {
        color: '#0f172a',
    },
    syncBanner: {
        flexDirection: 'row',
        backgroundColor: '#fef3c7',
        borderLeftWidth: 4,
        borderLeftColor: '#f59e0b',
        borderBottomWidth: 1,
        borderBottomColor: '#fde68a',
        padding: 16,
        alignItems: 'center',
    },
    syncTitle: {
        fontWeight: 'bold',
        color: '#92400e',
        fontSize: 15,
        marginBottom: 2,
    },
    syncText: {
        color: '#b45309',
        fontSize: 13,
    },
    syncBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#d97706',
        paddingHorizontal: 16,
        paddingVertical: 10,
        borderRadius: 8,
        gap: 6,
        marginLeft: 8,
    },
    syncBtnText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 13,
    },
    listContainer: {
        padding: 20,
        gap: 16,
    },
    card: {
        backgroundColor: '#fff',
        padding: 20,
        borderRadius: 16,
        borderWidth: 1,
        borderColor: '#e2e8f0',
        borderLeftWidth: 4,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.05,
        elevation: 3,
        marginBottom: 16, // RN workaround for gap sometimes
    },
    cardHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 8,
    },
    badge: {
        paddingHorizontal: 10,
        paddingVertical: 4,
        borderRadius: 20,
        borderWidth: 1,
    },
    badgeWarning: {
        backgroundColor: '#fef9c3',
        borderColor: '#fef08a',
    },
    badgeWarningText: {
        color: '#a16207',
        fontSize: 10,
        fontWeight: '700',
    },
    badgeSuccess: {
        backgroundColor: '#dcfce7',
        borderColor: '#bbf7d0',
    },
    badgeSuccessText: {
        color: '#166534',
        fontSize: 10,
        fontWeight: '700',
    },
    dateContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 4,
    },
    dateText: {
        color: '#94a3b8',
        fontSize: 12,
    },
    cardTitle: {
        fontSize: 18,
        fontWeight: '600',
        color: '#0f172a',
        marginBottom: 8,
    },
    pqrBadge: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
        backgroundColor: '#fff1f2',
        borderWidth: 1,
        borderColor: '#ffe4e6',
        paddingHorizontal: 10,
        paddingVertical: 4,
        borderRadius: 20,
        alignSelf: 'flex-start',
        marginBottom: 8,
    },
    pqrBadgeText: {
        color: '#e11d48',
        fontSize: 12,
        fontWeight: '600',
    },
    locationContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
        marginBottom: 16,
    },
    locationText: {
        color: '#64748b',
        fontSize: 13,
    },
    cardFooter: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        borderTopWidth: 1,
        borderTopColor: '#f1f5f9',
        paddingTop: 16,
    },
    neighborhoodText: {
        color: '#94a3b8',
        fontSize: 13,
        fontWeight: '500',
    },
    btnSm: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 6,
        paddingHorizontal: 16,
        paddingVertical: 8,
        borderRadius: 30,
    },
    btnPrimary: {
        backgroundColor: '#4f46e5',
        shadowColor: '#4f46e5',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        elevation: 4,
    },
    btnPrimaryText: {
        color: '#fff',
        fontWeight: '600',
        fontSize: 13,
    },
    btnSuccess: {
        backgroundColor: '#dcfce7',
        borderWidth: 1,
        borderColor: '#bbf7d0',
    },
    btnSuccessText: {
        color: '#166534',
        fontWeight: '600',
        fontSize: 13,
    },
    btnWarning: {
        backgroundColor: '#fef9c3',
        borderWidth: 1,
        borderColor: '#fef08a',
    },
    btnWarningText: {
        color: '#a16207',
        fontWeight: '600',
        fontSize: 13,
    },
    emptyContainer: {
        alignItems: 'center',
        justifyContent: 'center',
        marginTop: 60,
        gap: 12,
    },
    emptyText: {
        textAlign: 'center',
        color: '#94a3b8',
        fontSize: 16,
        fontWeight: '500',
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(0,0,0,0.5)',
        justifyContent: 'center',
        padding: 20,
    },
    modalContent: {
        backgroundColor: '#fff',
        borderRadius: 16,
        maxHeight: '80%',
        width: '100%',
        maxWidth: 500,
        alignSelf: 'center',
        overflow: 'hidden',
    },
    modalHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#f1f5f9',
    },
    modalTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#0f172a',
    },
    closeBtn: {
        padding: 4,
    },
    modalBody: {
        padding: 16,
    },
    errorAlert: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#fef2f2',
        padding: 12,
        borderRadius: 8,
        marginBottom: 16,
        gap: 8,
    },
    errorText: {
        color: '#b91c1c',
        fontWeight: '500',
        fontSize: 13,
        flex: 1,
    },
    activitySummary: {
        backgroundColor: '#f8fafc',
        padding: 12,
        borderRadius: 8,
        marginBottom: 16,
        gap: 8,
    },
    summaryItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
    },
    summaryLabel: {
        color: '#64748b',
        fontSize: 13,
    },
    summaryValue: {
        color: '#0f172a',
        fontWeight: '500',
        fontSize: 13,
    },
    formGroup: {
        marginBottom: 16,
    },
    formLabel: {
        fontWeight: '600',
        color: '#334155',
        marginBottom: 8,
        fontSize: 14,
    },
    textArea: {
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#cbd5e1',
        borderRadius: 8,
        padding: 12,
        minHeight: 80,
        textAlignVertical: 'top',
    },
    cameraBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 8,
        padding: 16,
        backgroundColor: '#f1f5f9',
        borderWidth: 2,
        borderColor: '#cbd5e1',
        borderStyle: 'dashed',
        borderRadius: 8,
    },
    cameraBtnText: {
        color: '#64748b',
        fontWeight: '600',
    },
    imagePreviewContainer: {
        position: 'relative',
        borderRadius: 8,
        overflow: 'hidden',
    },
    imagePreview: {
        width: '100%',
        height: 200,
        resizeMode: 'cover',
    },
    removeImageBtn: {
        position: 'absolute',
        top: 8,
        right: 8,
        backgroundColor: 'rgba(239, 68, 68, 0.9)',
        borderRadius: 20,
        padding: 4,
    },
    locationControl: {
        flexDirection: 'row',
        gap: 8,
    },
    coordsDisplay: {
        flex: 1,
        backgroundColor: '#f1f5f9',
        borderWidth: 1,
        borderColor: '#cbd5e1',
        borderRadius: 8,
        paddingHorizontal: 12,
        justifyContent: 'center',
    },
    coordsText: {
        color: '#334155',
        fontFamily: 'monospace',
    },
    coordsPlaceholder: {
        color: '#94a3b8',
    },
    locationBtn: {
        backgroundColor: '#4f46e5',
        width: 48,
        height: 48,
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
    },
    modalFooter: {
        flexDirection: 'row',
        justifyContent: 'flex-end',
        padding: 16,
        borderTopWidth: 1,
        borderTopColor: '#f1f5f9',
        gap: 8,
    },
    btnGhost: {
        paddingVertical: 10,
        paddingHorizontal: 16,
        borderRadius: 8,
    },
    btnGhostText: {
        color: '#64748b',
        fontWeight: '600',
    },
    btnBlock: {
        backgroundColor: '#4f46e5',
        paddingVertical: 10,
        paddingHorizontal: 16,
        borderRadius: 8,
        flex: 1,
        alignItems: 'center',
    },
    btnBlockText: {
        color: '#fff',
        fontWeight: '600',
    }
});
