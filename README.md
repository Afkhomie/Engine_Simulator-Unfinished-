# Engine Simulator v1.3

A professional-grade engine simulation application built with Python (GUI), C++ (Physics Engine), and real-time audio synthesis.

## What's New in v1.3

### Stage 1: Core Engine Physics
- ✅ **Gradual RPM Changes**: Time-based acceleration/deceleration - RPM now rises and falls smoothly instead of jumping instantly
- ✅ **Idle RPM Stability**: Engine holds steady at 800 ± 50 RPM when throttle is closed
- ✅ **Real Power/Torque Math**: Power (kW) = (Torque × RPM) / 9549, then converted to HP
- ✅ **Gear Ratio Speed Calculation**: Speed properly linked to gear ratio × RPM

### Stage 2: Physics Consistency
- ✅ **Weight & Inertia**: Added 1400kg vehicle mass affecting acceleration
- ✅ **Gradual Boost**: PSI increases smoothly with throttle and RPM (no instant boost)
- ✅ **Realistic Temperatures**: Oil, coolant, and intake temps rise/fall gradually with proper heat transfer rates
- ✅ **Real Fuel Consumption**: Consumption based on actual throttle position, RPM, boost, and gear load

### Stage 3: User Interface Logic
- ✅ **Proper Slider Integration**: Volume, boost, and rev limiter sliders control physics directly
- ✅ **Gear Shift Logic**: RPM drops/increases realistically during shifts (no spikes)
- ✅ **Shift Delay**: 200ms shift time prevents unrealistic instant gear changes

### Stage 4: Sound & Feedback
- ✅ **Idle/Accel/Decel Sounds**: Distinct sound character for different engine states
- ✅ **Smooth Pitch Scaling**: Audio frequency interpolates smoothly with RPM
- ✅ **Deceleration Crackle**: Overrun pops/crackles at high RPM when lifting throttle
- ✅ **No Audio Popping**: Fade in/out and exponential smoothing prevent clicks

### Stage 5: Dyno Mode & Fine Tuning
- ✅ **Realistic Dyno Data**: Torque and power curves calculated with proper physics
- ✅ **Drivetrain Loss**: 15% power loss between engine and wheels
- ✅ **Temperature Performance Impact**: Overheating (>105°C) reduces power output

## Features

✅ **Real-time Physics Simulation**
- Accurate RPM calculations with physics-based acceleration
- Torque curve simulation based on engine type
- Power output calculations (HP)
- Speed calculation in km/h based on gear ratios
- Engine inertia modeling
- Rev limiter with hard cut

✅ **Engine Types**
- Inline-4 2.0L Turbo: 250 HP, 280 Nm, 7200 RPM redline
- V6 3.5L NA: 300 HP, 380 Nm, 7000 RPM redline
- V8 5.0L NA: 450 HP, 530 Nm, 7500 RPM redline
- Diesel I4 2.0L: 180 HP, 420 Nm, 5000 RPM redline
- Custom Engine Builder: Full parameter control

✅ **Transmission System**
- 6-speed manual transmission + Reverse gear
- Fully customizable gear ratios
- Neutral position (gear 0)
- Clutch simulation (engaged/disengaged states)
- Gear-specific load on engine

✅ **Forced Induction**
- Turbocharger simulation with RPM-based spool
- Supercharger simulation (instant boost)
- Adjustable boost pressure (0-25 PSI)
- Boost multiplier on torque output
- Real-time boost gauge

✅ **Fuel System**
- Fuel level tracking (percentage)
- Real-time fuel consumption (L/h)
- Consumption varies by engine load, RPM, engine type, and fuel type
- Fuel range estimation (km remaining)
- Visual fuel bar with gradient
- 4 fuel types: Regular (87), Premium (93), E85 (105), Diesel

✅ **Temperature Simulation**
- Oil Temperature: Rises with throttle/RPM, cools passively
- Coolant Temperature: Engine heat dissipation
- Intake Air Temperature: Affected by boost pressure
- All temperatures in °Celsius
- Warning system for overheating

✅ **Performance Metrics**
- 0-100 km/h timer: Automatic acceleration tracking
- Quarter-mile timer: 402m performance measurement
- Real-time torque display (Nm)
- Real-time power display (HP)
- Real-time boost display (PSI)

✅ **Audio Engine**
- Real-time sound synthesis
- Engine rumble: Low-frequency oscillator based on RPM
- Exhaust note: Mid-frequency square wave (throttle-dependent)
- Turbo whistle: High-frequency sine wave (boost-dependent)
- Dynamic frequency based on cylinder count
- Volume adjustable (0-100%)

✅ **Visual Displays**
- RPM Gauge: Large digital display + progress bar
- Speed Gauge: km/h with progress bar
- Power Gauge: HP display
- Gear Indicator: Large animated display (R, N, 1-6)
- Fuel Bar: Visual percentage with gradient
- All gauges update at 60 FPS

✅ **Professional UI**
- Dark mode with glassmorphic design
- 4 Pages: Simulator, Builder, Dyno, Info
- Responsive 3-column layout
- Animated backgrounds and visual effects
- Keyboard hint overlay
- Warning system with color-coded alerts

## System Requirements

- **Windows 10/11** (64-bit)
- **Python 3.8+**
- **C++ Compiler** (MSVC, MinGW, or Clang)
- **RAM**: 2GB minimum
- **Disk Space**: 500MB

## Installation

### 1. Install Python Dependencies

```bash
pip install numpy
pip install sounddevice  # For audio support
```

### 2. Compile C++ Physics Engine

#### Option A: Using Microsoft Visual C++ (Recommended)

```bash
# Open Visual Studio Command Prompt and navigate to the project directory
cl.exe /LD engine_physics.cpp engine_physics_wrapper.cpp /Fe:engine_physics.dll
```

#### Option B: Using MinGW

```bash
g++ -shared -fPIC -O3 engine_physics.cpp engine_physics_wrapper.cpp -o engine_physics.dll
```

#### Option C: Using Clang

```bash
clang++ -shared -O3 engine_physics.cpp engine_physics_wrapper.cpp -o engine_physics.dll
```

### 3. Run the Application

```bash
python main_app.py
```

## Keyboard Controls

| Key | Action |
|-----|--------|
| **E** | Start/Stop Engine |
| **SPACE** | Throttle (hold for acceleration) |
| **B** | Brake (hold for deceleration) |
| **SHIFT** | Gear Up |
| **CTRL** | Gear Down |
| **BACKSPACE** | Toggle Clutch |
| **D** | Dyno View |
| **G** | Builder View |
| **I** | Info View |

## File Structure

```
Engine Simulator/
├── main_app.py              # Main GUI application
├── engine_physics.h         # C++ header (physics engine)
├── engine_physics.cpp       # C++ implementation (physics engine)
├── engine_physics_wrapper.cpp # C++ DLL wrapper
├── engine_wrapper.py        # Python wrapper for C++
├── audio_engine.py          # Real-time audio synthesis
├── engine_physics.dll       # Compiled physics engine (generated)
├── README.md                # This file
└── BUILD.md                 # Detailed build instructions
```

## Technical Details

### Architecture

- **GUI Layer**: tkinter (Python)
- **Physics Engine**: C++ with ctypes bindings
- **Audio Synthesis**: NumPy + sounddevice
- **Update Rate**: 60 FPS (16ms per frame)
- **Physics Timestep**: Delta-time based (frame-rate independent)

### Physics Model

1. **Torque Curve**: Parabolic model based on RPM
   - Peak torque varies by engine type
   - Falls off near redline
   - Boosted by turbocharger/supercharger

2. **Power Calculation**: Power = (Torque × RPM) / 7121

3. **Speed Calculation**: 
   - Based on wheel RPM from engine RPM / gear ratio
   - Accounts for wheel diameter and final drive ratio

4. **Fuel Consumption**: 
   - Base consumption modified by RPM, throttle, and gear load
   - Higher consumption at high RPM and full throttle

5. **Temperature Management**:
   - Oil temp rises with load, cools when off
   - Coolant temp affects engine performance
   - Intake temp affected by boost pressure

### Performance Tracking

- **0-100 km/h Time**: Automatic timing when acceleration starts
- **Quarter-Mile**: Tracks distance to 402m milestone
- **Distance Traveled**: Cumulative km
- **Runtime**: Total engine-on time

## Troubleshooting

### Issue: "Could not load engine_physics.dll"

**Solution**: Compile the C++ code as shown above. The application will fall back to pure Python engine physics if the DLL is not available (slower).

### Issue: No audio output

**Solution**: sounddevice is required for audio. Install with: `pip install sounddevice`
The application will work without audio - it will just show visual-only mode.

Note: sounddevice is easier to install than PyAudio and works across all platforms without additional compilation.

### Issue: Low FPS or performance issues

**Solution**: 
1. Close other applications
2. Ensure graphics drivers are updated
3. Consider using the C++ physics engine instead of pure Python

## Advanced Configuration

### Custom Engine Creation

In the Builder page, you can customize:
- Displacement (0.5L - 10L)
- Cylinder Count (1-16)
- Peak Torque (50-1000 Nm)
- Peak Power (50-2000 HP)
- Idle RPM (500-2000)
- Redline RPM (3000-12000)

### Tuning Parameters

- **Rev Limiter**: Adjustable from 3000-9000 RPM
- **Boost Pressure**: 0-25 PSI
- **Volume Control**: 0-100%
- **Launch Control**: Toggle for smooth starts

## Performance Metrics

- **Lines of Code**: ~2000+ (C++ + Python + Audio)
- **Engine Presets**: 5 (4 presets + custom)
- **Adjustable Parameters**: 20+
- **Real-time Metrics**: 15+
- **Keyboard Shortcuts**: 8+

## Changelog

### v1.3 (Current)
- **Stage 1**: Gradual RPM changes, idle stability, proper power/torque formulas
- **Stage 2**: Vehicle weight/inertia, gradual boost/temps, realistic fuel consumption
- **Stage 3**: Gear shift logic with RPM drop, proper slider integration
- **Stage 4**: Improved audio with idle/accel/decel mapping, smooth transitions
- **Stage 5**: Enhanced dyno mode with drivetrain loss and temperature effects

### v1.2
- Fixed audio callback logic to properly check `is_running` flag
- Added frequency bounds checking (min 20 Hz for rumble, 100 Hz for exhaust)
- Improved error handling in audio callback with try-catch
- Better error messages in engine wrapper fallback
- Enhanced volume parameter clamping in audio callback
- Optimized physics update loop

### v1.0
- Initial release with full feature set

## Future Enhancements

- [ ] Custom transmission builder
- [ ] Engine damage system
- [ ] Multiplayer network support
- [ ] VR compatibility
- [ ] Advanced telemetry recording
- [ ] Replay system
- [ ] Advanced dyno graphs with matplotlib
- [ ] Multiple engine sound profiles
- [ ] Anti-lag and traction control simulation

## Credits

**Development Team**: Engine Simulator Development Team
**Version**: 1.3
**Release Date**: 2025
**Last Updated**: October 24, 2025

## License

This project is provided as-is for educational and personal use.

## Support

For issues, feature requests, or contributions, please refer to the project repository.

---

**Enjoy your Engine Simulation Experience! 🏎️**
