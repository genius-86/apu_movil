import AsyncStorage from '@react-native-async-storage/async-storage';
import { activityService } from './api';
import { Platform } from 'react-native';

const SYNC_QUEUE_KEY = '@apu_sync_queue';

export const syncService = {
  // Add an item to the queue
  addToQueue: async (activityData, photoData) => {
    try {
      const queueStr = await AsyncStorage.getItem(SYNC_QUEUE_KEY);
      const queue = queueStr ? JSON.parse(queueStr) : [];
      
      const queueItem = {
        id: Date.now().toString(), // Unique local ID
        timestamp: new Date().toISOString(),
        activityData,
        photoData: photoData ? {
            uri: photoData.uri,
            type: photoData.type || 'image/jpeg',
            name: photoData.name || `despues_${Date.now()}.jpg`
        } : null
      };

      queue.push(queueItem);
      await AsyncStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(queue));
      return queueItem;
    } catch (error) {
      console.error('Error adding to sync queue', error);
      throw error;
    }
  },

  // Get the current queue
  getQueue: async () => {
    try {
      const queueStr = await AsyncStorage.getItem(SYNC_QUEUE_KEY);
      return queueStr ? JSON.parse(queueStr) : [];
    } catch (error) {
      console.error('Error getting sync queue', error);
      return [];
    }
  },

  // Remove specific items from queue
  removeFromQueue: async (idsToRemove) => {
    try {
      const queue = await syncService.getQueue();
      const updatedQueue = queue.filter(item => !idsToRemove.includes(item.id));
      await AsyncStorage.setItem(SYNC_QUEUE_KEY, JSON.stringify(updatedQueue));
    } catch (error) {
      console.error('Error removing from sync queue', error);
    }
  },

  // Attempt to sync all pending items
  syncAll: async () => {
    const queue = await syncService.getQueue();
    if (queue.length === 0) return { success: 0, failed: 0 };

    let successCount = 0;
    let failedCount = 0;
    const idsToRemove = [];

    for (const item of queue) {
      try {
        // 1. Create/Update Activity
        const saveRes = await activityService.save(item.activityData);
        const serverId = saveRes.data.id_actividad || item.activityData.id_actividad;

        // 2. Finish Activity
        try {
            await activityService.finish(serverId);
        } catch(e) {
            console.error('Error finishing activity during sync', e);
        }

        // 3. Upload Photo if exists
        if (item.photoData && serverId) {
            const formData = new FormData();
            formData.append('foto', {
                uri: item.photoData.uri,
                name: item.photoData.name,
                type: item.photoData.type
            });
            formData.append('tipo', 'DESPUES');
            try {
                await activityService.addPhoto(serverId, formData);
            } catch(photoErr) {
               console.error('Error uploading photo during sync', photoErr); 
            }
        }
        
        successCount++;
        idsToRemove.push(item.id);
      } catch (error) {
        console.error(`Failed to sync item ${item.id}`, error);
        failedCount++;
      }
    }

    // Clean up successful ones
    if (idsToRemove.length > 0) {
      await syncService.removeFromQueue(idsToRemove);
    }

    return { success: successCount, failed: failedCount, total: queue.length };
  },

  // Clear entire queue (DANGEROUS)
  clearQueue: async () => {
    await AsyncStorage.removeItem(SYNC_QUEUE_KEY);
  }
};
