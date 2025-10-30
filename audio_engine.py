"""
Real-time engine sound synthesis using sounddevice and NumPy
"""
import numpy as np
import threading
import queue
import sys

try:
    import sounddevice as sd
    SOUNDDEVICE_AVAILABLE = True
except ImportError:
    SOUNDDEVICE_AVAILABLE = False
    print("Warning: sounddevice not installed. Install with: pip install sounddevice")


class AudioEngine:
    """
    Real-time audio synthesis for engine sounds
    Uses sine and square waves to simulate engine rumble, exhaust, and turbo whistle
    """
    
    def __init__(self, sample_rate=44100, blocksize=2048):
        self.sample_rate = sample_rate
        self.blocksize = blocksize
        self.is_running = False
        self.volume = 0.5
        self.enabled = True
        
        # Audio parameters
        self.engine_rumble_freq = 100  # Hz
        self.exhaust_freq = 400  # Hz
        self.turbo_whistle_freq = 2000  # Hz
        
        # Smooth transition parameters (to prevent popping)
        self.prev_rumble_freq = 100
        self.prev_exhaust_freq = 400
        self.prev_turbo_freq = 2000
        self.prev_volume = 0.5
        
        # Audio state tracking
        self.current_rpm = 0
        self.current_throttle = 0
        self.is_idle = True
        
        # sounddevice setup
        self.stream = None
        self.stop_event = threading.Event()
        self.command_queue = queue.Queue()
        
        if SOUNDDEVICE_AVAILABLE:
            self.init_audio()
    
    def init_audio(self):
        """Initialize sounddevice stream"""
        try:
            self.is_running = True
            self.stream = sd.OutputStream(
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32',
                blocksize=self.blocksize,
                callback=self.audio_callback
            )
            self.stream.start()
            print("Audio engine initialized successfully (sounddevice)")
        except Exception as e:
            print(f"Error initializing audio: {e}")
            self.is_running = False
    
    def audio_callback(self, outdata, frames, time_info, status):
        """sounddevice callback - generates audio in real-time with smooth transitions"""
        if self.is_running and not self.command_queue.empty():
            try:
                cmd = self.command_queue.get_nowait()
                if cmd['type'] == 'parameters':
                    # Store previous values for smooth interpolation
                    self.prev_rumble_freq = self.engine_rumble_freq
                    self.prev_exhaust_freq = self.exhaust_freq
                    self.prev_turbo_freq = self.turbo_whistle_freq
                    self.prev_volume = self.volume
                    
                    # Update state
                    self.current_rpm = cmd['rpm']
                    self.current_throttle = cmd['throttle']
                    
                    # Determine if idle or accelerating
                    self.is_idle = (self.current_rpm < 1000 and self.current_throttle < 0.1)
                    
                    # Smooth frequency updates with bounds checking
                    target_rumble = max(20, min(300, cmd['rpm'] * 0.08))  # Lower frequency for deeper rumble
                    target_exhaust = max(100, min(2000, cmd['rpm'] * 0.25 + 150))
                    target_turbo = max(1500, min(5000, 2000 + cmd['boost'] * 150))
                    
                    # Interpolate to prevent sudden jumps (exponential smoothing)
                    smooth_factor = 0.3  # Lower = smoother transitions
                    self.engine_rumble_freq = self.prev_rumble_freq + (target_rumble - self.prev_rumble_freq) * smooth_factor
                    self.exhaust_freq = self.prev_exhaust_freq + (target_exhaust - self.prev_exhaust_freq) * smooth_factor
                    self.turbo_whistle_freq = self.prev_turbo_freq + (target_turbo - self.prev_turbo_freq) * smooth_factor
                    
                    # Volume with smooth fade
                    target_volume = max(0, min(1, cmd['volume']))
                    self.volume = self.prev_volume + (target_volume - self.prev_volume) * 0.1
            except queue.Empty:
                pass
        
        try:
            # Generate audio frames
            audio_data = self.generate_audio(frames)
            outdata[:] = audio_data.reshape(-1, 1)  # Reshape to (frames, 1) for mono output
        except Exception as e:
            print(f"Error in audio callback: {e}")
            outdata.fill(0)  # Silence on error
    
    def generate_audio(self, frame_count):
        """Generate engine sound audio with proper idle/accel/decel mapping"""
        t = np.arange(frame_count) / self.sample_rate
        
        # Engine rumble (low frequency sine wave with realistic variation)
        # Add firing order variation for realism
        rumble_variation = 1 + 0.15 * np.sin(2 * np.pi * 4 * t)  # 4-cylinder firing pattern
        rumble_freq_varied = self.engine_rumble_freq * rumble_variation
        rumble = 0.35 * np.sin(2 * np.pi * rumble_freq_varied * t)
        
        # Add subharmonic for deeper bass (only at higher RPM)
        if self.current_rpm > 2000:
            subharmonic_intensity = min(0.2, (self.current_rpm - 2000) / 5000 * 0.2)
            subharmonic = subharmonic_intensity * np.sin(2 * np.pi * (rumble_freq_varied * 0.5) * t)
            rumble += subharmonic
        
        # Exhaust note (square wave with harmonics) - varies with throttle
        throttle_factor = 0.5 + self.current_throttle * 0.5
        exhaust = 0.2 * throttle_factor * self.square_wave(self.exhaust_freq * t)
        exhaust += 0.12 * throttle_factor * self.square_wave(self.exhaust_freq * 1.5 * t)  # 1st harmonic
        exhaust += 0.06 * throttle_factor * self.square_wave(self.exhaust_freq * 2.0 * t)  # 2nd harmonic
        
        # Turbo whistle (high frequency sine) - only audible under boost
        turbo_intensity = max(0, min(0.25, (self.turbo_whistle_freq - 2000) / 3000 * 0.25))
        whistle = turbo_intensity * np.sin(2 * np.pi * self.turbo_whistle_freq * t)
        
        # Deceleration sound (slight overrun crackle at high RPM when throttle closes)
        if self.current_rpm > 3000 and self.current_throttle < 0.1:
            # Add subtle crackle/pop effect
            crackle_noise = 0.05 * np.random.uniform(-1, 1, frame_count)
            crackle_envelope = np.exp(-5 * t)  # Decay envelope
            exhaust += crackle_noise * crackle_envelope
        
        # Idle sound - different character at idle
        if self.is_idle:
            # Gentler, more consistent idle
            idle_mix = 0.7
            rumble *= idle_mix
            exhaust *= 0.3
            whistle *= 0.0  # No turbo whistle at idle
        
        # Mix all components with proper balance
        audio = (rumble + exhaust + whistle) * self.volume * 0.25
        
        # Soft clipping to prevent distortion (tanh provides smooth limiting)
        audio = np.tanh(audio)
        
        # Apply fade in/out to prevent clicking (very short, just at boundaries)
        fade_samples = min(10, frame_count // 10)
        if fade_samples > 0:
            fade_in = np.linspace(0, 1, fade_samples)
            fade_out = np.linspace(1, 0, fade_samples)
            audio[:fade_samples] *= fade_in
            audio[-fade_samples:] *= fade_out
        
        return audio
    
    @staticmethod
    def square_wave(phase):
        """Generate square wave from phase"""
        return np.where(np.sin(2 * np.pi * phase) > 0, 0.5, -0.5)
    
    def update_parameters(self, rpm, boost, throttle, volume):
        """Queue audio parameter updates"""
        if self.is_running and SOUNDDEVICE_AVAILABLE:
            self.command_queue.put({
                'type': 'parameters',
                'rpm': rpm,
                'boost': boost,
                'throttle': throttle,
                'volume': volume
            })
    
    def set_volume(self, volume):
        """Set audio volume (0-1)"""
        self.volume = max(0, min(1, volume))
    
    def stop(self):
        """Stop audio playback"""
        if SOUNDDEVICE_AVAILABLE:
            self.is_running = False
            if self.stream:
                self.stream.stop()
                self.stream.close()
    
    def __del__(self):
        self.stop()


class SimpleAudioGenerator:
    """Fallback audio generator for systems without PyAudio"""
    
    def __init__(self):
        self.sample_rate = 44100
        self.is_running = False
        self.volume = 0.5
        self.enabled = True
    
    def update_parameters(self, rpm, boost, throttle, volume):
        """Simulate parameter update"""
        pass
    
    def set_volume(self, volume):
        self.volume = max(0, min(1, volume))
    
    def stop(self):
        self.is_running = False


def get_audio_engine():
    """Factory function to get the appropriate audio engine"""
    if SOUNDDEVICE_AVAILABLE:
        try:
            return AudioEngine()
        except Exception as e:
            print(f"Could not initialize sounddevice: {e}")
            print("Using simple audio generator (visual only)")
            return SimpleAudioGenerator()
    else:
        return SimpleAudioGenerator()
