# Engine Simulator - Quick Start Guide

## 📋 Prerequisites

- **Python 3.8 or higher**
- **NumPy** (`pip install numpy`)
- **PyAudio** (optional, for audio) (`pip install pyaudio`)

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies
```bash
pip install numpy
pip install pyaudio  # Optional but recommended
```

### Step 2: Compile C++ Engine (Optional but Recommended)
The app will work without this, but performance will be better with compilation.

**Windows with Visual Studio:**
```bash
cd "C:\Users\Prakash\OneDrive\Desktop\Engine SImulator"
cl.exe /LD /O2 engine_physics.cpp engine_physics_wrapper.cpp /Fe:engine_physics.dll
```

**Windows with MinGW:**
```bash
g++ -shared -fPIC -O3 engine_physics.cpp engine_physics_wrapper.cpp -o engine_physics.dll
```

### Step 3: Run the Application
```bash
python main_app.py
```

**Or use the launcher (handles compilation automatically):**
```bash
python launch.py
```

## 🎮 First Time Using the Simulator

1. **Start the engine**: Press **E** or click "START ENGINE"
2. **Apply throttle**: Hold **SPACE** to accelerate
3. **Shift gears**: Press **SHIFT** to go up, **CTRL** to go down
4. **Brake**: Press **B** to decelerate
5. **Toggle clutch**: Press **BACKSPACE** before shifting

## 📊 UI Overview

### Main Simulator Page (Default)
- **Left Panel**: Engine controls (start, gears, rev limiter, boost, volume)
- **Center Panel**: Main gauges (RPM, Speed, Power, Gear display)
- **Right Panel**: Engine information (torque, temperature, fuel, performance)

### Navigation
- Press **D** to view Dyno graphs
- Press **G** to access Custom Engine Builder
- Press **I** for Information page
- Or use buttons at the bottom of right panel

## ⌨️ Keyboard Controls Cheat Sheet

| Key | Action |
|-----|--------|
| **E** | Start/Stop Engine |
| **SPACE** | Throttle |
| **B** | Brake |
| **SHIFT** | Gear Up |
| **CTRL** | Gear Down |
| **BACKSPACE** | Toggle Clutch |
| **D** | Dyno View |
| **G** | Builder View |
| **I** | Info View |

## 🎯 Tips for Beginners

1. **Always engage clutch before shifting**: Press BACKSPACE before using SHIFT/CTRL
2. **Smooth acceleration**: Hold SPACE gradually, don't slam throttle
3. **Avoid over-revving**: Watch the red zone on the RPM gauge
4. **Monitor temperatures**: Keep oil and coolant temps in the green zone
5. **Fuel consumption**: At full throttle, fuel depletes quickly

## 🔧 Performance Modes

### With C++ Engine (Fast)
- Compiled DLL available
- Smooth 60 FPS operation
- Best physics accuracy
- ~0.5ms per frame

### Pure Python Mode (Slower)
- DLL not found or compilation skipped
- Still playable but may have frame rate dips
- Physics calculations slower
- ~2-5ms per frame

## 🐛 Troubleshooting

### "Could not load engine_physics.dll"
- **Normal!** App works fine in Python mode
- To enable C++ mode, compile using Step 2 above

### Audio not working
- PyAudio not installed: `pip install pyaudio`
- On some systems, audio dependencies need to be installed separately
- App works fine without audio (visual only)

### Low FPS/Lag
- Close other applications
- Reduce screen resolution if needed
- C++ mode will significantly improve performance

### Can't compile C++ code
- Install **Visual Studio Community** (free) or
- Install **MinGW-w64** for Windows

## 📈 Understanding the Gauges

- **RPM**: Engine revolutions per minute (higher = more power)
- **Speed**: Vehicle speed in km/h
- **Power**: Horsepower output in real-time
- **Torque**: Engine turning force in Newton-meters
- **Boost**: Turbocharger/supercharger boost pressure in PSI
- **Oil/Coolant Temp**: Engine temperature (green=ok, yellow=warning, red=overheat)
- **Fuel**: Tank level percentage

## 🎓 Physics Basics

- **Torque**: Peak torque varies by engine type and RPM
- **Power**: Calculated from torque × RPM / 7121
- **Speed**: Depends on engine RPM, gear ratio, and wheel size
- **Fuel Consumption**: Higher at full throttle and high RPM
- **Temperature**: Rises during hard acceleration, cools when off

## 🏆 Performance Challenges

Try these challenges to test your skills:

1. **0-100 km/h Sprint**: Quick acceleration from stop
2. **Smooth Acceleration**: Minimal wheel spin, efficient gear changes
3. **Fuel Economy**: Drive 10 km using least fuel
4. **Temperature Management**: Keep temps in green while accelerating hard

## 📞 Need Help?

1. Check README.md for detailed information
2. Review keyboard controls with **I** key (Info page)
3. Experiment with different settings in the Builder page
4. Check BUILD.md for compilation help

---

**Enjoy driving! 🏎️**
