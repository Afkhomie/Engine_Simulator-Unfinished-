import ctypes
import os
import time

# Load the DLL with full path
dll_path = os.path.abspath("engine_physics.dll")
dll = ctypes.CDLL(dll_path)

# Define function signatures based on exported functions
# Constructor/Destructor
dll.EnginePhysics_new.restype = ctypes.c_void_p
dll.EnginePhysics_delete.argtypes = [ctypes.c_void_p]

# Control functions
dll.EnginePhysics_startEngine.argtypes = [ctypes.c_void_p]
dll.EnginePhysics_stopEngine.argtypes = [ctypes.c_void_p]
dll.EnginePhysics_setThrottle.argtypes = [ctypes.c_void_p, ctypes.c_double]
dll.EnginePhysics_setGear.argtypes = [ctypes.c_void_p, ctypes.c_int]
dll.EnginePhysics_update.argtypes = [ctypes.c_void_p, ctypes.c_double]

# Getter functions
dll.EnginePhysics_getRPM.argtypes = [ctypes.c_void_p]
dll.EnginePhysics_getRPM.restype = ctypes.c_double

dll.EnginePhysics_getSpeed.argtypes = [ctypes.c_void_p]
dll.EnginePhysics_getSpeed.restype = ctypes.c_double

dll.EnginePhysics_getCurrentGear.argtypes = [ctypes.c_void_p]
dll.EnginePhysics_getCurrentGear.restype = ctypes.c_int

dll.EnginePhysics_isEngineRunning.argtypes = [ctypes.c_void_p]
dll.EnginePhysics_isEngineRunning.restype = ctypes.c_bool

print("="*60)
print("ENGINE SIMULATOR - NEUTRAL RPM ACCELERATION TEST")
print("="*60)

# Create engine instance
engine = dll.EnginePhysics_new()
print(f"✓ Engine instance created: {hex(engine)}")

# Start engine
dll.EnginePhysics_startEngine(engine)
time.sleep(0.1)  # Let it settle

if dll.EnginePhysics_isEngineRunning(engine):
    print("✓ Engine started successfully")
else:
    print("✗ Engine failed to start")
    dll.EnginePhysics_delete(engine)
    exit(1)

# Set to neutral (gear 0)
dll.EnginePhysics_setGear(engine, 0)
print(f"✓ Gear set to: {dll.EnginePhysics_getCurrentGear(engine)}")

# Full throttle
dll.EnginePhysics_setThrottle(engine, 1.0)
print("✓ Throttle: 100%")
print("-"*60)
print("Time (s) | RPM      | Speed (km/h)")
print("-"*60)

# Run simulation
start_time = time.time()
dt = 0.016  # ~60 FPS simulation step
redline = 7000  # Adjust to your engine's redline

try:
    while True:
        elapsed = time.time() - start_time
        
        # Update physics
        dll.EnginePhysics_update(engine, dt)
        
        # Get current state
        rpm = dll.EnginePhysics_getRPM(engine)
        speed = dll.EnginePhysics_getSpeed(engine)
        
        # Print every 0.1 seconds
        if int(elapsed * 10) != int((elapsed - dt) * 10):
            print(f"{elapsed:7.2f}  | {rpm:7.0f}  | {speed:7.2f}")
        
        # Stop at redline
        if rpm >= redline:
            print("-"*60)
            print(f"✓ REDLINE REACHED at {elapsed:.2f}s")
            print(f"  Final RPM: {rpm:.0f}")
            break
        
        # Safety timeout
        if elapsed > 30:
            print("-"*60)
            print("✗ Timeout after 30 seconds")
            break
        
        time.sleep(dt)

except KeyboardInterrupt:
    print("\n" + "-"*60)
    print("✗ Test interrupted by user")

# Cleanup
dll.EnginePhysics_stopEngine(engine)
dll.EnginePhysics_delete(engine)
print("✓ Engine stopped and cleaned up")
print("="*60)