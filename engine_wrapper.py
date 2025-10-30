"""
Python wrapper for C++ Engine Physics using ctypes
"""
import ctypes
import os
from ctypes import c_double, c_int, c_bool, c_void_p, POINTER
from pathlib import Path

# Determine the path to the compiled DLL
current_dir = Path(__file__).parent
dll_path = current_dir / "engine_physics.dll"

try:
    engine_lib = ctypes.CDLL(str(dll_path))
except OSError:
    print(f"Warning: Could not load {dll_path}")
    print("Make sure to compile engine_physics.cpp to engine_physics.dll")
    engine_lib = None

# Define the return types and argument types for C++ functions
if engine_lib:
    # Constructor and destructor
    engine_lib.EnginePhysics_new.restype = c_void_p
    engine_lib.EnginePhysics_delete.argtypes = [c_void_p]
    
    # Core control methods
    engine_lib.EnginePhysics_startEngine.argtypes = [c_void_p]
    engine_lib.EnginePhysics_stopEngine.argtypes = [c_void_p]
    engine_lib.EnginePhysics_setThrottle.argtypes = [c_void_p, c_double]
    engine_lib.EnginePhysics_setBrake.argtypes = [c_void_p, c_double]
    engine_lib.EnginePhysics_shiftUp.argtypes = [c_void_p]
    engine_lib.EnginePhysics_shiftDown.argtypes = [c_void_p]
    engine_lib.EnginePhysics_toggleClutch.argtypes = [c_void_p]
    engine_lib.EnginePhysics_setGear.argtypes = [c_void_p, c_int]
    
    # Configuration methods
    engine_lib.EnginePhysics_setRevLimiter.argtypes = [c_void_p, c_int]
    engine_lib.EnginePhysics_setBoostPressure.argtypes = [c_void_p, c_double]
    
    # Update simulation
    engine_lib.EnginePhysics_update.argtypes = [c_void_p, c_double]
    
    # Getters (all return double or int)
    engine_lib.EnginePhysics_getRPM.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getRPM.restype = c_double
    
    engine_lib.EnginePhysics_getSpeed.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getSpeed.restype = c_double
    
    engine_lib.EnginePhysics_getTorque.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getTorque.restype = c_double
    
    engine_lib.EnginePhysics_getPower.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getPower.restype = c_double
    
    engine_lib.EnginePhysics_getBoost.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getBoost.restype = c_double
    
    engine_lib.EnginePhysics_getCurrentGear.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getCurrentGear.restype = c_int
    
    engine_lib.EnginePhysics_isEngineRunning.argtypes = [c_void_p]
    engine_lib.EnginePhysics_isEngineRunning.restype = c_bool
    
    engine_lib.EnginePhysics_getOilTemp.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getOilTemp.restype = c_double
    
    engine_lib.EnginePhysics_getCoolantTemp.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getCoolantTemp.restype = c_double
    
    engine_lib.EnginePhysics_getIntakeTemp.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getIntakeTemp.restype = c_double
    
    engine_lib.EnginePhysics_getFuelLevel.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getFuelLevel.restype = c_double
    
    engine_lib.EnginePhysics_getFuelConsumption.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getFuelConsumption.restype = c_double
    
    engine_lib.EnginePhysics_getEngineWear.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getEngineWear.restype = c_double
    
    engine_lib.EnginePhysics_getBest0To100Time.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getBest0To100Time.restype = c_double
    
    engine_lib.EnginePhysics_getTotalDistance.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getTotalDistance.restype = c_double
    
    engine_lib.EnginePhysics_getRuntime.argtypes = [c_void_p]
    engine_lib.EnginePhysics_getRuntime.restype = c_double
    
    engine_lib.EnginePhysics_resetSession.argtypes = [c_void_p]


class EnginePhysics:
    """Python wrapper for C++ EnginePhysics class"""
    
    def __init__(self):
        if engine_lib is None:
            raise RuntimeError("Engine library not loaded. Using pure Python implementation.")
        try:
            self.engine = engine_lib.EnginePhysics_new()
        except Exception as e:
            raise RuntimeError(f"Failed to create engine instance: {e}")
    
    def __del__(self):
        if hasattr(self, 'engine') and engine_lib:
            engine_lib.EnginePhysics_delete(self.engine)
    
    # Control methods
    def start_engine(self):
        engine_lib.EnginePhysics_startEngine(self.engine)
    
    def stop_engine(self):
        engine_lib.EnginePhysics_stopEngine(self.engine)
    
    def set_throttle(self, throttle):
        engine_lib.EnginePhysics_setThrottle(self.engine, c_double(throttle))
    
    def set_brake(self, brake):
        engine_lib.EnginePhysics_setBrake(self.engine, c_double(brake))
    
    def shift_up(self):
        engine_lib.EnginePhysics_shiftUp(self.engine)
    
    def shift_down(self):
        engine_lib.EnginePhysics_shiftDown(self.engine)
    
    def toggle_clutch(self):
        engine_lib.EnginePhysics_toggleClutch(self.engine)
    
    def set_gear(self, gear):
        engine_lib.EnginePhysics_setGear(self.engine, c_int(gear))
    
    # Configuration
    def set_rev_limiter(self, rpm):
        engine_lib.EnginePhysics_setRevLimiter(self.engine, c_int(rpm))
    
    def set_boost_pressure(self, psi):
        engine_lib.EnginePhysics_setBoostPressure(self.engine, c_double(psi))
    
    # Simulation
    def update(self, delta_time):
        engine_lib.EnginePhysics_update(self.engine, c_double(delta_time))
    
    # Getters
    @property
    def rpm(self):
        return engine_lib.EnginePhysics_getRPM(self.engine)
    
    @property
    def speed(self):
        return engine_lib.EnginePhysics_getSpeed(self.engine)
    
    @property
    def torque(self):
        return engine_lib.EnginePhysics_getTorque(self.engine)
    
    @property
    def power(self):
        return engine_lib.EnginePhysics_getPower(self.engine)
    
    @property
    def boost(self):
        return engine_lib.EnginePhysics_getBoost(self.engine)
    
    @property
    def current_gear(self):
        return engine_lib.EnginePhysics_getCurrentGear(self.engine)
    
    @property
    def is_running(self):
        return engine_lib.EnginePhysics_isEngineRunning(self.engine)
    
    @property
    def oil_temp(self):
        return engine_lib.EnginePhysics_getOilTemp(self.engine)
    
    @property
    def coolant_temp(self):
        return engine_lib.EnginePhysics_getCoolantTemp(self.engine)
    
    @property
    def intake_temp(self):
        return engine_lib.EnginePhysics_getIntakeTemp(self.engine)
    
    @property
    def fuel_level(self):
        return engine_lib.EnginePhysics_getFuelLevel(self.engine)
    
    @property
    def fuel_consumption(self):
        return engine_lib.EnginePhysics_getFuelConsumption(self.engine)
    
    @property
    def engine_wear(self):
        return engine_lib.EnginePhysics_getEngineWear(self.engine)
    
    @property
    def best_0_100_time(self):
        return engine_lib.EnginePhysics_getBest0To100Time(self.engine)
    
    @property
    def total_distance(self):
        return engine_lib.EnginePhysics_getTotalDistance(self.engine)
    
    @property
    def runtime(self):
        return engine_lib.EnginePhysics_getRuntime(self.engine)
    
    def reset_session(self):
        engine_lib.EnginePhysics_resetSession(self.engine)


# Fallback pure-Python implementation for testing without C++ compilation
class EnginePhysicsPython:
    """Pure Python fallback implementation for engine physics"""
    
    def __init__(self):
        self.rpm = 0
        self.target_rpm = 800
        self.speed = 0
        self.throttle = 0
        self.gear = 0  # 0=neutral, 1-6=forward, -1=reverse
        self.clutch_engaged = True
        self.is_running = False
        self.is_shifting = False
        self.shift_timer = 0.0
        
        self.torque = 0
        self.power = 0
        self.boost = 0
        self.target_boost = 0
        self.max_boost = 15
        
        self.oil_temp = 20
        self.coolant_temp = 20
        self.intake_temp = 20
        
        self.fuel_level = 100
        self.fuel_consumption = 0
        self.engine_wear = 0
        
        self.best_0_100_time = 0
        self.total_distance = 0
        self.runtime = 0
        
        # Engine characteristics
        self.redline = 7200
        self.peak_torque = 280
        self.peak_power = 250
        self.idle_rpm = 800
        self.vehicle_mass = 1400
    
    def start_engine(self):
        if self.fuel_level > 0:
            self.is_running = True
            self.rpm = 800
            self.target_rpm = 800
    
    def stop_engine(self):
        self.is_running = False
        self.rpm = 0
        self.throttle = 0
    
    def set_throttle(self, throttle):
        self.throttle = max(0, min(1, throttle))
        if self.is_running:
            if self.throttle < 0.05:
                self.target_rpm = self.idle_rpm  # Idle stability
            else:
                self.target_rpm = self.idle_rpm + self.throttle * (self.redline - self.idle_rpm)
    
    def set_brake(self, brake):
        brake = max(0, min(1, brake))
        if brake > 0:
            self.speed = max(0, self.speed - brake * 50 * 0.016)
    
    def shift_up(self):
        if self.clutch_engaged and self.gear < 6 and not self.is_shifting:
            old_gear = self.gear
            self.gear += 1
            self.is_shifting = True
            self.shift_timer = 0.2
            # RPM drop on upshift
            if old_gear > 0 and self.gear > 0:
                gear_ratios = [3.36, 2.07, 1.43, 1.00, 0.84, 0.56]
                self.rpm *= gear_ratios[self.gear-1] / gear_ratios[old_gear-1]
                self.target_rpm *= gear_ratios[self.gear-1] / gear_ratios[old_gear-1]
    
    def shift_down(self):
        if self.clutch_engaged and self.gear > -1 and not self.is_shifting:
            old_gear = self.gear
            self.gear -= 1
            self.is_shifting = True
            self.shift_timer = 0.2
            # RPM increase on downshift
            if old_gear > 0 and self.gear > 0:
                gear_ratios = [3.36, 2.07, 1.43, 1.00, 0.84, 0.56]
                self.rpm *= gear_ratios[self.gear-1] / gear_ratios[old_gear-1]
                self.target_rpm *= gear_ratios[self.gear-1] / gear_ratios[old_gear-1]
                if self.rpm > self.redline:
                    self.rpm = self.redline
                    self.target_rpm = self.redline
    
    def toggle_clutch(self):
        self.clutch_engaged = not self.clutch_engaged
    
    def set_gear(self, gear):
        if -1 <= gear <= 6:
            self.gear = gear
    
    def set_rev_limiter(self, rpm):
        self.redline = max(3000, min(12000, rpm))
    
    def set_boost_pressure(self, psi):
        self.max_boost = max(0, min(25, psi))
    
    def update(self, delta_time):
        # Handle gear shift delay
        if self.is_shifting:
            self.shift_timer -= delta_time
            if self.shift_timer <= 0:
                self.is_shifting = False
                self.shift_timer = 0
        
        if not self.is_running and self.rpm > 0:
            spindown_rate = 300 + (self.rpm * 0.2)
            self.rpm = max(0, self.rpm - spindown_rate * delta_time)
        elif self.is_running:
            rpm_diff = self.target_rpm - self.rpm
            
            if self.gear == 0:
                self.rpm += rpm_diff * 6.0 * delta_time
            else:
                mass_factor = self.vehicle_mass / 1000.0
                accel_rate = 2.5 / mass_factor
                self.rpm += rpm_diff * accel_rate * delta_time
            
            # Idle stability
            if self.throttle < 0.05 and abs(self.rpm - self.idle_rpm) < 50:
                self.rpm = self.idle_rpm + (hash(str(self.runtime)) % 20 - 10)
            
            if self.rpm > self.redline:
                self.rpm = self.redline
                self.target_rpm = self.redline * 0.95
            
            self.runtime += delta_time
        
        # Gradual boost update
        if self.is_running and self.throttle > 0.1:
            rpm_factor = max(0, (self.rpm - 2000) / (self.redline - 2000))
            self.target_boost = self.max_boost * rpm_factor * self.throttle
        else:
            self.target_boost = 0
        
        boost_rate = 3.0 if self.target_boost > self.boost else 6.0
        self.boost += (self.target_boost - self.boost) * boost_rate * delta_time
        self.boost = max(0, min(self.max_boost, self.boost))
        
        # Update torque and power with boost
        if self.rpm > 0:
            rpm_ratio = self.rpm / 3500
            torque_mult = 0.3 + 0.7 * min(rpm_ratio, 1.0)
            boost_mult = 1.0 + (self.boost / 14.7) * 0.6
            self.torque = self.peak_torque * torque_mult * self.throttle * boost_mult
            # Correct power formula: Power(kW) = Torque * RPM / 9549, then convert to HP
            power_kw = (self.torque * self.rpm) / 9549.0
            self.power = power_kw * 1.341
        
        # Realistic fuel consumption
        if self.is_running:
            rpm_factor = self.rpm / self.redline
            throttle_factor = 0.2 + self.throttle * self.throttle * 0.8
            boost_factor = 1.0 + (self.boost / self.max_boost) * 0.6
            self.fuel_consumption = 8.0 * rpm_factor * throttle_factor * boost_factor
            fuel_used = (self.fuel_consumption * delta_time) / 3600.0
            self.fuel_level = max(0, self.fuel_level - (fuel_used / 50.0) * 100.0)
        
        # Gradual temperature update
        if self.is_running:
            load_factor = (self.rpm / self.redline) * self.throttle
            target_oil = 20 + load_factor * 80 + (self.rpm / self.redline) * 20
            target_coolant = 20 + load_factor * 60 + (self.rpm / self.redline) * 15
            target_intake = 20 + load_factor * 25 + self.boost * 3.5
            
            self.oil_temp += (target_oil - self.oil_temp) * 0.15 * delta_time
            self.coolant_temp += (target_coolant - self.coolant_temp) * 0.12 * delta_time
            self.intake_temp += (target_intake - self.intake_temp) * 0.25 * delta_time
        else:
            self.oil_temp += (20 - self.oil_temp) * 0.1 * delta_time
            self.coolant_temp += (20 - self.coolant_temp) * 0.15 * delta_time
            self.intake_temp += (20 - self.intake_temp) * 0.3 * delta_time
        
        # Speed update (simplified)
        if self.gear > 0 and self.clutch_engaged and self.is_running:
            gear_ratio = [3.36, 2.07, 1.43, 1.00, 0.84, 0.56][self.gear - 1]
            self.speed = (self.rpm * 0.65 * 3.14159 * 60) / (1000 * gear_ratio * 3.73)
        
        # Distance tracking
        if self.speed > 0:
            self.total_distance += (self.speed * delta_time) / 3600.0
    
    def reset_session(self):
        self.total_distance = 0
        self.runtime = 0
        self.best_0_100_time = 0
        self.engine_wear = 0
        self.fuel_level = 100
    
    @property
    def current_gear(self):
        return self.gear


# Try to use C++ version, fall back to Python
def get_engine_physics():
    try:
        return EnginePhysics()
    except:
        print("Using pure Python engine physics (compile C++ for better performance)")
        return EnginePhysicsPython()
