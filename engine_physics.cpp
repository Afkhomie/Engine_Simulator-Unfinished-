#include "engine_physics.h"
#include <chrono>
#include <random>

EnginePhysics::EnginePhysics() {
    // Initialize with default inline-4 turbo engine
    engine = getInline4Turbo();
    transmission = getDefault6Speed();
    forced_induction = {ForcedInductionConfig::TURBO, 15.0, 0.1};
    vehicle = {1400.0, 0.15, 0.32, 0.015};
    
    // Initialize engine state
    current_rpm = 0;
    target_rpm = engine.idle_rpm;
    throttle_position = 0;
    current_gear = 0;
    clutch_engaged = true;
    engine_running = false;
    shift_timer = 0.0;
    is_shifting = false;
    
    // Initialize performance metrics
    current_speed = 0;
    current_torque = 0;
    current_power = 0;
    current_boost = 0;
    
    // Initialize temperatures (ambient)
    oil_temp = 20;
    coolant_temp = 20;
    intake_temp = 20;
    
    // Initialize fuel and wear
    fuel_level = 100;
    fuel_consumption = 0;
    engine_wear = 0;
    
    // Initialize performance tracking
    acceleration_start_time = 0;
    quarter_mile_start_time = 0;
    timing_0_100 = false;
    timing_quarter_mile = false;
    best_0_100_time = 0;
    best_quarter_mile_time = 0;
    
    // Initialize session data
    total_distance = 0;
    runtime = 0;
}

EnginePhysics::~EnginePhysics() {}

void EnginePhysics::startEngine() {
    if (fuel_level > 0 && !engine_running) {
        engine_running = true;
        current_rpm = engine.idle_rpm;
        target_rpm = engine.idle_rpm;
    }
}

void EnginePhysics::stopEngine() {
    engine_running = false;
    current_rpm = 0;
    target_rpm = 0;
    throttle_position = 0;
}

void EnginePhysics::setThrottle(double throttle) {
    throttle_position = std::max(0.0, std::min(1.0, throttle));
    
    if (engine_running) {
        if (current_gear == 0) {
            // Neutral - allow full RPM range
            if (throttle_position < 0.05) {
                target_rpm = engine.idle_rpm;
            } else {
                // Full range from idle to redline with 5% safety margin
                target_rpm = engine.idle_rpm + throttle_position * (engine.redline_rpm * 0.95 - engine.idle_rpm);
            }
        } else {
            // In gear - RPM depends on speed, gear ratio, and throttle
            double load_factor = (current_gear > 0) ? 1.0 : 0.8;
            if (throttle_position < 0.05) {
                target_rpm = engine.idle_rpm;
            } else {
                target_rpm = engine.idle_rpm + throttle_position * (engine.redline_rpm - engine.idle_rpm) * load_factor;
            }
        }
    }
}

void EnginePhysics::setBrake(double brake) {
    brake = std::max(0.0, std::min(1.0, brake));
    
    if (brake > 0 && current_speed > 0) {
        double brake_force = brake * 50.0;
        current_speed = std::max(0.0, current_speed - brake_force * 0.016);
    }
}

void EnginePhysics::shiftUp() {
    if (!clutch_engaged || is_shifting || current_gear >= 6) return;
    
    is_shifting = true;
    shift_timer = 0.15; // 150ms shift time
    
    int old_gear = current_gear;
    current_gear++;
    if (current_gear == 0) current_gear = 1;
    
    // Calculate RPM drop during upshift
    if (old_gear > 0 && current_gear > 0) {
        double old_ratio = transmission.gear_ratios[old_gear - 1];
        double new_ratio = transmission.gear_ratios[current_gear - 1];
        double rpm_factor = new_ratio / old_ratio;
        
        // RPM drops proportionally to gear ratio change
        current_rpm *= rpm_factor;
        target_rpm = current_rpm; // Match target to current during shift
        
        // Add slight RPM drop for realism (clutch engagement)
        current_rpm *= 0.95;
    }
}

void EnginePhysics::shiftDown() {
    if (!clutch_engaged || is_shifting || current_gear <= -1) return;
    
    is_shifting = true;
    shift_timer = 0.15; // 150ms shift time
    
    int old_gear = current_gear;
    current_gear--;
    if (current_gear == 0 && current_speed > 5) {
        current_gear = 1;
    }
    
    // Calculate RPM increase for downshift
    if (old_gear > 0 && current_gear > 0) {
        double old_ratio = transmission.gear_ratios[old_gear - 1];
        double new_ratio = transmission.gear_ratios[current_gear - 1];
        double rpm_factor = new_ratio / old_ratio;
        
        // RPM increases proportionally to gear ratio change
        current_rpm *= rpm_factor;
        target_rpm = current_rpm; // Match target to current during shift
        
        // Prevent over-rev on downshift
        if (current_rpm > engine.redline_rpm) {
            current_rpm = engine.redline_rpm;
            target_rpm = engine.redline_rpm;
        }
    }
}

void EnginePhysics::toggleClutch() {
    clutch_engaged = !clutch_engaged;
}

void EnginePhysics::setGear(int gear) {
    if (!clutch_engaged || is_shifting) return;
    
    if (gear >= -1 && gear <= 6) {
        is_shifting = true;
        shift_timer = 0.2; // 200ms for manual gear selection
        
        int old_gear = current_gear;
        current_gear = gear;
        
        // Adjust RPM based on gear change
        if (old_gear > 0 && current_gear > 0) {
            double old_ratio = transmission.gear_ratios[old_gear - 1];
            double new_ratio = transmission.gear_ratios[current_gear - 1];
            double rpm_factor = new_ratio / old_ratio;
            
            // RPM adjusts to match speed in new gear
            current_rpm *= rpm_factor;
            target_rpm = current_rpm; // Match target to current during shift
            
            // Add shift lag (slight RPM drop for upshift, prevent over-rev for downshift)
            if (current_gear > old_gear) {
                current_rpm *= 0.95; // 5% RPM drop on upshift
            }
            
            // Prevent over-rev on downshift
            if (current_rpm > engine.redline_rpm) {
                current_rpm = engine.redline_rpm;
                target_rpm = engine.redline_rpm;
            }
        } else if (current_gear == 0) {
            // Shifting to neutral - RPM settles to idle
            target_rpm = engine.idle_rpm;
        }
    }
}

double EnginePhysics::calculateTorqueAtRPM(double rpm) {
    if (rpm <= 0) return 0;
    
    // Realistic torque curve with peak at specified RPM
    double rpm_ratio = rpm / engine.peak_torque_rpm;
    double torque_multiplier;
    
    if (rpm < engine.peak_torque_rpm) {
        // Rising torque before peak
        torque_multiplier = 0.3 + 0.7 * rpm_ratio;
    } else {
        // Falling torque after peak
        double fall_rate = (engine.redline_rpm - engine.peak_torque_rpm) / (double)engine.peak_torque_rpm;
        torque_multiplier = 1.0 - 0.6 * ((rpm_ratio - 1.0) / fall_rate);
    }
    
    torque_multiplier = std::max(0.1, std::min(1.0, torque_multiplier));
    
    double base_torque = engine.peak_torque * torque_multiplier * throttle_position;
    
    // Apply boost multiplier (60% increase at max boost)
    double boost_multiplier = 1.0 + (current_boost / 14.7) * 0.6;
    
    return base_torque * boost_multiplier;
}

double EnginePhysics::calculatePowerAtRPM(double rpm) {
    double torque = calculateTorqueAtRPM(rpm);
    // Power (kW) = Torque (Nm) × RPM / 9549
    // Power (HP) = Power (kW) × 1.341
    double power_kw = (torque * rpm) / 9549.0;
    return power_kw * 1.341;
}

double EnginePhysics::calculateFuelConsumption() {
    if (!engine_running) return 0;
    
    double rpm_factor = current_rpm / (double)engine.redline_rpm;
    double throttle_factor = 0.2 + throttle_position * throttle_position * 0.8;
    
    double load_factor = 1.0;
    if (current_gear != 0) {
        load_factor = 1.0 + (0.3 / (std::abs(current_gear) + 1.0));
    }
    
    double boost_factor = 1.0 + (current_boost / forced_induction.max_boost) * 0.6;
    
    double base_consumption = engine.fuel_base * engine.displacement * 0.5;
    
    return base_consumption * rpm_factor * throttle_factor * load_factor * boost_factor;
}

void EnginePhysics::updateTemperatures(double delta_time) {
    if (!engine_running) {
        // Cool down when engine is off
        double ambient_temp = 20.0;
        oil_temp += (ambient_temp - oil_temp) * 0.1 * delta_time;
        coolant_temp += (ambient_temp - coolant_temp) * 0.15 * delta_time;
        intake_temp += (ambient_temp - intake_temp) * 0.3 * delta_time;
        return;
    }
    
    double load_factor = (current_rpm / (double)engine.redline_rpm) * throttle_position;
    
    // Oil temperature
    double target_oil_temp = 20 + load_factor * 80 + (current_rpm / engine.redline_rpm) * 20;
    double oil_heat_rate = (target_oil_temp > oil_temp) ? 0.15 : 0.08;
    oil_temp += (target_oil_temp - oil_temp) * oil_heat_rate * delta_time;
    
    // Coolant temperature
    double target_coolant_temp = 20 + load_factor * 60 + (current_rpm / engine.redline_rpm) * 15;
    double coolant_heat_rate = (target_coolant_temp > coolant_temp) ? 0.12 : 0.1;
    coolant_temp += (target_coolant_temp - coolant_temp) * coolant_heat_rate * delta_time;
    
    // Intake temperature (affected by boost)
    double boost_heat = current_boost * 3.5;
    double target_intake_temp = 20 + load_factor * 25 + boost_heat;
    double intake_heat_rate = (target_intake_temp > intake_temp) ? 0.25 : 0.35;
    intake_temp += (target_intake_temp - intake_temp) * intake_heat_rate * delta_time;
    
    // Overheating penalty
    if (coolant_temp > 105.0) {
        double overheat_penalty = 1.0 - ((coolant_temp - 105.0) / 20.0) * 0.3;
        overheat_penalty = std::max(0.7, std::min(1.0, overheat_penalty));
        current_power *= overheat_penalty;
        current_torque *= overheat_penalty;
    }
}

void EnginePhysics::updateEngineWear(double delta_time) {
    if (!engine_running) return;
    
    double wear_rate = 0.001 * delta_time;
    
    if (current_rpm > engine.redline_rpm * 0.9) wear_rate *= 3.0;
    if (oil_temp > 110) wear_rate *= 2.0;
    if (coolant_temp > 100) wear_rate *= 2.5;
    if (current_boost > forced_induction.max_boost * 0.9) wear_rate *= 1.5;
    
    engine_wear = std::min(100.0, engine_wear + wear_rate);
}

void EnginePhysics::updateBoost(double delta_time) {
    if (forced_induction.type == ForcedInductionConfig::NONE) {
        current_boost = 0;
        return;
    }
    
    double target_boost = 0;
    if (engine_running && throttle_position > 0.1) {
        if (forced_induction.type == ForcedInductionConfig::SUPERCHARGER) {
            double rpm_factor = current_rpm / (double)engine.redline_rpm;
            target_boost = forced_induction.max_boost * rpm_factor * throttle_position;
        } else if (forced_induction.type == ForcedInductionConfig::TURBO) {
            double rpm_factor = std::max(0.0, (current_rpm - 2000.0) / (engine.redline_rpm - 2000.0));
            target_boost = forced_induction.max_boost * rpm_factor * throttle_position;
        }
    }
    
    double response_rate;
    if (forced_induction.type == ForcedInductionConfig::TURBO) {
        response_rate = (target_boost > current_boost) ? forced_induction.spool_rate : forced_induction.spool_rate * 2.0;
    } else {
        response_rate = 5.0;
    }
    
    current_boost += (target_boost - current_boost) * response_rate * delta_time;
    current_boost = std::max(0.0, std::min(forced_induction.max_boost, current_boost));
}

void EnginePhysics::update(double delta_time) {
    if (!engine_running && current_rpm > 0) {
        // Engine off - spin down
        double spindown_rate = 300.0 + (current_rpm * 0.2);
        current_rpm = std::max(0.0, current_rpm - spindown_rate * delta_time);
    } else if (engine_running) {
        // Engine running - update RPM with realistic acceleration
        double rpm_diff = target_rpm - current_rpm;
        double base_accel_rate = 1.0 / (engine.engine_inertia * 6.0);
        
        if (current_gear == 0) {
            // Neutral - fast response (8x faster than base)
            double accel_rate = base_accel_rate * 8.0;
            current_rpm += rpm_diff * accel_rate * delta_time;
        } else {
            // In gear - slower due to vehicle mass and drivetrain
            double mass_factor = vehicle.vehicle_mass / 1000.0;
            double gear_load = 1.0 + (std::abs(current_gear) * 0.15);
            double total_inertia = engine.engine_inertia * mass_factor * gear_load;
            double accel_rate = base_accel_rate * 1.0 / total_inertia;
            current_rpm += rpm_diff * accel_rate * delta_time;
            
            // Apply engine braking when throttle is released in gear
            if (throttle_position < 0.05 && current_speed > 1.0) {
                // Engine braking force proportional to RPM and gear
                double engine_braking = (current_rpm / engine.redline_rpm) * 15.0 * std::abs(current_gear);
                current_speed = std::max(0.0, current_speed - engine_braking * delta_time);
            }
        }
        
        // Idle stability with slight fluctuation
        if (throttle_position < 0.05 && std::abs(current_rpm - engine.idle_rpm) < 50) {
            static int fluctuation_counter = 0;
            fluctuation_counter++;
            if (fluctuation_counter % 30 == 0) {
                double random_offset = ((rand() % 20) - 10);
                current_rpm = engine.idle_rpm + random_offset;
            }
        }
        
        // Rev limiter with hard cut
        if (current_rpm > engine.redline_rpm) {
            current_rpm = engine.redline_rpm;
            target_rpm = engine.redline_rpm * 0.95;
        }
        
        runtime += delta_time;
    }
    
    // Handle shifting delay
    if (is_shifting) {
        shift_timer -= delta_time;
        if (shift_timer <= 0) {
            is_shifting = false;
            shift_timer = 0;
            
            // After shift completes, recalculate target RPM based on current throttle
            if (engine_running && current_gear != 0) {
                double load_factor = (current_gear > 0) ? 1.0 : 0.8;
                if (throttle_position < 0.05) {
                    target_rpm = engine.idle_rpm;
                } else {
                    target_rpm = engine.idle_rpm + throttle_position * (engine.redline_rpm - engine.idle_rpm) * load_factor;
                }
            }
        }
    }
    
    // Update derived values
    current_torque = calculateTorqueAtRPM(current_rpm);
    current_power = calculatePowerAtRPM(current_rpm);
    fuel_consumption = calculateFuelConsumption();
    
    // Update speed based on gear and RPM
    if (current_gear > 0 && clutch_engaged && engine_running) {
        double gear_ratio = transmission.gear_ratios[current_gear - 1];
        double wheel_circumference = M_PI * transmission.wheel_diameter;
        double wheel_rpm = current_rpm / (gear_ratio * transmission.final_drive);
        double target_speed = (wheel_rpm * wheel_circumference * 60.0) / 1000.0;
        
        // Smooth speed changes to prevent instant jumps
        double speed_diff = target_speed - current_speed;
        double speed_accel_rate = 0.5; // Smooth acceleration/deceleration
        current_speed += speed_diff * speed_accel_rate * delta_time * 60.0;
        
    } else if (current_gear < 0 && clutch_engaged && engine_running) {
        double gear_ratio = 3.5;
        double wheel_circumference = M_PI * transmission.wheel_diameter;
        double wheel_rpm = current_rpm / (gear_ratio * transmission.final_drive);
        current_speed = -(wheel_rpm * wheel_circumference * 60.0) / 1000.0;
    } else if (current_gear == 0 && current_speed > 0) {
        // In neutral, apply rolling resistance to slow down
        double rolling_decel = 5.0; // Gradual slowdown in neutral
        current_speed = std::max(0.0, current_speed - rolling_decel * delta_time);
    }
    
    // Update distance
    if (current_speed > 0) {
        total_distance += (current_speed * delta_time) / 3600.0;
    }
    
    // Update fuel level
    if (fuel_consumption > 0) {
        double fuel_used = (fuel_consumption * delta_time) / 3600.0;
        fuel_level = std::max(0.0, fuel_level - (fuel_used / 50.0) * 100.0);
    }
    
    // Update subsystems
    updateTemperatures(delta_time);
    updateEngineWear(delta_time);
    updateBoost(delta_time);
    
    // Performance tracking
    if (current_speed >= 100.0 && !timing_0_100 && current_speed > 5.0) {
        if (acceleration_start_time > 0) {
            double time_0_100 = runtime - acceleration_start_time;
            if (best_0_100_time == 0 || time_0_100 < best_0_100_time) {
                best_0_100_time = time_0_100;
            }
            timing_0_100 = true;
        }
    }
    
    if (current_speed > 5.0 && acceleration_start_time == 0) {
        acceleration_start_time = runtime;
        timing_0_100 = false;
    } else if (current_speed < 2.0) {
        acceleration_start_time = 0;
        timing_0_100 = false;
    }
    
    // Quarter mile timing
    if (total_distance >= 0.402 && !timing_quarter_mile && quarter_mile_start_time > 0) {
        double quarter_time = runtime - quarter_mile_start_time;
        if (best_quarter_mile_time == 0 || quarter_time < best_quarter_mile_time) {
            best_quarter_mile_time = quarter_time;
        }
        timing_quarter_mile = true;
    }
}

void EnginePhysics::setEngineConfig(const EngineConfig& config) {
    engine = config;
}

void EnginePhysics::setTransmissionConfig(const TransmissionConfig& config) {
    transmission = config;
}

void EnginePhysics::setForcedInduction(const ForcedInductionConfig& config) {
    forced_induction = config;
}

void EnginePhysics::setRevLimiter(int rpm) {
    engine.redline_rpm = std::max(3000, std::min(12000, rpm));
}

void EnginePhysics::setBoostPressure(double psi) {
    forced_induction.max_boost = std::max(0.0, std::min(25.0, psi));
}

// Engine presets
EngineConfig EnginePhysics::getInline4Turbo() {
    return {"Inline-4 2.0L Turbo", 2.0, 4, 800, 7200, 280, 3500, 250, 5500, 0.15, 8.0, "Premium"};
}

EngineConfig EnginePhysics::getV6NA() {
    return {"V6 3.5L NA", 3.5, 6, 700, 7000, 380, 4500, 300, 6200, 0.25, 12.0, "Premium"};
}

EngineConfig EnginePhysics::getV8NA() {
    return {"V8 5.0L NA", 5.0, 8, 650, 7500, 530, 4200, 450, 6800, 0.35, 18.0, "Premium"};
}

EngineConfig EnginePhysics::getDieselI4() {
    return {"Diesel I4 2.0L", 2.0, 4, 750, 5000, 420, 1800, 180, 4000, 0.18, 6.0, "Diesel"};
}

TransmissionConfig EnginePhysics::getDefault6Speed() {
    TransmissionConfig config;
    config.gear_ratios = {3.36, 2.07, 1.43, 1.00, 0.84, 0.56};
    config.final_drive = 3.73;
    config.wheel_diameter = 0.65;
    return config;
}

std::vector<std::pair<double, double>> EnginePhysics::getPowerCurve(int rpm_start, int rpm_end, int step) {
    std::vector<std::pair<double, double>> curve;
    double original_throttle = throttle_position;
    throttle_position = 1.0;
    
    for (int rpm = rpm_start; rpm <= rpm_end; rpm += step) {
        if (rpm > engine.redline_rpm) break;
        double power = calculatePowerAtRPM(rpm);
        curve.push_back({rpm, power});
    }
    
    throttle_position = original_throttle;
    return curve;
}

std::vector<std::pair<double, double>> EnginePhysics::getTorqueCurve(int rpm_start, int rpm_end, int step) {
    std::vector<std::pair<double, double>> curve;
    double original_throttle = throttle_position;
    throttle_position = 1.0;
    
    for (int rpm = rpm_start; rpm <= rpm_end; rpm += step) {
        if (rpm > engine.redline_rpm) break;
        double torque = calculateTorqueAtRPM(rpm);
        curve.push_back({rpm, torque});
    }
    
    throttle_position = original_throttle;
    return curve;
}

void EnginePhysics::resetSession() {
    total_distance = 0;
    runtime = 0;
    best_0_100_time = 0;
    best_quarter_mile_time = 0;
    acceleration_start_time = 0;
    quarter_mile_start_time = 0;
    timing_0_100 = false;
    timing_quarter_mile = false;
    engine_wear = 0;
    fuel_level = 100;
}