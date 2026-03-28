import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, KeyboardAvoidingView, Platform, ScrollView, Pressable } from 'react-native';
import { router } from 'expo-router';
import { FontAwesome5 } from '@expo/vector-icons';
import { useAuth } from '../src/context/AuthContext';

export default function LoginScreen() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isUsernameFocused, setIsUsernameFocused] = useState(false);
    const [isPasswordFocused, setIsPasswordFocused] = useState(false);
    const { login } = useAuth() as any;

    const usernameInputRef = React.useRef<TextInput>(null);
    const passwordInputRef = React.useRef<TextInput>(null);

    const handleSubmit = async () => {
        if (!username || !password) {
            setError('Por favor complete todos los campos.');
            return;
        }
        
        setError('');
        setIsLoading(true);
        try {
            await login(username, password);
            router.replace('/activities');
        } catch (err) {
            setError('Credenciales inválidas. Por favor intente nuevamente.');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <View style={styles.container}>
            {/* Fondo fijo */}
            <View style={styles.background} pointerEvents="none">
                <View style={[styles.shape, styles.shape1]} />
                <View style={[styles.shape, styles.shape2]} />
                <View style={[styles.shape, styles.shape3]} />
            </View>

            <KeyboardAvoidingView 
                style={styles.keyboardView} 
                behavior={Platform.OS === 'ios' ? 'padding' : undefined}
                enabled={Platform.OS === 'ios'}
            >
                <ScrollView 
                    contentContainerStyle={styles.scrollContent}
                    keyboardShouldPersistTaps="handled"
                    showsVerticalScrollIndicator={false}
                >
                    <View style={styles.card}>
                        <View style={styles.header}>
                            <View style={styles.brandLogo}>
                                <View style={styles.logoIconContainer}>
                                    <Text style={styles.logoText}>A</Text>
                                </View>
                            </View>
                            <Text style={styles.welcomeText}>Bienvenido</Text>
                            <Text style={styles.subText}>Inicie sesión en APU System</Text>
                        </View>

                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Usuario</Text>
                            <Pressable 
                                onPress={() => usernameInputRef.current?.focus()}
                                style={[
                                    styles.inputWrapper,
                                    isUsernameFocused && styles.inputWrapperFocused
                                ]}
                            >
                                <FontAwesome5 
                                    name="user" 
                                    size={18} 
                                    color={isUsernameFocused ? "#4f46e5" : "#64748b"} 
                                    style={styles.inputIcon} 
                                />
                                <TextInput
                                    ref={usernameInputRef}
                                    style={styles.input}
                                    placeholder="Ingrese su usuario"
                                    placeholderTextColor="#94a3b8"
                                    value={username}
                                    onChangeText={setUsername}
                                    autoCapitalize="none"
                                    onFocus={() => setIsUsernameFocused(true)}
                                    onBlur={() => setIsUsernameFocused(false)}
                                    blurOnSubmit={false}
                                    onSubmitEditing={() => passwordInputRef.current?.focus()}
                                />
                            </Pressable>
                        </View>

                        <View style={styles.formGroup}>
                            <Text style={styles.label}>Contraseña</Text>
                            <Pressable 
                                onPress={() => passwordInputRef.current?.focus()}
                                style={[
                                    styles.inputWrapper,
                                    isPasswordFocused && styles.inputWrapperFocused
                                ]}
                            >
                                <FontAwesome5 
                                    name="lock" 
                                    size={18} 
                                    color={isPasswordFocused ? "#4f46e5" : "#64748b"} 
                                    style={styles.inputIcon} 
                                />
                                <TextInput
                                    ref={passwordInputRef}
                                    style={styles.input}
                                    placeholder="••••••••"
                                    placeholderTextColor="#94a3b8"
                                    secureTextEntry
                                    value={password}
                                    onChangeText={setPassword}
                                    onFocus={() => setIsPasswordFocused(true)}
                                    onBlur={() => setIsPasswordFocused(false)}
                                    onSubmitEditing={handleSubmit}
                                />
                            </Pressable>
                        </View>

                        {error ? (
                            <View style={styles.errorContainer}>
                                <Text style={styles.errorText}>{error}</Text>
                            </View>
                        ) : null}

                        <TouchableOpacity 
                            style={[styles.button, isLoading && styles.buttonDisabled]} 
                            onPress={handleSubmit}
                            disabled={isLoading}
                        >
                            {isLoading ? (
                                <ActivityIndicator color="#fff" />
                            ) : (
                                <View style={styles.buttonContent}>
                                    <Text style={styles.buttonText}>Iniciar Sesión</Text>
                                    <FontAwesome5 name="arrow-right" size={16} color="#fff" style={styles.buttonIcon} />
                                </View>
                            )}
                        </TouchableOpacity>

                        <View style={styles.footer}>
                            <Text style={styles.footerText}>© 2026 APU System. Gestión de Alumbrado.</Text>
                        </View>
                    </View>
                </ScrollView>
            </KeyboardAvoidingView>
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#f8fafc',
    },
    keyboardView: {
        flex: 1,
        width: '100%',
    },
    scrollContent: {
        flexGrow: 1,
        justifyContent: 'center',
        paddingVertical: 40,
    },
    background: {
        ...StyleSheet.absoluteFillObject,
        overflow: 'hidden',
        zIndex: -1,
    },
    shape: {
        position: 'absolute',
        borderRadius: 9999,
        opacity: 0.1,
    },
    shape1: {
        top: -100,
        left: -100,
        width: 400,
        height: 400,
        backgroundColor: '#3b82f6',
    },
    shape2: {
        bottom: -50,
        right: -50,
        width: 300,
        height: 300,
        backgroundColor: '#818cf8',
    },
    shape3: {
        top: '40%',
        left: '40%',
        width: 250,
        height: 250,
        backgroundColor: '#22d3ee',
    },
    card: {
        padding: 30,
        backgroundColor: 'rgba(255, 255, 255, 0.9)',
        borderRadius: 24,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 10 },
        shadowOpacity: 0.1,
        shadowRadius: 15,
        elevation: 5,
        width: '90%',
        maxWidth: 400,
        alignSelf: 'center',
        zIndex: 10,
    },
    header: {
        alignItems: 'center',
        marginBottom: 30,
    },
    brandLogo: {
        marginBottom: 20,
    },
    logoIconContainer: {
        width: 60,
        height: 60,
        backgroundColor: '#2563eb',
        borderRadius: 16,
        alignItems: 'center',
        justifyContent: 'center',
        shadowColor: '#2563eb',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
    },
    logoText: {
        color: '#fff',
        fontSize: 28,
        fontWeight: '800',
    },
    welcomeText: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#1e293b',
        marginBottom: 5,
    },
    subText: {
        fontSize: 15,
        color: '#64748b',
    },
    formGroup: {
        marginBottom: 20,
    },
    label: {
        fontSize: 14,
        fontWeight: '600',
        color: '#1e293b',
        marginBottom: 8,
    },
    inputWrapper: {
        flexDirection: 'row',
        alignItems: 'center',
        backgroundColor: '#fff',
        borderWidth: 1,
        borderColor: '#cbd5e1',
        borderRadius: 12,
        paddingHorizontal: 15,
    },
    inputWrapperFocused: {
        borderColor: '#4f46e5',
        borderWidth: 1,
        backgroundColor: '#fff',
        // Sombra suave sin usar elevation agresiva
        shadowColor: '#4f46e5',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
    },
    inputIcon: {
        marginRight: 10,
    },
    input: {
        flex: 1,
        paddingVertical: 12,
        fontSize: 16,
        color: '#1e293b',
    },
    errorContainer: {
        backgroundColor: '#fef2f2',
        borderWidth: 1,
        borderColor: '#fca5a5',
        borderRadius: 8,
        padding: 10,
        marginBottom: 20,
        alignItems: 'center',
    },
    errorText: {
        color: '#ef4444',
        fontSize: 14,
    },
    button: {
        backgroundColor: '#2563eb',
        borderRadius: 12,
        paddingVertical: 14,
        alignItems: 'center',
        marginTop: 10,
        shadowColor: '#2563eb',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 5,
        elevation: 6,
    },
    buttonDisabled: {
        opacity: 0.7,
    },
    buttonContent: {
        flexDirection: 'row',
        alignItems: 'center',
    },
    buttonText: {
        color: '#fff',
        fontSize: 16,
        fontWeight: '600',
        marginRight: 10,
    },
    buttonIcon: {
        marginTop: 2,
    },
    footer: {
        marginTop: 30,
        alignItems: 'center',
    },
    footerText: {
        color: '#94a3b8',
        fontSize: 12,
    }
});
