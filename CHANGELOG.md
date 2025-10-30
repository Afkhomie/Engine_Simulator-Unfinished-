# Changelog - Engine Simulator

All notable changes to the Engine Simulator project are documented in this file.

## [1.3] - 2025-10-24

### Major Upgrade: Physics Realism & Simulation Quality

This release transforms the engine simulator from a "glorified tachometer" into a realistic physics simulation.

#### Stage 1: Core Engine Physics

**Added**
- Time-based RPM acceleration/deceleration (gradual rise/fall instead of instant jumps)
- Idle RPM stability system (holds 800 ± 50 RPM with realistic fluctuation)
- Proper power calculation: Power(kW) = (Torque × RPM) / 9549, converted to HP
- Gear ratio-based speed calculation linked to actual physics
- RPM acceleration rate affected by engine inertia and throttle position

**Changed**
- RPM response now varies by gear (neutral = fast, in-gear = slower due to vehicle mass)
- Spindown rate when engine off now proportional to current RPM (higher RPM = faster spindown)
- Rev limiter now drops RPM slightly below redline instead of hard stop

#### Stage 2: Physics Consistency

**Added**
- Vehicle mass property (1400 kg) affecting acceleration calculations
- Drivetrain loss simulation (15% power loss between engine and wheels)
- Drag coefficient and rolling resistance properties
- Gradual boost spool: turbo spools up slower, spools down faster
- Temperature-based performance degradation (>105°C coolant reduces power by up to 30%)

**Changed**
- Boost PSI increases gradually with throttle and RPM (no instant boost)
- Oil temperature: slow heating, slower cooling
- Coolant temperature: moderate heat/cool rates
- Intake temperature: affected by boost compression (more boost = hotter intake)
- Fuel consumption now based on real physics: throttle^2, RPM, boost, gear load
- Fuel consumption increases significantly with boost (up to 60% more at max boost)

#### Stage 3: User Interface Logic

**Added**
- Gear shift delay (200-250ms) prevents instant gear changes
- RPM drop/increase during shifts based on gear ratio differences
- Shift prevention when already shifting (is_shifting flag)
- Over-rev protection on downshifts

**Changed**
- Sliders (volume, boost, rev limiter) now directly control physics engine
- RPM adjusts automatically during gear changes (no unrealistic spikes)
- Neutral shifts cause RPM to settle to idle

#### Stage 4: Sound & Feedback

**Added**
- Idle detection (distinct sound character at <1000 RPM, <10% throttle)
- Deceleration crackle/pop effects at high RPM when throttle closes
- Subharmonic bass frequencies at higher RPM for deeper sound
- Firing order variation (4-cylinder pattern simulation)
- Fade in/out envelopes to prevent audio clicking

**Changed**
- Audio frequency smoothing with exponential interpolation (prevents popping)
- Throttle affects exhaust note intensity
- Turbo whistle only audible under boost (intensity scales with boost pressure)
- Volume transitions smoothly (no sudden changes)
- Multiple harmonic layers for exhaust note (1st, 2nd harmonics)

#### Stage 5: Dyno Mode & Fine Tuning

**Added**
- Drivetrain loss calculation in dyno display
- Wheel power calculation (engine power - 15% drivetrain loss)
- Temperature warning in dyno mode
- Vehicle mass display

**Changed**
- Dyno info shows realistic wheel power vs engine power
- Power/torque curves use corrected formula (Power = Torque × RPM / 9549)

### Technical Improvements

**C++ Engine (engine_physics.cpp)**
- Added VehicleConfig struct with mass, drivetrain loss, drag, rolling resistance
- Added shift_timer and is_shifting state variables
- Enhanced updateBoost() with separate spool-up/spool-down rates
- Enhanced updateTemperatures() with realistic heat transfer coefficients
- Rewrote calculateFuelConsumption() with BSFC approximation
- Modified shiftUp(), shiftDown(), setGear() with RPM adjustment logic

**Python Fallback (engine_wrapper.py)**
- Updated EnginePhysicsPython class with all C++ improvements
- Added gradual boost update logic
- Added gear shift RPM adjustment
- Added vehicle mass property
- Proper power formula implementation

**Audio Engine (audio_engine.py)**
- Added smooth transition parameters (prev_rumble_freq, etc.)
- Added state tracking (current_rpm, current_throttle, is_idle)
- Exponential smoothing for frequency updates (smooth_factor = 0.3)
- Frequency bounds: rumble 20-300 Hz, exhaust 100-2000 Hz, turbo 1500-5000 Hz
- Added idle detection and special idle mixing
- Added deceleration crackle effect

### Bug Fixes
- Fixed instant RPM jumps during throttle changes
- Fixed unrealistic RPM spikes when shifting gears
- Fixed instant boost response on supercharged engines
- Fixed audio popping during rapid RPM changes
- Fixed temperature not affecting performance
- Fixed fuel consumption being arbitrary instead of physics-based

### Performance
- Maintained 60 FPS with all new physics calculations
- Optimized audio smoothing to prevent excessive CPU usage
- Efficient gear shift delay implementation

---

## [1.2] - 2025-10-24

### Fixed
- **Audio Callback Logic**: Fixed condition in `audio_callback()` to properly check `is_running` flag before processing commands
- **Audio Parameter Bounds**: Added minimum frequency bounds for engine rumble (20 Hz) and exhaust (100 Hz) to prevent invalid values
- **Audio Error Handling**: Added try-catch block in audio callback to handle exceptions gracefully and prevent audio stream crashes
- **Volume Clamping**: Improved volume parameter validation with proper min/max clamping in the audio callback
- **Engine Wrapper Error Messages**: Better error messaging when engine library fails to load
- **Physics Fallback**: Improved fallback to pure Python physics engine with clearer diagnostic messages

### Changed
- Updated version string to "1.2" throughout application
- Modified info page to show "Engine Simulator v1.2" 
- Updated README with v1.2 features and changelog
- Enhanced keyboard hints in info page
- Improved error handling in main application initialization

### Added
- Added error handling for audio engine initialization
- Added error handling for physics engine initialization
- Added version tracking in app instance (`self.version`)
- Added frequency bounds checking in audio synthesis
- Added changelog documentation

### Performance
- Optimized audio callback to reduce computational overhead
- Improved physics update loop efficiency

### Known Issues
- C++ DLL compilation requires manual compilation (not automatic)
- PyAudio is optional but recommended for audio features

---

## [1.0] - 2025-10-23

### Initial Release
- Complete GUI application with tkinter
- Real-time physics simulation (Pure Python + Optional C++)
- Multiple engine presets (4 presets + custom builder)
- Transmission system with 6-speed manual + reverse
- Turbocharger/Supercharger simulation
- Fuel system with consumption tracking
- Temperature monitoring (Oil, Coolant, Intake Air)
- Performance metrics (0-100 km/h, quarter-mile tracking)
- Real-time audio synthesis with engine sounds
- Professional dark-mode UI with digital gauges
- Multi-page interface (Simulator, Builder, Dyno, Info)
- Keyboard controls for all major functions
- Full physics-based calculations

### Features
- RPM gauges with progress bars
- Speed display with real-time updates
- Power output in HP
- Gear indicator (R, N, 1-6)
- Fuel level and consumption display
- Oil and coolant temperature gauges
- Rev limiter adjustment
- Boost pressure control
- Volume control for audio
- Performance tracking (distance, runtime)

---

## Version History Summary

| Version | Date | Status |
|---------|------|--------|
| 1.3 | 2025-10-24 | Current - Major Physics Upgrade |
| 1.2 | 2025-10-24 | Bug Fixes & Improvements |
| 1.0 | 2025-10-23 | Initial Release |

---

## Bug Reports & Fixes

### v1.2 Bug Fixes
1. Audio callback was using `not self.is_running` instead of `self.is_running` - Fixed
2. Audio frequencies could become invalid (< 0) - Added bounds checking
3. Audio callback could crash on errors - Added exception handling
4. Volume parameters weren't clamped properly - Improved validation

### How to Report Issues
Please document any bugs found and submit them with:
- Steps to reproduce
- Expected behavior
- Actual behavior
- Error messages or logs

---

## Future Roadmap

## Completed in v1.3
- [x] Gradual RPM changes with time-based acceleration
- [x] Idle RPM stability (±50 RPM)
- [x] Proper physics formulas (torque, power, fuel)
- [x] Vehicle weight and inertia simulation
- [x] Gradual boost and temperature simulation
- [x] Gear shift RPM drop logic
- [x] Improved audio engine with smooth transitions
- [x] Dyno mode with drivetrain loss
- [x] Temperature-based performance degradation

## Planned for v1.4
- [ ] Custom transmission builder
- [ ] Advanced dyno graphs with matplotlib
- [ ] Replay system
- [ ] Performance logging and statistics

### Planned for v2.0
- [ ] Engine damage system
- [ ] Multiple engine sound profiles
- [ ] Anti-lag and traction control simulation
- [ ] Multiplayer network support

### Long-term Vision
- [ ] VR compatibility
- [ ] Advanced telemetry recording
- [ ] Machine learning-based performance prediction
- [ ] Custom paint/livery system
