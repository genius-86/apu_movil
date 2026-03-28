import { ActivityIndicator, View } from 'react-native';

export default function IndexPage() {
    // La redirección inicial ocurrirá en _layout.tsx a través del RootLayoutNav y el hook useEffect
    return (
        <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
            <ActivityIndicator size="large" color="#2563eb" />
        </View>
    );
}
