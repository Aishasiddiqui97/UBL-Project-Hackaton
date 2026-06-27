/**
 * Play alert sound for high-priority notifications
 * @param {string} type - Alert type: 'high', 'medium', 'low', 'success'
 */
export const playAlertSound = (type = 'medium') => {
  try {
    // Check if AudioContext is available
    const AudioContext = window.AudioContext || window.webkitAudioContext;
    if (!AudioContext) {
      console.warn('AudioContext not available');
      return;
    }

    const audioContext = new AudioContext();
    
    // Different frequencies for different alert types
    const frequencies = {
      high: [880, 660, 880],    // Urgent: A5, E5, A5
      medium: [660, 550],       // Warning: E5, C#5
      low: [440],               // Info: A4
      success: [523, 659, 784], // Success: C5, E5, G5
    };

    const freqs = frequencies[type] || frequencies.medium;
    
    freqs.forEach((freq, index) => {
      const oscillator = audioContext.createOscillator();
      const gainNode = audioContext.createGain();
      
      oscillator.connect(gainNode);
      gainNode.connect(audioContext.destination);
      
      oscillator.frequency.value = freq;
      oscillator.type = 'sine';
      
      // Set volume
      gainNode.gain.value = 0.3;
      
      // Fade in and out
      const startTime = audioContext.currentTime + (index * 0.15);
      gainNode.gain.setValueAtTime(0, startTime);
      gainNode.gain.linearRampToValueAtTime(0.3, startTime + 0.05);
      gainNode.gain.linearRampToValueAtTime(0, startTime + 0.15);
      
      oscillator.start(startTime);
      oscillator.stop(startTime + 0.15);
    });
  } catch (error) {
    console.error('Failed to play alert sound:', error);
  }
};

/**
 * Play notification sound
 */
export const playNotificationSound = () => {
  playAlertSound('low');
};

/**
 * Play error sound
 */
export const playErrorSound = () => {
  playAlertSound('high');
};

/**
 * Play success sound
 */
export const playSuccessSound = () => {
  playAlertSound('success');
};

export default playAlertSound;
