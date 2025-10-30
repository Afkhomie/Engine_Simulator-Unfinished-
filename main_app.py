"""
Engine Simulator - Main Application
High-performance engine physics simulation with real-time visualization
"""

import tkinter as tk
from tkinter import ttk
import ctypes
import os
import time
import math


class EnginePhysicsDLL:
    """Wrapper for C++ engine physics DLL"""
    
    def __init__(self, dll_path="engine_physics.dll"):
        self.dll_path = os.path.abspath(dll_path)
        self.dll = ctypes.CDLL(self.dll_path)
        self._setup_function_signatures()
        self.engine = self.dll.EnginePhysics_new()
        
    def _setup_function_signatures(self):
        """Define all function signatures for ctypes"""
        # Constructor/Destructor
        self.dll.EnginePhysics_new.restype = ctypes.c_void_p
        self.dll.EnginePhysics_delete.argtypes = [ctypes.c_void_p]
        
        # Control functions
        self.dll.EnginePhysics_startEngine.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_stopEngine.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_setThrottle.argtypes = [ctypes.c_void_p, ctypes.c_double]
        self.dll.EnginePhysics_setBrake.argtypes = [ctypes.c_void_p, ctypes.c_double]
        self.dll.EnginePhysics_shiftUp.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_shiftDown.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_toggleClutch.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_setGear.argtypes = [ctypes.c_void_p, ctypes.c_int]
        
        # Configuration
        self.dll.EnginePhysics_setRevLimiter.argtypes = [ctypes.c_void_p, ctypes.c_int]
        self.dll.EnginePhysics_setBoostPressure.argtypes = [ctypes.c_void_p, ctypes.c_double]
        
        # Update
        self.dll.EnginePhysics_update.argtypes = [ctypes.c_void_p, ctypes.c_double]
        
        # Getters
        self.dll.EnginePhysics_getRPM.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getRPM.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getSpeed.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getSpeed.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getTorque.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getTorque.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getPower.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getPower.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getBoost.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getBoost.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getCurrentGear.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getCurrentGear.restype = ctypes.c_int
        
        self.dll.EnginePhysics_isEngineRunning.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_isEngineRunning.restype = ctypes.c_bool
        
        self.dll.EnginePhysics_getThrottlePosition.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getThrottlePosition.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getOilTemp.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getOilTemp.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getCoolantTemp.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getCoolantTemp.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getIntakeTemp.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getIntakeTemp.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getFuelLevel.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getFuelLevel.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getFuelConsumption.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getFuelConsumption.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getEngineWear.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getEngineWear.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getTotalDistance.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getTotalDistance.restype = ctypes.c_double
        
        self.dll.EnginePhysics_getRuntime.argtypes = [ctypes.c_void_p]
        self.dll.EnginePhysics_getRuntime.restype = ctypes.c_double
        
        self.dll.EnginePhysics_resetSession.argtypes = [ctypes.c_void_p]
    
    # Control methods
    def start_engine(self):
        self.dll.EnginePhysics_startEngine(self.engine)
    
    def stop_engine(self):
        self.dll.EnginePhysics_stopEngine(self.engine)
    
    def set_throttle(self, value):
        self.dll.EnginePhysics_setThrottle(self.engine, float(value))
    
    def set_brake(self, value):
        self.dll.EnginePhysics_setBrake(self.engine, float(value))
    
    def shift_up(self):
        self.dll.EnginePhysics_shiftUp(self.engine)
    
    def shift_down(self):
        self.dll.EnginePhysics_shiftDown(self.engine)
    
    def toggle_clutch(self):
        self.dll.EnginePhysics_toggleClutch(self.engine)
    
    def set_gear(self, gear):
        self.dll.EnginePhysics_setGear(self.engine, int(gear))
    
    def set_rev_limiter(self, rpm):
        self.dll.EnginePhysics_setRevLimiter(self.engine, int(rpm))
    
    def set_boost_pressure(self, psi):
        self.dll.EnginePhysics_setBoostPressure(self.engine, float(psi))
    
    def update(self, delta_time):
        self.dll.EnginePhysics_update(self.engine, float(delta_time))
    
    # Property getters
    @property
    def rpm(self):
        return self.dll.EnginePhysics_getRPM(self.engine)
    
    @property
    def speed(self):
        return self.dll.EnginePhysics_getSpeed(self.engine)
    
    @property
    def torque(self):
        return self.dll.EnginePhysics_getTorque(self.engine)
    
    @property
    def power(self):
        return self.dll.EnginePhysics_getPower(self.engine)
    
    @property
    def boost(self):
        return self.dll.EnginePhysics_getBoost(self.engine)
    
    @property
    def current_gear(self):
        return self.dll.EnginePhysics_getCurrentGear(self.engine)
    
    @property
    def is_running(self):
        return self.dll.EnginePhysics_isEngineRunning(self.engine)
    
    @property
    def throttle_position(self):
        return self.dll.EnginePhysics_getThrottlePosition(self.engine)
    
    @property
    def oil_temp(self):
        return self.dll.EnginePhysics_getOilTemp(self.engine)
    
    @property
    def coolant_temp(self):
        return self.dll.EnginePhysics_getCoolantTemp(self.engine)
    
    @property
    def intake_temp(self):
        return self.dll.EnginePhysics_getIntakeTemp(self.engine)
    
    @property
    def fuel_level(self):
        return self.dll.EnginePhysics_getFuelLevel(self.engine)
    
    @property
    def fuel_consumption(self):
        return self.dll.EnginePhysics_getFuelConsumption(self.engine)
    
    @property
    def engine_wear(self):
        return self.dll.EnginePhysics_getEngineWear(self.engine)
    
    @property
    def total_distance(self):
        return self.dll.EnginePhysics_getTotalDistance(self.engine)
    
    @property
    def runtime(self):
        return self.dll.EnginePhysics_getRuntime(self.engine)
    
    def reset_session(self):
        self.dll.EnginePhysics_resetSession(self.engine)
    
    def __del__(self):
        if hasattr(self, 'engine') and self.engine:
            self.dll.EnginePhysics_delete(self.engine)


class DigitalGauge(tk.Frame):
    """Modern digital gauge with progress bar"""
    
    def __init__(self, parent, title, unit, max_value=1000, warning_threshold=0.8, danger_threshold=0.9):
        super().__init__(parent, bg='#1a1a1a')
        self.title = title
        self.unit = unit
        self.max_value = max_value
        self.warning_threshold = warning_threshold
        self.danger_threshold = danger_threshold
        self.current_value = 0
        
        # Title label
        title_label = tk.Label(self, text=title, font=('Arial', 10, 'bold'),
                              bg='#1a1a1a', fg='#00ff00')
        title_label.pack(anchor='w', padx=5, pady=2)
        
        # Value display
        self.value_label = tk.Label(self, text='0', font=('Arial', 28, 'bold'),
                                   bg='#1a1a1a', fg='#00ff00')
        self.value_label.pack(anchor='w', padx=5)
        
        # Unit label
        unit_label = tk.Label(self, text=unit, font=('Arial', 9),
                             bg='#1a1a1a', fg='#00aa00')
        unit_label.pack(anchor='w', padx=5)
        
        # Progress bar canvas
        self.bar_width = 140
        self.bar_height = 24
        self.canvas = tk.Canvas(self, width=self.bar_width, height=self.bar_height,
                               bg='#0a0a0a', highlightthickness=1, highlightbackground='#00ff00')
        self.canvas.pack(pady=5, padx=5)
    
    def update(self, value):
        """Update gauge value and color"""
        self.current_value = value
        self.value_label.config(text=f'{int(value)}')
        
        # Update progress bar
        self.canvas.delete('bar')
        if self.max_value > 0:
            ratio = min(1.0, value / self.max_value)
            bar_width = ratio * self.bar_width
            
            # Color based on threshold
            if ratio < self.warning_threshold:
                color = '#00ff00'
            elif ratio < self.danger_threshold:
                color = '#ffaa00'
            else:
                color = '#ff0000'
            
            if bar_width > 0:
                self.canvas.create_rectangle(0, 0, bar_width, self.bar_height,
                                            fill=color, outline='', tags='bar')


class EngineSimulatorApp:
    """Main application window"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Engine Simulator v2.0 - C++ Physics Edition")
        self.root.geometry("1400x900")
        self.root.config(bg='#0a0a0a')
        
        # Initialize engine physics
        try:
            self.engine = EnginePhysicsDLL()
            print("✓ Engine physics DLL loaded successfully")
        except Exception as e:
            print(f"✗ Failed to load engine physics DLL: {e}")
            self.root.destroy()
            return
        
        # Application state
        self.running = True
        self.last_update_time = time.time()
        self.throttle_pressed = False
        self.brake_pressed = False
        
        # Build UI
        self.create_ui()
        self.setup_keybindings()
        
        # Start simulation loop
        self.simulation_loop()
    
    def create_ui(self):
        """Create user interface"""
        # Header
        header = tk.Frame(self.root, bg='#1a1a1a', height=70)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        title = tk.Label(header, text="🏎️ ENGINE SIMULATOR", font=('Arial', 26, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(side=tk.LEFT, padx=10)
        
        version = tk.Label(header, text="v2.0 | C++ Physics", font=('Arial', 12),
                          bg='#1a1a1a', fg='#00aa00')
        version.pack(side=tk.LEFT, padx=10)
        
        # Main layout: 3 columns
        container = tk.Frame(self.root, bg='#0a0a0a')
        container.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Controls
        left_panel = tk.Frame(container, bg='#1a1a1a', width=320)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        # Center panel - Main gauges
        center_panel = tk.Frame(container, bg='#0a0a0a')
        center_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        # Right panel - Information
        right_panel = tk.Frame(container, bg='#1a1a1a', width=320)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=5)
        
        # Create sections
        self.create_controls_panel(left_panel)
        self.create_gauges_panel(center_panel)
        self.create_info_panel(right_panel)
    
    def create_controls_panel(self, parent):
        """Create left control panel"""
        # Title
        title = tk.Label(parent, text='CONTROLS', font=('Arial', 14, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(anchor='w', padx=10, pady=10)
        
        # Engine start/stop button
        self.start_button = tk.Button(parent, text='START ENGINE [E]',
                                     font=('Arial', 12, 'bold'), bg='#00ff00', fg='#000000',
                                     command=self.toggle_engine, height=2)
        self.start_button.pack(fill=tk.X, padx=10, pady=5)
        
        # Gear display
        gear_frame = tk.LabelFrame(parent, text='GEAR SELECTION', bg='#1a1a1a',
                                  fg='#00ff00', font=('Arial', 11, 'bold'))
        gear_frame.pack(fill=tk.X, padx=10, pady=10)
        
        gear_button_frame = tk.Frame(gear_frame, bg='#1a1a1a')
        gear_button_frame.pack(pady=5)
        
        gears = ['R', 'N', '1', '2', '3', '4', '5', '6']
        for i, gear in enumerate(gears):
            btn = tk.Button(gear_button_frame, text=gear, width=4, height=2,
                          font=('Arial', 10, 'bold'), bg='#333333', fg='#00ff00',
                          command=lambda g=i-1: self.set_gear(g))
            btn.grid(row=0, column=i, padx=2)
        
        # Rev limiter
        rev_frame = tk.LabelFrame(parent, text='REV LIMITER', bg='#1a1a1a',
                                 fg='#00ff00', font=('Arial', 11, 'bold'))
        rev_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.rev_slider = tk.Scale(rev_frame, from_=3000, to=9000, orient=tk.HORIZONTAL,
                                  bg='#333333', fg='#00ff00', troughcolor='#000000',
                                  font=('Arial', 10), command=self.on_rev_limiter_change)
        self.rev_slider.set(7200)
        self.rev_slider.pack(fill=tk.X, padx=5, pady=5)
        
        self.rev_label = tk.Label(rev_frame, text='7200 RPM', font=('Arial', 10, 'bold'),
                                 bg='#1a1a1a', fg='#00ff00')
        self.rev_label.pack()
        
        # Boost control
        boost_frame = tk.LabelFrame(parent, text='BOOST PRESSURE', bg='#1a1a1a',
                                   fg='#00ff00', font=('Arial', 11, 'bold'))
        boost_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.boost_slider = tk.Scale(boost_frame, from_=0, to=25, orient=tk.HORIZONTAL,
                                    bg='#333333', fg='#00ff00', troughcolor='#000000',
                                    font=('Arial', 10), command=self.on_boost_change)
        self.boost_slider.set(15)
        self.boost_slider.pack(fill=tk.X, padx=5, pady=5)
        
        self.boost_label = tk.Label(boost_frame, text='15.0 PSI', font=('Arial', 10, 'bold'),
                                   bg='#1a1a1a', fg='#00ff00')
        self.boost_label.pack()
        
        # Keyboard shortcuts info
        shortcuts_frame = tk.LabelFrame(parent, text='KEYBOARD SHORTCUTS', bg='#1a1a1a',
                                       fg='#00ff00', font=('Arial', 11, 'bold'))
        shortcuts_frame.pack(fill=tk.X, padx=10, pady=10)
        
        shortcuts_text = (
            "E - Start/Stop Engine\n"
            "SPACE - Throttle\n"
            "B - Brake\n"
            "↑ - Shift Up\n"
            "↓ - Shift Down\n"
            "C - Toggle Clutch\n"
            "R - Reset Session"
        )
        shortcuts_label = tk.Label(shortcuts_frame, text=shortcuts_text, font=('Courier', 9),
                                  bg='#1a1a1a', fg='#00aa00', justify=tk.LEFT)
        shortcuts_label.pack(padx=10, pady=5, anchor='w')
    
    def create_gauges_panel(self, parent):
        """Create center gauges panel"""
        # Main gauges
        self.rpm_gauge = DigitalGauge(parent, 'ENGINE RPM', 'rev/min', 8000, 0.85, 0.95)
        self.rpm_gauge.pack(pady=10)
        
        self.speed_gauge = DigitalGauge(parent, 'SPEED', 'km/h', 250, 0.8, 0.95)
        self.speed_gauge.pack(pady=10)
        
        self.power_gauge = DigitalGauge(parent, 'POWER', 'HP', 500, 0.9, 0.98)
        self.power_gauge.pack(pady=10)
        
        # Large gear display
        gear_display_frame = tk.Frame(parent, bg='#1a1a1a', height=120)
        gear_display_frame.pack(pady=20, fill=tk.X)
        
        tk.Label(gear_display_frame, text='CURRENT GEAR', font=('Arial', 12),
                bg='#1a1a1a', fg='#00ff00').pack()
        
        self.gear_display = tk.Label(gear_display_frame, text='N', font=('Arial', 56, 'bold'),
                                    bg='#1a1a1a', fg='#00ff00')
        self.gear_display.pack(pady=10)
    
    def create_info_panel(self, parent):
        """Create right information panel"""
        # Title
        title = tk.Label(parent, text='ENGINE DATA', font=('Arial', 14, 'bold'),
                        bg='#1a1a1a', fg='#00ff00')
        title.pack(anchor='w', padx=10, pady=10)
        
        # Performance metrics
        perf_frame = tk.LabelFrame(parent, text='PERFORMANCE', bg='#1a1a1a',
                                  fg='#00ff00', font=('Arial', 11, 'bold'))
        perf_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.torque_label = tk.Label(perf_frame, text='Torque: 0 Nm',
                                    font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.torque_label.pack(anchor='w', padx=5, pady=2)
        
        self.boost_display = tk.Label(perf_frame, text='Boost: 0.0 PSI',
                                     font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.boost_display.pack(anchor='w', padx=5, pady=2)
        
        self.throttle_label = tk.Label(perf_frame, text='Throttle: 0%',
                                      font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.throttle_label.pack(anchor='w', padx=5, pady=2)
        
        # Temperature section
        temp_frame = tk.LabelFrame(parent, text='TEMPERATURES', bg='#1a1a1a',
                                  fg='#00ff00', font=('Arial', 11, 'bold'))
        temp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.oil_temp_label = tk.Label(temp_frame, text='Oil: 20°C',
                                      font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.oil_temp_label.pack(anchor='w', padx=5, pady=2)
        
        self.coolant_temp_label = tk.Label(temp_frame, text='Coolant: 20°C',
                                          font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.coolant_temp_label.pack(anchor='w', padx=5, pady=2)
        
        self.intake_temp_label = tk.Label(temp_frame, text='Intake: 20°C',
                                         font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.intake_temp_label.pack(anchor='w', padx=5, pady=2)
        
        # Fuel section
        fuel_frame = tk.LabelFrame(parent, text='FUEL SYSTEM', bg='#1a1a1a',
                                  fg='#00ff00', font=('Arial', 11, 'bold'))
        fuel_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.fuel_level_label = tk.Label(fuel_frame, text='Level: 100.0%',
                                        font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.fuel_level_label.pack(anchor='w', padx=5, pady=2)
        
        self.fuel_consumption_label = tk.Label(fuel_frame, text='Consumption: 0.0 L/h',
                                              font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.fuel_consumption_label.pack(anchor='w', padx=5, pady=2)
        
        # Session statistics
        session_frame = tk.LabelFrame(parent, text='SESSION', bg='#1a1a1a',
                                     fg='#00ff00', font=('Arial', 11, 'bold'))
        session_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.distance_label = tk.Label(session_frame, text='Distance: 0.00 km',
                                      font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.distance_label.pack(anchor='w', padx=5, pady=2)
        
        self.runtime_label = tk.Label(session_frame, text='Runtime: 0.0 s',
                                     font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.runtime_label.pack(anchor='w', padx=5, pady=2)
        
        self.wear_label = tk.Label(session_frame, text='Engine Wear: 0.0%',
                                  font=('Courier', 10), bg='#1a1a1a', fg='#00aa00')
        self.wear_label.pack(anchor='w', padx=5, pady=2)
        
        # Reset button
        reset_btn = tk.Button(session_frame, text='RESET SESSION [R]',
                            font=('Arial', 10), bg='#333333', fg='#00ff00',
                            command=self.reset_session)
        reset_btn.pack(fill=tk.X, padx=5, pady=5)
        
        # Engine info
        info_frame = tk.LabelFrame(parent, text='ENGINE SPEC', bg='#1a1a1a',
                                  fg='#00ff00', font=('Arial', 11, 'bold'))
        info_frame.pack(fill=tk.X, padx=10, pady=5)
        
        info_text = (
            "Inline-4 2.0L Turbo\n"
            "Peak Power: 250 HP\n"
            "Peak Torque: 280 Nm\n"
            "Redline: 7200 RPM\n"
            "Max Boost: 15 PSI"
        )
        info_label = tk.Label(info_frame, text=info_text, font=('Courier', 9),
                            bg='#1a1a1a', fg='#00aa00', justify=tk.LEFT)
        info_label.pack(padx=10, pady=5, anchor='w')
    
    def setup_keybindings(self):
        """Setup keyboard controls"""
        # Engine control
        self.root.bind('e', lambda e: self.toggle_engine())
        self.root.bind('E', lambda e: self.toggle_engine())
        
        # Throttle
        self.root.bind('<space>', lambda e: self.on_throttle_press())
        self.root.bind('<KeyRelease-space>', lambda e: self.on_throttle_release())
        
        # Brake
        self.root.bind('b', lambda e: self.on_brake_press())
        self.root.bind('B', lambda e: self.on_brake_press())
        self.root.bind('<KeyRelease-b>', lambda e: self.on_brake_release())
        self.root.bind('<KeyRelease-B>', lambda e: self.on_brake_release())
        
        # Shifting
        self.root.bind('<Up>', lambda e: self.engine.shift_up())
        self.root.bind('<Down>', lambda e: self.engine.shift_down())
        
        # Clutch
        self.root.bind('c', lambda e: self.engine.toggle_clutch())
        self.root.bind('C', lambda e: self.engine.toggle_clutch())
        
        # Reset
        self.root.bind('r', lambda e: self.reset_session())
        self.root.bind('R', lambda e: self.reset_session())
    
    def toggle_engine(self):
        """Toggle engine on/off"""
        if self.engine.is_running:
            self.engine.stop_engine()
            self.start_button.config(text='START ENGINE [E]', bg='#00ff00')
        else:
            self.engine.start_engine()
            self.start_button.config(text='STOP ENGINE [E]', bg='#ff3333')
    
    def set_gear(self, gear):
        """Set transmission gear"""
        self.engine.set_gear(gear)
    
    def on_rev_limiter_change(self, value):
        """Update rev limiter"""
        rpm = int(float(value))
        self.engine.set_rev_limiter(rpm)
        self.rev_label.config(text=f'{rpm} RPM')
    
    def on_boost_change(self, value):
        """Update boost pressure"""
        psi = float(value)
        self.engine.set_boost_pressure(psi)
        self.boost_label.config(text=f'{psi:.1f} PSI')
    
    def on_throttle_press(self):
        """Throttle pressed"""
        self.throttle_pressed = True
        self.engine.set_throttle(1.0)
    
    def on_throttle_release(self):
        """Throttle released"""
        self.throttle_pressed = False
        self.engine.set_throttle(0.0)
    
    def on_brake_press(self):
        """Brake pressed"""
        self.brake_pressed = True
        self.engine.set_brake(1.0)
    
    def on_brake_release(self):
        """Brake released"""
        self.brake_pressed = False
        self.engine.set_brake(0.0)
    
    def reset_session(self):
        """Reset session statistics"""
        self.engine.reset_session()
    
    def update_display(self):
        """Update all display elements"""
        # Update main gauges
        self.rpm_gauge.update(self.engine.rpm)
        self.speed_gauge.update(abs(self.engine.speed))
        self.power_gauge.update(self.engine.power)
        
        # Update gear display
        gear_map = {-1: 'R', 0: 'N', 1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6'}
        gear_text = gear_map.get(self.engine.current_gear, 'N')
        self.gear_display.config(text=gear_text)
        
        # Color code gear display
        if self.engine.current_gear == 0:
            self.gear_display.config(fg='#ffaa00')  # Orange for neutral
        elif self.engine.current_gear == -1:
            self.gear_display.config(fg='#ff3333')  # Red for reverse
        else:
            self.gear_display.config(fg='#00ff00')  # Green for forward gears
        
        # Update performance labels
        self.torque_label.config(text=f'Torque: {self.engine.torque:.0f} Nm')
        self.boost_display.config(text=f'Boost: {self.engine.boost:.1f} PSI')
        self.throttle_label.config(text=f'Throttle: {self.engine.throttle_position*100:.0f}%')
        
        # Update temperature labels with color coding
        oil_temp = self.engine.oil_temp
        oil_color = '#00aa00' if oil_temp < 100 else ('#ffaa00' if oil_temp < 110 else '#ff3333')
        self.oil_temp_label.config(text=f'Oil: {oil_temp:.0f}°C', fg=oil_color)
        
        coolant_temp = self.engine.coolant_temp
        coolant_color = '#00aa00' if coolant_temp < 95 else ('#ffaa00' if coolant_temp < 105 else '#ff3333')
        self.coolant_temp_label.config(text=f'Coolant: {coolant_temp:.0f}°C', fg=coolant_color)
        
        self.intake_temp_label.config(text=f'Intake: {self.engine.intake_temp:.0f}°C')
        
        # Update fuel labels
        fuel_level = self.engine.fuel_level
        fuel_color = '#00aa00' if fuel_level > 25 else ('#ffaa00' if fuel_level > 10 else '#ff3333')
        self.fuel_level_label.config(text=f'Level: {fuel_level:.1f}%', fg=fuel_color)
        self.fuel_consumption_label.config(text=f'Consumption: {self.engine.fuel_consumption:.1f} L/h')
        
        # Update session labels
        self.distance_label.config(text=f'Distance: {self.engine.total_distance:.2f} km')
        self.runtime_label.config(text=f'Runtime: {self.engine.runtime:.1f} s')
        self.wear_label.config(text=f'Engine Wear: {self.engine.engine_wear:.1f}%')
    
    def simulation_loop(self):
        """Main simulation loop"""
        if not self.running:
            return
        
        # Calculate delta time
        current_time = time.time()
        delta_time = current_time - self.last_update_time
        self.last_update_time = current_time
        
        # Clamp delta time to prevent large jumps
        delta_time = min(delta_time, 0.1)
        
        # Update engine physics
        try:
            self.engine.update(delta_time)
        except Exception as e:
            print(f"Physics update error: {e}")
        
        # Update display
        try:
            self.update_display()
        except Exception as e:
            print(f"Display update error: {e}")
        
        # Schedule next update (target 60 FPS)
        self.root.after(16, self.simulation_loop)
    
    def on_closing(self):
        """Handle window close"""
        self.running = False
        try:
            self.engine.stop_engine()
        except:
            pass
        self.root.destroy()


def main():
    """Main entry point"""
    print("=" * 60)
    print("ENGINE SIMULATOR v2.0 - C++ Physics Edition")
    print("=" * 60)
    print("Loading C++ physics engine...")
    
    root = tk.Tk()
    
    try:
        app = EngineSimulatorApp(root)
        root.protocol("WM_DELETE_WINDOW", app.on_closing)
        print("✓ Application initialized successfully")
        print("=" * 60)
        root.mainloop()
    except Exception as e:
        print(f"✗ Failed to initialize application: {e}")
        print("\nMake sure engine_physics.dll is in the same folder!")
        root.destroy()


if __name__ == '__main__':
    main()