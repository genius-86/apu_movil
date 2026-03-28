import React, { useState, useEffect, useRef } from 'react';
import { View, Text, TextInput, TouchableOpacity, ScrollView, StyleSheet, ActivityIndicator, Alert, Image, KeyboardAvoidingView, Platform, Modal } from 'react-native';
import { useLocalSearchParams, useRouter } from 'expo-router';
import { useAuth } from '../src/context/AuthContext';
import { activityService, masterService, pqrService } from '../src/services/api';
import { syncService } from '../src/services/SyncService';
import { Feather, FontAwesome5 } from '@expo/vector-icons';
import * as ImagePicker from 'expo-image-picker';
import SignatureScreen, { SignatureViewRef } from 'react-native-signature-canvas';
import { APP_CONSTANTS } from '../src/constants/AppConstants';

// --- COMPONENTE DE FIRMA PARA WEB (FALLBACK) ---
const WebSignature = React.forwardRef(({ onOK, onEmpty }: any, ref: any) => {
    const canvasRef = useRef<any>(null);
    const [isDrawing, setIsDrawing] = useState(false);

    React.useImperativeHandle(ref, () => ({
        readSignature: () => {
            if (canvasRef.current) {
                const dataUrl = canvasRef.current.toDataURL();
                onOK(dataUrl);
            }
        },
        clearSignature: () => {
            if (canvasRef.current) {
                const ctx = canvasRef.current.getContext('2d');
                ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
                onEmpty();
            }
        }
    }));

    useEffect(() => {
        if (Platform.OS !== 'web' || !canvasRef.current) return;
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        ctx.strokeStyle = '#000';
        ctx.lineWidth = 2;
        ctx.lineCap = 'round';

        const getPos = (e: any) => {
            const rect = canvas.getBoundingClientRect();
            const clientX = e.touches ? e.touches[0].clientX : e.clientX;
            const clientY = e.touches ? e.touches[0].clientY : e.clientY;
            return { x: clientX - rect.left, y: clientY - rect.top };
        };

        const start = (e: any) => {
            setIsDrawing(true);
            const { x, y } = getPos(e);
            ctx.beginPath();
            ctx.moveTo(x, y);
        };

        const move = (e: any) => {
            if (!isDrawing) return;
            const { x, y } = getPos(e);
            ctx.lineTo(x, y);
            ctx.stroke();
            e.preventDefault();
        };

        const stop = () => setIsDrawing(false);

        canvas.addEventListener('mousedown', start);
        canvas.addEventListener('mousemove', move);
        window.addEventListener('mouseup', stop);
        canvas.addEventListener('touchstart', start, { passive: false });
        canvas.addEventListener('touchmove', move, { passive: false });
        canvas.addEventListener('touchend', stop);

        return () => {
            canvas.removeEventListener('mousedown', start);
            canvas.removeEventListener('mousemove', move);
            window.removeEventListener('mouseup', stop);
            canvas.removeEventListener('touchstart', start);
            canvas.removeEventListener('touchmove', move);
            canvas.removeEventListener('touchend', stop);
        };
    }, [isDrawing]);

    return (
        <View style={{ flex: 1, backgroundColor: '#fff' }}>
            <canvas 
                ref={canvasRef} 
                width={500} 
                height={200} 
                style={{ width: '100%', height: '100%', touchAction: 'none' }} 
            />
        </View>
    );
});

export default function ManageActivityScreen() {
    const { id } = useLocalSearchParams();
    const router = useRouter();
    const { user } = useAuth() as any;

    const [loading, setLoading] = useState(true);
    const [submitting, setSubmitting] = useState(false);
    const [formError, setFormError] = useState('');
    const [activeTab, setActiveTab] = useState('pqr'); // pqr, punto, ejecucion, materiales
    const [currentTime, setCurrentTime] = useState(new Date());
    const [pickerModal, setPickerModal] = useState<any>({ visible: false, title: '', options: [], onSelect: null, selectedValue: '' });
    const signatureRef = useRef<SignatureViewRef>(null);

    useEffect(() => {
        const timer = setInterval(() => setCurrentTime(new Date()), 1000);
        return () => clearInterval(timer);
    }, []);

    const addMaterialRow = () => {
        setFormData((prev: any) => ({
            ...prev,
            materiales: [...prev.materiales, { 
                id_articulo: '', 
                cantidad: '', 
                id_unidad_medida: '', 
                tipo: APP_CONSTANTS.MATERIAL_TYPES[0].value, 
                serial: '' 
            }]
        }));
    };

    const removeMaterialRow = (index: number) => {
        setFormData((prev: any) => {
            const newMat = [...prev.materiales];
            newMat.splice(index, 1);
            return { ...prev, materiales: newMat };
        });
    };

    const handleMaterialChange = (index: number, field: string, value: any) => {
        setFormData((prev: any) => {
            const newMat = [...prev.materiales];
            newMat[index] = { ...newMat[index], [field]: value };
            
            if (field === 'id_articulo') {
                const art = params.articulos.find((a: any) => a.id_articulo == value);
                if (art) newMat[index].articulo_desc = art.descripcion;
            }
            
            return { ...prev, materiales: newMat };
        });
    };

    const openPicker = (title: string, data: any[], valueKey: string, labelFn: any, selectedValue: any, onSelect: any) => {
        if (!data || !Array.isArray(data)) return;
        const options = data.map((item: any) => {
            let label = 'Sin descripción';
            try {
                label = labelFn(item) || 'Sin descripción';
            } catch (e) {
                label = item[valueKey]?.toString() || 'Opción';
            }
            return { value: item[valueKey], label: label.toString() };
        });
        setPickerModal({ visible: true, title, options, selectedValue, onSelect });
    };

    const [searchingPqr, setSearchingPqr] = useState(false);
    const [searchingLuminaria, setSearchingLuminaria] = useState(false);

    const [params, setParams] = useState<any>({
        vehiculos: [] as any[],
        estados_actividad: [] as any[],
        unidades_medida: [] as any[],
        tipos_actividad: [] as any[],
        articulos: [] as any[],
        barrios: [] as any[]
    });

    const [formData, setFormData] = useState<any>({
        id_actividad: id,
        id_pqr: null,
        pqr_no: '',
        fch_pqr: '',
        tipo_pqr: '',
        tipo_reporte: '',

        id_luminaria: null,
        poste_no: '',
        tipo_luminaria: '',

        id_tipo_actividad: '',
        id_vehiculo: '',
        id_estado_actividad: '',
        fch_ejecucion_actividad: new Date().toISOString().split('T')[0],
        hora_ejecucion_actividad: new Date().toTimeString().split(' ')[0],
        id_municipio: '',
        id_barrio: '',
        direccion: '',
        observacion: '',
        cerrar_pqr: false,

        materiales: [],
        foto_despues: null,
        firma_tecnico: null
    });

    useEffect(() => {
        if (id) {
            fetchData();
        }
    }, [id]);

    const fetchData = async () => {
        setLoading(true);
        try {
            const [paramsRes, activityRes] = await Promise.all([
                masterService.getParameters(),
                activityService.detail(id as string)
            ]);

            setParams(paramsRes.data);
            const act = activityRes.data;

            setFormData((prev: any) => ({
                ...prev,
                ...act,
                pqr_no: act.id_pqr?.id_pqr || '',
                fch_pqr: act.id_pqr?.fch_pqr || '',
                tipo_pqr: act.id_pqr?.tipo_pqr_desc || '',
                tipo_reporte: act.id_pqr?.tipo_reporte_desc || '',

                poste_no: act.id_luminaria?.poste_no || '',
                tipo_luminaria: act.id_luminaria?.tipo_luminaria_desc || '',
                
                materiales: act.materiales || []
            }));
        } catch (error) {
            console.error("Error fetching activity data", error);
            Alert.alert("Error", "No se pudo cargar la información de la actividad");
        } finally {
            setLoading(false);
        }
    };

    const handlePqrSearch = async () => {
        setFormError('');
        if (!formData.pqr_no) {
            setFormError("Ingrese un número de PQR para buscar.");
            setTimeout(() => setFormError(''), 4000);
            return;
        }

        setSearchingPqr(true);
        try {
            const response = await pqrService.detail(formData.pqr_no);
            const pqr = response.data;
            setFormData((prev: any) => ({
                ...prev,
                id_pqr: pqr.id_pqr,
                pqr_no: pqr.id_pqr.toString(),
                fch_pqr: pqr.fch_pqr,
                tipo_pqr: pqr.tipo_pqr_desc || '',
                tipo_reporte: pqr.tipo_reporte_desc || '',
                id_luminaria: pqr.id_luminaria || prev.id_luminaria,
                poste_no: pqr.poste_no || prev.poste_no,
                tipo_luminaria: pqr.tipo_luminaria_desc || prev.tipo_luminaria,
                direccion: pqr.direccion_reporte || prev.direccion
            }));
        } catch (error) {
            setFormError("No se encontró la PQR especificada.");
            setTimeout(() => setFormError(''), 4000);
        } finally {
            setSearchingPqr(false);
        }
    };

    const handleLuminariaSearch = async () => {
        setFormError('');
        if (!formData.poste_no) {
            setFormError("Ingrese un número de poste para buscar.");
            setTimeout(() => setFormError(''), 4000);
            return;
        }

        setSearchingLuminaria(true);
        try {
            const response = await masterService.getLuminarias({ poste_no: formData.poste_no });
            const luminarias = response.data.results || response.data;

            if (luminarias.length > 0) {
                const lum = luminarias[0];
                setFormData((prev: any) => ({
                    ...prev,
                    id_luminaria: lum.id_luminaria,
                    poste_no: lum.poste_no,
                    tipo_luminaria: lum.tipo_luminaria_desc,
                    direccion: lum.direccion || prev.direccion,
                    id_municipio: lum.id_municipio || prev.id_municipio,
                    id_barrio: lum.id_barrio || prev.id_barrio
                }));
            } else {
                setFormError("No se encontró ninguna luminaria con ese número de poste.");
                setTimeout(() => setFormError(''), 4000);
            }
        } finally {
            setSearchingLuminaria(false);
        }
    };

    const isTabComplete = (tabId: string) => {
        if (tabId === 'pqr') return !!formData.id_pqr;
        if (tabId === 'punto') return !!formData.id_luminaria;
        if (tabId === 'ejecucion') return !!(formData.id_tipo_actividad && formData.id_vehiculo && formData.id_estado_actividad);
        if (tabId === 'materiales') return formData.materiales && formData.materiales.length > 0;
        return false;
    };

    const isTabLocked = (tabId: string) => {
        // Si la actividad ya existe (ID presente), permitir navegación libre
        if (id) return false;
        
        if (tabId === 'pqr') return false;
        if (tabId === 'punto') return !isTabComplete('pqr');
        if (tabId === 'ejecucion') return !isTabComplete('punto');
        if (tabId === 'materiales') return !isTabComplete('ejecucion');
        return false;
    };

    const handleTabClick = (tabId: string) => {
        setFormError('');
        if (isTabLocked(tabId)) {
            let message = "Pestaña bloqueada:";
            if (tabId === 'punto') message = "Debe buscar y seleccionar una PQR primero.";
            if (tabId === 'ejecucion') message = "Debe buscar y seleccionar el Punto Lumínico primero.";
            if (tabId === 'materiales') message = "Debe completar Vehículo, Tipo de Actividad y Estado primero.";
            setFormError(message);
            setTimeout(() => setFormError(''), 4000);
            return;
        }
        setActiveTab(tabId);
    };

    const pickFinalImage = async () => {
        try {
            const { status } = await ImagePicker.requestCameraPermissionsAsync();
            if (status !== 'granted') {
                Alert.alert('Permiso Denegado', 'Se requieren permisos de cámara.');
                return;
            }

            let result = await ImagePicker.launchCameraAsync({
                mediaTypes: ImagePicker.MediaTypeOptions.Images,
                allowsEditing: false,
                quality: 0.7,
            });

            if (!result.canceled) {
                setFormData((prev: any) => ({ ...prev, foto_despues: result.assets[0] }));
            }
        } catch (error) {
            Alert.alert("Error", "No se pudo abrir la cámara");
        }
    };

    const handleSignature = (signature: string) => {
        setFormData((prev: any) => ({ ...prev, firma_tecnico: signature }));
    };

    const handleClearSignature = () => {
        signatureRef.current?.clearSignature();
        setFormData((prev: any) => ({ ...prev, firma_tecnico: null }));
    };

    const handleSubmit = async () => {
        setFormError('');

        if (!formData.foto_despues) {
            setFormError(APP_CONSTANTS.MESSAGES.REQUIRED_PHOTO);
            setTimeout(() => setFormError(''), 4000);
            return;
        }

        if (!formData.firma_tecnico) {
            setFormError(APP_CONSTANTS.MESSAGES.REQUIRED_SIGNATURE);
            setTimeout(() => setFormError(''), 4000);
            return;
        }

        setSubmitting(true);
        
        // Limpiar datos para el backend (evitar enviar objetos de imagen o campos inexistentes)
        const cleanData = { ...formData };
        delete cleanData.foto_antes;
        delete cleanData.foto_despues;
        delete cleanData.materiales_pendientes; // Campo auxiliar si existe
        
        // Asegurar que materiales solo envíen lo necesario
        if (cleanData.materiales) {
            cleanData.materiales = cleanData.materiales.map((m: any) => ({
                id_articulo: m.id_articulo,
                id_unidad_medida: m.id_unidad_medida,
                cantidad: m.cantidad,
                tipo: m.tipo,
                serial: m.serial
            }));
        }

        try {
            await activityService.save(cleanData);
            
            // Llamar al endpoint finish para "cerrar" la actividad en el backend
            try {
                const finishRes = await activityService.finish(id as string);
                console.log("Finish result:", finishRes.data);
            } catch (finishErr) {
                console.error("Error calling finish endpoint:", finishErr);
                // No detenemos el flujo si el save funcionó pero el finish falló
            }

            if (formData.foto_despues) {
                const photoData = new FormData();
                photoData.append('foto', {
                    uri: formData.foto_despues.uri,
                    name: `despues_${id}.jpg`,
                    type: 'image/jpeg'
                } as any);
                photoData.append('tipo', 'DESPUES');
                try {
                    await activityService.addPhoto(id as string, photoData);
                } catch (photoErr) {
                    console.error("Error subiendo foto final", photoErr);
                }
            }

            if (Platform.OS === 'web') {
                router.replace('/activities');
            } else {
                Alert.alert("¡Éxito!", APP_CONSTANTS.MESSAGES.SAVE_SUCCESS, [
                    { text: "OK", onPress: () => router.replace('/activities') }
                ]);
            }
        } catch (error: any) {
            const isNetworkError = error.message === 'Network Error' || error.message?.includes('Network Error') || error.code === 'ERR_NETWORK';
            
            if (isNetworkError) {
                console.log("Network error saving activity. Queueing offline.");
                try {
                    await syncService.addToQueue(cleanData, formData.foto_despues);
                    Alert.alert(
                        APP_CONSTANTS.MESSAGES.OFFLINE_MODE, 
                        APP_CONSTANTS.MESSAGES.OFFLINE_SAVED, 
                        [{ text: "OK", onPress: () => router.replace('/activities') }]
                    );
                    return; // Terminamos sin ejecutar finally inmediatamente
                } catch (queueErr) {
                    Alert.alert(APP_CONSTANTS.MESSAGES.CRITICAL_ERROR, APP_CONSTANTS.MESSAGES.QUEUE_ERROR);
                }
            } else {
                console.error("Error saving activity:", error.response?.data || error.message);
                const msg = error.response?.data 
                    ? JSON.stringify(error.response.data) 
                    : "No se pudo guardar la actividad. Verifique los datos.";
                Alert.alert("Error de Guardado", msg);
            }
        } finally {
            setSubmitting(false);
        }
    };

    const renderTabHeader = () => {
        const tabs = [
            { id: 'pqr', label: 'Reporte', icon: 'clipboard-list' },
            { id: 'punto', label: 'Punto', icon: 'lightbulb' },
            { id: 'ejecucion', label: 'Ejecución', icon: 'truck' },
            { id: 'materiales', label: 'Materiales', icon: 'box' }
        ];

        return (
            <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.tabContainer} contentContainerStyle={{ paddingHorizontal: 16, gap: 8 }}>
                {tabs.map(tab => {
                    const locked = isTabLocked(tab.id);
                    const complete = isTabComplete(tab.id);
                    const active = activeTab === tab.id;

                    return (
                        <TouchableOpacity
                            key={tab.id}
                            style={[
                                styles.tabBtn,
                                active && styles.tabActive,
                                complete && !active && styles.tabComplete,
                                locked && styles.tabLocked
                            ]}
                            onPress={() => handleTabClick(tab.id)}
                            disabled={locked}
                        >
                            <FontAwesome5 
                                name={locked ? 'lock' : complete && !active ? 'check-circle' : tab.icon} 
                                size={14} 
                                color={active ? '#fff' : complete && !active ? '#10b981' : locked ? '#94a3b8' : '#64748b'} 
                            />
                            <Text style={[
                                styles.tabText,
                                active && styles.tabTextActive,
                                complete && !active && styles.tabTextComplete,
                                locked && styles.tabTextLocked
                            ]}>
                                {tab.label}
                            </Text>
                        </TouchableOpacity>
                    );
                })}
            </ScrollView>
        );
    };

    if (loading) {
        return (
            <View style={styles.loadingContainer}>
                <ActivityIndicator size="large" color="#4f46e5" />
                <Text style={styles.loadingText}>Cargando datos...</Text>
            </View>
        );
    }

    return (
        <KeyboardAvoidingView 
            style={styles.container} 
            behavior={Platform.OS === "ios" ? "padding" : undefined}
            keyboardVerticalOffset={Platform.OS === "ios" ? 100 : 0}
        >
            <View style={styles.header}>
                <TouchableOpacity style={styles.backBtn} onPress={() => router.back()}>
                    <Feather name="arrow-left" size={24} color="#0f172a" />
                </TouchableOpacity>
                <View style={styles.headerTitleContainer}>
                    <Text style={styles.headerTitle}>Gestionar Actividad</Text>
                    <Text style={styles.headerSubtitle}>ID: {id}</Text>
                </View>
            </View>

            {formError ? (
                <View style={styles.errorAlert}>
                    <Feather name="alert-circle" size={18} color="#ef4444" />
                    <Text style={styles.errorText}>{formError}</Text>
                </View>
            ) : null}

            <View style={styles.tabBarWrapper}>
                {renderTabHeader()}
            </View>
            
            <ScrollView 
                style={styles.container} 
                contentContainerStyle={styles.scrollContent}
                keyboardShouldPersistTaps="handled"
            >                
                {activeTab === 'pqr' && (
                    <View style={styles.card}>
                        <Text style={styles.sectionTitle}><FontAwesome5 name="clipboard-list" /> Datos de la PQR</Text>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>PQR / Reporte No.</Text>
                            <View style={styles.searchRow}>
                                <TextInput
                                    style={styles.searchInput}
                                    value={formData.pqr_no}
                                    onChangeText={(t: string) => setFormData((p: any) => ({...p, pqr_no: t}))}
                                    placeholder="N° de PQR"
                                />
                                <TouchableOpacity style={styles.searchBtn} onPress={handlePqrSearch} disabled={searchingPqr}>
                                    {searchingPqr ? <ActivityIndicator size="small" color="#fff" /> : <Feather name="search" size={18} color="#fff" />}
                                </TouchableOpacity>
                            </View>
                        </View>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Fecha PQR</Text>
                            <TextInput style={styles.inputReadOnly} value={formData.fch_pqr} editable={false} />
                        </View>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Tipo PQR</Text>
                            <TextInput style={styles.inputReadOnly} value={formData.tipo_pqr} editable={false} />
                        </View>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Dirección</Text>
                            <TextInput style={styles.inputReadOnly} value={formData.direccion} editable={false} />
                        </View>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Barrio</Text>
                            <TextInput style={styles.inputReadOnly} value={params.barrios.find((b: any) => b.id_barrio === formData.id_barrio)?.descripcion || ''} editable={false} />
                        </View>
                    </View>
                )}

                {activeTab === 'punto' && (
                    <View style={styles.card}>
                        <Text style={[styles.sectionTitle, {color: '#0284c7'}]}><FontAwesome5 name="lightbulb" /> Punto Lumínico</Text>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Poste No.</Text>
                            <View style={styles.searchRow}>
                                <TextInput
                                    style={styles.searchInput}
                                    value={formData.poste_no}
                                    onChangeText={(t: string) => setFormData((p: any) => ({...p, poste_no: t}))}
                                    placeholder="N° de Poste"
                                />
                                <TouchableOpacity style={[styles.searchBtn, {backgroundColor: '#0284c7'}]} onPress={handleLuminariaSearch} disabled={searchingLuminaria}>
                                    {searchingLuminaria ? <ActivityIndicator size="small" color="#fff" /> : <Feather name="search" size={18} color="#fff" />}
                                </TouchableOpacity>
                            </View>
                        </View>
                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Tipo Luminaria</Text>
                            <TextInput style={styles.inputReadOnly} value={formData.tipo_luminaria} editable={false} />
                        </View>
                    </View>
                )}

                {activeTab === 'ejecucion' && (
                    <View style={styles.card}>
                        <Text style={[styles.sectionTitle, { color: '#4f46e5' }]}><FontAwesome5 name="clipboard-list" /> Datos de la Actividad</Text>
                        
                        <View style={styles.formGroup}>
                            <Text style={styles.label}><FontAwesome5 name="clipboard-list" /> TIPO DE ACTIVIDAD *</Text>
                            <TouchableOpacity 
                                style={styles.selectBtn} 
                                onPress={() => openPicker('Tipo Actividad', params.tipos_actividad, 'id_tipo_actividad', (i:any) => i.descripcion || 'Sin descripción', formData.id_tipo_actividad, (val:any) => setFormData((p:any) => ({...p, id_tipo_actividad: val})))}
                            >
                                <Text style={formData.id_tipo_actividad ? styles.selectText : styles.selectPlaceholder}>
                                    {params.tipos_actividad.find((t:any) => t.id_tipo_actividad === formData.id_tipo_actividad)?.descripcion || '- Seleccione el tipo de trabajo -'}
                                </Text>
                                <Feather name="chevron-down" size={18} color="#64748b" />
                            </TouchableOpacity>
                        </View>

                        <View style={styles.formGrid2}>
                            <View style={[styles.formGroup, {flex:1}]}>
                                <Text style={styles.label}><FontAwesome5 name="truck" /> Vehículo *</Text>
                                <TouchableOpacity 
                                    style={styles.selectBtn} 
                                    onPress={() => openPicker('Vehículo', params.vehiculos, 'id_vehiculo', (i:any) => i.placa ? `${i.placa} (${i.descripcion || ''})` : i.descripcion || 'Sin placa', formData.id_vehiculo, (val:any) => setFormData((p:any) => ({...p, id_vehiculo: val})))}
                                >
                                    <Text style={formData.id_vehiculo ? styles.selectText : styles.selectPlaceholder} numberOfLines={1}>
                                        {params.vehiculos.find((v:any) => v.id_vehiculo === formData.id_vehiculo) 
                                            ? `${params.vehiculos.find((v:any) => v.id_vehiculo === formData.id_vehiculo)?.placa || params.vehiculos.find((v:any) => v.id_vehiculo === formData.id_vehiculo)?.descripcion || 'Vehículo'}` 
                                            : '- Seleccione -'}
                                    </Text>
                                    <Feather name="chevron-down" size={18} color="#64748b" />
                                </TouchableOpacity>
                            </View>
                            <View style={[styles.formGroup, {flex: 1}]}>
                                <Text style={styles.label}><FontAwesome5 name="check-circle" /> Estado *</Text>
                                <TouchableOpacity 
                                    style={styles.selectBtn} 
                                    onPress={() => openPicker('Estado', params.estados_actividad, 'id_estado_actividad', (i:any) => i.descripcion || 'Sin descripción', formData.id_estado_actividad, (val:any) => setFormData((p:any) => ({...p, id_estado_actividad: val})))}
                                >
                                    <Text style={formData.id_estado_actividad ? styles.selectText : styles.selectPlaceholder} numberOfLines={1}>
                                        {params.estados_actividad.find((e:any) => e.id_estado_actividad === formData.id_estado_actividad)?.descripcion || '- Seleccione -'}
                                    </Text>
                                    <Feather name="chevron-down" size={18} color="#64748b" />
                                </TouchableOpacity>
                            </View>
                        </View>

                        <View style={styles.formGrid2}>
                            <View style={[styles.formGroup, {flex:1}]}>
                                <Text style={styles.label}><FontAwesome5 name="calendar" /> Fecha Ejecución</Text>
                                <TextInput style={styles.inputReadOnly} value={formData.fch_ejecucion_actividad || new Date().toISOString().split('T')[0]} editable={false} />
                            </View>
                            <View style={[styles.formGroup, {flex:1}]}>
                                <Text style={styles.label}><FontAwesome5 name="clock" /> Hora Ejecución</Text>
                                <TextInput style={styles.inputReadOnly} value={formData.hora_ejecucion_actividad || new Date().toLocaleTimeString()} editable={false} />
                            </View>
                        </View>

                        <View style={styles.formGrid2}>
                            <View style={[styles.formGroup, {flex:1}]}>
                                <Text style={styles.label}><FontAwesome5 name="clock" /> Hora Inicio</Text>
                                <TextInput style={styles.inputReadOnly} value={formData.mobile_data?.fch_inicio ? new Date(formData.mobile_data.fch_inicio).toLocaleTimeString() : 'No iniciada'} editable={false} />
                            </View>
                            <View style={[styles.formGroup, {flex:1}]}>
                                <Text style={[styles.label, {color: '#4f46e5'}]}><FontAwesome5 name="clock" /> Hora Fin (Actual)</Text>
                                <TextInput style={[styles.inputReadOnly, {borderColor: '#c7d2fe', backgroundColor: '#e0e7ff', color: '#3730a3', fontWeight: 'bold'}]} value={currentTime.toLocaleTimeString()} editable={false} />
                            </View>
                        </View>

                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Observación</Text>
                            <TextInput
                                style={[styles.input, { height: 80, textAlignVertical: 'top' }]}
                                multiline
                                value={formData.observacion}
                                onChangeText={(t: string) => setFormData((p:any) => ({...p, observacion: t}))}
                                placeholder="Detalle los trabajos realizados..."
                            />
                        </View>
                        
                        <TouchableOpacity 
                            style={styles.checkboxRow}
                            onPress={() => setFormData((p:any) => ({...p, cerrar_pqr: !p.cerrar_pqr}))}
                        >
                            <View style={[styles.checkbox, formData.cerrar_pqr && styles.checkboxActive]}>
                                {formData.cerrar_pqr && <Feather name="check" size={14} color="#fff" />}
                            </View>
                            <Text style={styles.checkboxLabel}>Cerrar PQR asociada después de guardar</Text>
                        </TouchableOpacity>
                    </View>
                )}

                {activeTab === 'materiales' && (
                    <View style={styles.card}>
                        <View style={styles.sectionHeader}>
                            <Text style={[styles.sectionTitle, { color: '#10b981', marginBottom: 0 }]}><FontAwesome5 name="package" /> Materiales / Servicios</Text>
                            <TouchableOpacity style={styles.btnAdd} onPress={addMaterialRow}>
                                <Feather name="plus" size={16} color="#fff" />
                                <Text style={styles.btnAddText}>Agregar</Text>
                            </TouchableOpacity>
                        </View>

                        <View style={styles.materialsList}>
                            {formData.materiales.map((mat: any, index: number) => (
                                <View key={index} style={styles.materialItem}>
                                    <TouchableOpacity 
                                        style={styles.btnRemove} 
                                        onPress={() => removeMaterialRow(index)}
                                    >
                                        <Feather name="trash-2" size={18} color="#ef4444" />
                                    </TouchableOpacity>

                                    <View style={styles.formGroup}>
                                        <Text style={styles.label}>Artículo / Material</Text>
                                        <TouchableOpacity 
                                            style={styles.selectBtn} 
                                            onPress={() => openPicker('Artículo', params.articulos, 'id_articulo', (i:any) => i.descripcion || 'Sin descripción', mat.id_articulo, (val:any) => handleMaterialChange(index, 'id_articulo', val))}
                                        >
                                            <Text style={mat.id_articulo ? styles.selectText : styles.selectPlaceholder} numberOfLines={1}>
                                                {params.articulos.find((a:any) => a.id_articulo == mat.id_articulo)?.descripcion || '- Seleccione -'}
                                            </Text>
                                            <Feather name="chevron-down" size={18} color="#64748b" />
                                        </TouchableOpacity>
                                    </View>

                                    <View style={styles.formGrid2}>
                                        <View style={[styles.formGroup, {flex:1}]}>
                                            <Text style={styles.label}>Cantidad</Text>
                                            <TextInput 
                                                style={styles.input} 
                                                keyboardType="numeric" 
                                                value={mat.cantidad.toString()} 
                                                onChangeText={(t: string) => handleMaterialChange(index, 'cantidad', t)} 
                                            />
                                        </View>
                                        <View style={[styles.formGroup, {flex: 1}]}>
                                            <Text style={styles.label}>Und. Medida</Text>
                                            <TouchableOpacity 
                                                style={styles.selectBtn} 
                                                onPress={() => openPicker('Unidad', params.unidades_medida, 'id_unitario', (i:any) => i.abreviatura || i.descripcion || 'Unidad', mat.id_unidad_medida, (val:any) => handleMaterialChange(index, 'id_unidad_medida', val))}
                                            >
                                                <Text style={mat.id_unidad_medida ? styles.selectText : styles.selectPlaceholder}>
                                                    {params.unidades_medida.find((u:any) => u.id_unitario == mat.id_unidad_medida)?.abreviatura || '- Sel -'}
                                                </Text>
                                                <Feather name="chevron-down" size={18} color="#64748b" />
                                            </TouchableOpacity>
                                        </View>
                                    </View>

                                    <View style={styles.formGrid2}>
                                        <View style={[styles.formGroup, {flex:1}]}>
                                            <Text style={styles.label}>Serial (Opcional)</Text>
                                            <TextInput 
                                                style={styles.input} 
                                                value={mat.serial || ''} 
                                                onChangeText={(t: string) => handleMaterialChange(index, 'serial', t)}
                                                placeholder="Ej. SN-123"
                                            />
                                        </View>
                                        <View style={[styles.formGroup, {flex: 1}]}>
                                            <Text style={styles.label}>Tipo</Text>
                                            <TouchableOpacity 
                                                style={styles.selectBtn} 
                                                onPress={() => openPicker('Tipo', APP_CONSTANTS.MATERIAL_TYPES, 'value', (i:any) => i.label, mat.tipo, (val:any) => handleMaterialChange(index, 'tipo', val))}
                                            >
                                                <Text style={styles.selectText}>{APP_CONSTANTS.MATERIAL_TYPES.find((t:any) => t.value === mat.tipo)?.label || 'Instalado'}</Text>
                                                <Feather name="chevron-down" size={18} color="#64748b" />
                                            </TouchableOpacity>
                                        </View>
                                    </View>
                                </View>
                            ))}

                            {formData.materiales.length === 0 && (
                                <View style={styles.emptyState}>
                                    <Text style={styles.emptyStateText}>No se han agregado materiales.</Text>
                                </View>
                            )}
                        </View>
                        
                        {/* Registro Fotográfico Final */}
                        <View style={[styles.divider, { marginTop: 20 }]} />
                        <View style={styles.formGroup}>
                            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 4 }}>
                                <Feather name="camera" size={18} color="#0f172a" />
                                <Text style={[styles.label, { marginBottom: 0 }]}>Registro Fotográfico Final <Text style={{color:'red'}}>*</Text></Text>
                            </View>
                            <Text style={styles.hint}>Evidencia de cómo quedó la actividad</Text>
                            
                            {formData.foto_despues ? (
                                <View style={styles.imagePreviewContainer}>
                                    <Image source={{ uri: formData.foto_despues.uri }} style={styles.imagePreview} />
                                    <TouchableOpacity 
                                        style={styles.removeImageBtn}
                                        onPress={() => setFormData((p:any) => ({...p, foto_despues: null}))}
                                    >
                                        <Feather name="x" size={16} color="#fff" />
                                    </TouchableOpacity>
                                </View>
                            ) : (
                                <TouchableOpacity style={styles.cameraBtn} onPress={pickFinalImage}>
                                    <View style={styles.cameraIconBg}>
                                        <Feather name="camera" size={24} color="#64748b" />
                                    </View>
                                    <Text style={styles.cameraBtnText}>Capturar Foto Final</Text>
                                </TouchableOpacity>
                            )}
                        </View>

                        <View style={styles.divider} />
                        <View style={styles.formGroup}>
                            <View style={{ flexDirection: 'row', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                                <Feather name="edit-3" size={18} color="#0f172a" />
                                <Text style={[styles.label, { marginBottom: 0 }]}>Firma del Técnico / Responsable <Text style={{color:'red'}}>*</Text></Text>
                            </View>
                            <View style={styles.signatureContainer}>
                                {Platform.OS === 'web' ? (
                                    <WebSignature
                                        ref={signatureRef}
                                        onOK={handleSignature}
                                        onEmpty={() => setFormData((p:any) => ({...p, firma_tecnico: null}))}
                                    />
                                ) : (
                                    <SignatureScreen
                                        ref={signatureRef}
                                        onOK={handleSignature}
                                        onEmpty={() => setFormData((p:any) => ({...p, firma_tecnico: null}))}
                                        descriptionText="Firme aquí"
                                        clearText="Limpiar"
                                        confirmText="Confirmar"
                                        webStyle={`.m-signature-pad--footer {display: none; margin: 0px;}`}
                                        autoClear={false}
                                    />
                                )}
                            </View>
                            <View style={styles.signatureActions}>
                                <TouchableOpacity style={styles.clearBtn} onPress={handleClearSignature}>
                                    <Feather name="trash-2" size={14} color="#fff" />
                                    <Text style={styles.clearBtnText}>LIMPIAR</Text>
                                </TouchableOpacity>
                                <TouchableOpacity 
                                    style={[styles.confirmBtn, !!formData.firma_tecnico && styles.confirmBtnActive]} 
                                    onPress={() => signatureRef.current?.readSignature()}
                                >
                                    <Feather name="check" size={14} color="#fff" />
                                    <Text style={styles.confirmBtnText}>{formData.firma_tecnico ? 'FIRMA CAPTURADA' : 'CONFIRMAR FIRMA'}</Text>
                                </TouchableOpacity>
                            </View>
                        </View>

                        <TouchableOpacity 
                            style={[styles.btnSubmit, submitting && {opacity: 0.7}]}
                            onPress={handleSubmit}
                            disabled={submitting}
                        >
                            <Feather name="save" size={20} color="#fff" style={{ marginRight: 8 }} />
                            {submitting ? <ActivityIndicator size="small" color="#fff" /> : <Text style={styles.btnSubmitText}>GUARDAR ACTIVIDAD</Text>}
                        </TouchableOpacity>
                    </View>
                )}
            </ScrollView>

            {/* Selector Modal NATIVO */}
            <Modal
                visible={pickerModal.visible}
                transparent={true}
                animationType="fade"
                onRequestClose={() => setPickerModal((p:any) => ({ ...p, visible: false }))}
            >
                <View style={styles.modalOverlay}>
                    <View style={styles.modalContent}>
                        <View style={styles.modalHeader}>
                            <Text style={styles.modalTitle}>{pickerModal.title}</Text>
                            <TouchableOpacity onPress={() => setPickerModal((p:any) => ({ ...p, visible: false }))}>
                                <Feather name="x" size={24} color="#64748b" />
                            </TouchableOpacity>
                        </View>
                        <ScrollView style={styles.modalScroll}>
                            {pickerModal.options.map((opt: any) => (
                                <TouchableOpacity 
                                    key={opt.value} 
                                    style={[styles.optionItem, pickerModal.selectedValue == opt.value && styles.optionSelected]}
                                    onPress={() => {
                                        pickerModal.onSelect(opt.value);
                                        setPickerModal((p:any) => ({ ...p, visible: false }));
                                    }}
                                >
                                    <Text 
                                        style={[styles.optionText, pickerModal.selectedValue == opt.value && styles.optionTextSelected]}
                                        numberOfLines={2}
                                    >
                                        {opt.label}
                                    </Text>
                                    {pickerModal.selectedValue == opt.value && <Feather name="check" size={18} color="#4f46e5" />}
                                </TouchableOpacity>
                            ))}
                        </ScrollView>
                    </View>
                </View>
            </Modal>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8fafc',
    },
    loadingContainer: {
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        backgroundColor: '#f8fafc',
    },
    loadingText: {
        marginTop: 12,
        color: '#64748b',
        fontWeight: '500',
    },
    header: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#fff',
        paddingTop: 50,
        paddingBottom: 16,
        paddingHorizontal: 16,
        borderBottomWidth: 1,
        borderBottomColor: '#f1f5f9',
    },
    backBtn: {
        padding: 8,
        marginRight: 8,
    },
    headerTitleContainer: {
        flex: 1,
    },
    headerTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#0f172a',
    },
    headerSubtitle: {
        fontSize: 12,
        color: '#64748b',
    },
    tabContainer: {
        paddingVertical: 10,
    },
    tabBarWrapper: {
        height: 60,
        backgroundColor: '#fff',
        borderBottomWidth: 1,
        borderBottomColor: '#f1f5f9',
    },
    tabBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        paddingHorizontal: 14,
        paddingVertical: 8,
        borderRadius: 20,
        backgroundColor: '#f1f5f9',
        borderWidth: 1,
        borderColor: '#e2e8f0',
        gap: 6,
    },
    tabActive: {
        backgroundColor: '#4f46e5',
        borderColor: '#4f46e5',
    },
    tabComplete: {
        backgroundColor: '#ecfdf5',
        borderColor: '#10b981',
    },
    tabLocked: {
        opacity: 0.6,
    },
    tabText: {
        fontSize: 13,
        fontWeight: '600',
        color: '#64748b',
    },
    tabTextActive: {
        color: '#fff',
    },
    tabTextComplete: {
        color: '#10b981',
    },
    tabTextLocked: {
        color: '#94a3b8',
    },
    errorAlert: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#fef2f2',
        padding: 12,
        marginHorizontal: 16,
        marginTop: 16,
        borderRadius: 8,
        borderLeftWidth: 4,
        borderLeftColor: '#ef4444',
        gap: 8,
    },
    errorText: {
        color: '#b91c1c',
        fontWeight: '500',
        fontSize: 13,
        flex: 1,
    },
    scrollContent: {
        padding: 16,
        paddingBottom: 40,
        maxWidth: 600,
        alignSelf: 'center',
        width: '100%',
        flexGrow: 1,
    },
    card: {
        backgroundColor: '#fff',
        borderRadius: 16,
        padding: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.05,
        elevation: 2,
    },
    sectionTitle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#4f46e5',
        marginBottom: 20,
    },
    formGroup: {
        marginBottom: 16,
    },
    label: {
        fontSize: 14,
        fontWeight: '600',
        color: '#334155',
        marginBottom: 8,
    },
    input: {
        backgroundColor: '#f8fafc',
        borderWidth: 1,
        borderColor: '#cbd5e1',
        borderRadius: 8,
        padding: 12,
        color: '#334155',
    },
    inputReadOnly: {
        backgroundColor: '#f1f5f9',
        borderWidth: 1,
        borderColor: '#e2e8f0',
        borderRadius: 8,
        padding: 12,
        color: '#64748b',
    },
    searchRow: {
        flexDirection: 'row',
        gap: 8,
    },
    searchInput: {
        flex: 1,
        backgroundColor: '#f8fafc',
        borderWidth: 1,
        borderColor: '#cbd5e1',
        borderRadius: 8,
        padding: 12,
        color: '#334155',
    },
    searchBtn: {
        backgroundColor: '#4f46e5',
        width: 48,
        borderRadius: 8,
        alignItems: 'center',
        justifyContent: 'center',
    },
    hint: {
        fontSize: 12,
        color: '#94a3b8',
        marginBottom: 4,
    },
    checkboxRow: {
        flexDirection: 'row',
        alignItems: 'center',
        gap: 12,
        marginTop: 8,
    },
    checkbox: {
        width: 20,
        height: 20,
        borderWidth: 2,
        borderColor: '#cbd5e1',
        borderRadius: 4,
        alignItems: 'center',
        justifyContent: 'center',
    },
    checkboxActive: {
        backgroundColor: '#4f46e5',
        borderColor: '#4f46e5',
    },
    checkboxLabel: {
        color: '#334155',
        fontWeight: '500',
    },
    cameraBtn: {
        backgroundColor: '#f1f5f9',
        borderWidth: 2,
        borderColor: '#cbd5e1',
        borderStyle: 'dashed',
        borderRadius: 12,
        padding: 24,
        alignItems: 'center',
        justifyContent: 'center',
        gap: 8,
    },
    cameraBtnText: {
        color: '#64748b',
        fontWeight: '600',
    },
    imagePreviewContainer: {
        position: 'relative',
        borderRadius: 12,
        overflow: 'hidden',
    },
    imagePreview: {
        width: '100%',
        height: 200,
        backgroundColor: '#f1f5f9',
    },
    removeImageBtn: {
        position: 'absolute',
        top: 8,
        right: 8,
        backgroundColor: 'rgba(239, 68, 68, 0.9)',
        width: 32,
        height: 32,
        borderRadius: 16,
        alignItems: 'center',
        justifyContent: 'center',
    },
    btnSubmit: {
        backgroundColor: '#10b981',
        borderRadius: 12,
        padding: 16,
        alignItems: 'center',
        marginTop: 24,
    },
    btnSubmitText: {
        color: '#fff',
        fontWeight: 'bold',
        fontSize: 16,
    },
    selectBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'space-between',
        backgroundColor: '#f8fafc',
        borderWidth: 1,
        borderColor: '#cbd5e1',
        borderRadius: 8,
        padding: 12,
    },
    selectText: {
        fontSize: 14,
        color: '#334155',
        fontWeight: '500',
    },
    selectPlaceholder: {
        fontSize: 14,
        color: '#94a3b8',
    },
    formGrid2: {
        flexDirection: 'row',
        gap: 12,
        width: '100%',
        flexWrap: 'wrap',
    },
    sectionHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginBottom: 20,
    },
    btnAdd: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#10b981',
        paddingHorizontal: 12,
        paddingVertical: 6,
        borderRadius: 8,
        gap: 4,
    },
    btnAddText: {
        color: '#fff',
        fontSize: 12,
        fontWeight: 'bold',
    },
    materialsList: {
        gap: 12,
    },
    materialItem: {
        padding: 16,
        borderRadius: 12,
        borderWidth: 1,
        borderColor: '#e2e8f0',
        backgroundColor: '#f8fafc',
        position: 'relative',
    },
    btnRemove: {
        position: 'absolute',
        top: 10,
        right: 10,
        zIndex: 10,
    },
    emptyState: {
        padding: 20,
        borderWidth: 1,
        borderColor: '#e2e8f0',
        borderStyle: 'dashed',
        borderRadius: 12,
        alignItems: 'center',
    },
    emptyStateText: {
        color: '#64748b',
        fontSize: 14,
    },
    divider: {
        height: 1,
        backgroundColor: '#e2e8f0',
        marginVertical: 20,
        borderStyle: 'dashed',
        borderWidth: 0.5,
    },
    cameraIconBg: {
        width: 48,
        height: 48,
        borderRadius: 24,
        backgroundColor: '#fff',
        alignItems: 'center',
        justifyContent: 'center',
        marginBottom: 8,
        borderWidth: 1,
        borderColor: '#e2e8f0',
    },
    signatureContainer: {
        height: 200,
        backgroundColor: '#fff',
        borderRadius: 12,
        borderWidth: 2,
        borderColor: '#cbd5e1',
        overflow: 'hidden',
    },
    signatureActions: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        marginTop: 12,
        gap: 12,
    },
    clearBtn: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#ef4444',
        paddingHorizontal: 16,
        paddingVertical: 10,
        borderRadius: 8,
        gap: 6,
    },
    clearBtnText: {
        color: '#fff',
        fontSize: 12,
        fontWeight: 'bold',
    },
    confirmBtn: {
        flex: 1,
        flexDirection: 'row',
        alignItems: 'center',
        justifyContent: 'center',
        backgroundColor: '#64748b',
        paddingHorizontal: 16,
        paddingVertical: 10,
        borderRadius: 8,
        gap: 6,
    },
    confirmBtnActive: {
        backgroundColor: '#4f46e5',
    },
    confirmBtnText: {
        color: '#fff',
        fontSize: 12,
        fontWeight: 'bold',
    },
    modalOverlay: {
        flex: 1,
        backgroundColor: 'rgba(15, 23, 42, 0.5)',
        justifyContent: 'center',
        padding: 20,
    },
    modalContent: {
        backgroundColor: '#fff',
        borderRadius: 24,
        maxHeight: '80%',
        width: '100%',
        maxWidth: 500,
        alignSelf: 'center',
        overflow: 'hidden',
        paddingBottom: 20,
    },
    modalHeader: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 20,
        borderBottomWidth: 1,
        borderBottomColor: '#f1f5f9',
    },
    modalTitle: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#0f172a',
    },
    modalScroll: {
        padding: 10,
    },
    optionItem: {
        flexDirection: 'row',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: 16,
        borderRadius: 12,
        marginBottom: 4,
    },
    optionSelected: {
        backgroundColor: '#f0f4ff',
    },
    optionText: {
        fontSize: 16,
        color: '#334155',
    },
    optionTextSelected: {
        color: '#4f46e5',
        fontWeight: 'bold',
    }
});
