#ifndef ENGINE_PHYSICS_H
#define ENGINE_PHYSICS_H

#include <vector>
#include <string>
#include <cmath>
#include <algorithm>

// Engine configuration structure
struct EngineConfig {
    std::string name;
    double displacement;        // Liters
    int cylinders;
    int idle_rpm;
    int redline_rpm;
    double peak_torque;         // Nm
    int peak_torque_rpm;
    double peak_power;          // HP
    int peak_power_rpm;
    double engine_inertia;      // Rotational inertia factor
    double fuel_base;           // L/h base consumption
    std::string fuel_type;
};

// Vehicle configuration
struct VehicleConfig {
    double vehicle_mass;        // kg
    double drivetrain_loss;     // 0.15 = 15% loss
    double drag_coefficient;    // Cd for aerodynamics
    double rolling_resistance;  // Tire resistance coefficient
};

// Transmission configuration
struct TransmissionConfig {
    std::vector<double> gear_ratios;
    double final_drive;
    double wheel_diameter;      // meters
};

// Forced induction configuration
struct ForcedInductionConfig {
    enum Type { NONE, TURBO, SUPERCHARGER };
    Type type;
    double max_boost;           // PSI
    double spool_rate;          // Response rate for turbo
};

class EnginePhysics {
private:
    // Configuration
    EngineConfig engine;
    TransmissionConfig transmission;
    ForcedInductionConfig forced_induction;
    VehicleConfig vehicle;
    
    // Engine state
    double current_rpm;
    double target_rpm;
    double throttle_position;   // 0.0 to 1.0
    int current_gear;           // -1=Reverse, 0=Neutral, 1-6=Gears
    bool clutch_engaged;
    bool engine_running;
    double shift_timer;
    bool is_shifting;
    
    // Performance metrics
    double current_speed;       // km/h
    double current_torque;      // Nm
    double current_power;       // HP
    double current_boost;       // PSI
    
    // Temperature simulation
    double oil_temp;            // °C
    double coolant_temp;        // °C
    double intake_temp;         // °C
    
    // Fuel and wear
    double fuel_level;          // Percentage (0-100)
    double fuel_consumption;    // L/h
    double engine_wear;         // Percentage (0-100)
    
    // Performance tracking
    double acceleration_start_time;
    double quarter_mile_start_time;
    bool timing_0_100;
    bool timing_quarter_mile;
    double best_0_100_time;
    double best_quarter_mile_time;
    
    // Session tracking
    double total_distance;      // km
    double runtime;             // seconds
    
    // Internal physics calculations
    double calculateTorqueAtRPM(double rpm);
    double calculatePowerAtRPM(double rpm);
    double calculateFuelConsumption();
    void updateTemperatures(double delta_time);
    void updateEngineWear(double delta_time);
    void updateBoost(double delta_time);
    
public:
    EnginePhysics();
    ~EnginePhysics();
    
    // Engine control
    void startEngine();
    void stopEngine();
    void setThrottle(double throttle);
    void setBrake(double brake);
    void shiftUp();
    void shiftDown();
    void toggleClutch();
    void setGear(int gear);
    
    // Configuration setters
    void setEngineConfig(const EngineConfig& config);
    void setTransmissionConfig(const TransmissionConfig& config);
    void setForcedInduction(const ForcedInductionConfig& config);
    void setRevLimiter(int rpm);
    void setBoostPressure(double psi);
    
    // Main simulation update
    void update(double delta_time);
    
    // State getters
    double getRPM() const { return current_rpm; }
    double getSpeed() const { return current_speed; }
    double getTorque() const { return current_torque; }
    double getPower() const { return current_power; }
    double getBoost() const { return current_boost; }
    int getCurrentGear() const { return current_gear; }
    bool isClutchEngaged() const { return clutch_engaged; }
    bool isEngineRunning() const { return engine_running; }
    double getThrottlePosition() const { return throttle_position; }
    
    // Temperature getters
    double getOilTemp() const { return oil_temp; }
    double getCoolantTemp() const { return coolant_temp; }
    double getIntakeTemp() const { return intake_temp; }
    
    // Fuel and health getters
    double getFuelLevel() const { return fuel_level; }
    double getFuelConsumption() const { return fuel_consumption; }
    double getEngineWear() const { return engine_wear; }
    
    // Performance getters
    double getBest0To100Time() const { return best_0_100_time; }
    double getBestQuarterMileTime() const { return best_quarter_mile_time; }
    double getTotalDistance() const { return total_distance; }
    double getRuntime() const { return runtime; }
    
    // Engine presets
    static EngineConfig getInline4Turbo();
    static EngineConfig getV6NA();
    static EngineConfig getV8NA();
    static EngineConfig getDieselI4();
    static TransmissionConfig getDefault6Speed();
    
    // Dyno curves
    std::vector<std::pair<double, double>> getPowerCurve(int rpm_start = 1000, int rpm_end = 8000, int step = 100);
    std::vector<std::pair<double, double>> getTorqueCurve(int rpm_start = 1000, int rpm_end = 8000, int step = 100);
    
    // Session management
    void resetSession();
};

#endif // ENGINE_PHYSICS_H