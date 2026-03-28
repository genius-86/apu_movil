import React, { createContext, useState, useEffect, useContext } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../services/api';

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadStoredUser = async () => {
            try {
                const token = await AsyncStorage.getItem('access_token');
                const userData = await AsyncStorage.getItem('user_data');
                
                if (token && userData) {
                    setUser(JSON.parse(userData));
                }
            } catch (error) {
                console.error('Error loading stored user:', error);
                await AsyncStorage.removeItem('user_data');
            } finally {
                setLoading(false);
            }
        };

        loadStoredUser();
    }, []);

    const login = async (username, password) => {
        try {
            const response = await api.post('token/', { usuario: username, password });
            const { access, refresh, user: userData } = response.data;

            await AsyncStorage.setItem('access_token', access);
            await AsyncStorage.setItem('refresh_token', refresh);
            await AsyncStorage.setItem('user_data', JSON.stringify(userData));

            setUser(userData);
            return true;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    };

    const logout = async () => {
        try {
            await AsyncStorage.removeItem('access_token');
            await AsyncStorage.removeItem('refresh_token');
            await AsyncStorage.removeItem('user_data');
            setUser(null);
        } catch (error) {
            console.error('Error on logout:', error);
        }
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
