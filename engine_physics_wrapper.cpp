/*
 * C Wrapper for EnginePhysics C++ Class
 * Exports C-compatible functions for use with Python ctypes
 */

#include "engine_physics.h"

#ifdef _WIN32
    #define EXPORT __declspec(dllexport)
#else
    #define EXPORT __attribute__((visibility("default")))
#endif

extern "C" {
    
    // ============================================================================
    // Instance Management
    // ============================================================================
    
    EXPORT void* EnginePhysics_new() {
        return new EnginePhysics();
    }
    
    EXPORT void EnginePhysics_delete(void* engine) {
        if (engine) {
            delete static_cast<EnginePhysics*>(engine);
        }
    }
    
    // ============================================================================
    // Engine Control Functions
    // ============================================================================
    
    EXPORT void EnginePhysics_startEngine(void* engine) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->startEngine();
        }
    }
    
    EXPORT void EnginePhysics_stopEngine(void* engine) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->stopEngine();
        }
    }
    
    EXPORT void EnginePhysics_setThrottle(void* engine, double throttle) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->setThrottle(throttle);
        }
    }
    
    EXPORT void EnginePhysics_setBrake(void* engine, double brake) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->setBrake(brake);
        }
    }
    
    EXPORT void EnginePhysics_shiftUp(void* engine) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->shiftUp();
        }
    }
    
    EXPORT void EnginePhysics_shiftDown(void* engine) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->shiftDown();
        }
    }
    
    EXPORT void EnginePhysics_toggleClutch(void* engine) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->toggleClutch();
        }
    }
    
    EXPORT void EnginePhysics_setGear(void* engine, int gear) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->setGear(gear);
        }
    }
    
    // ============================================================================
    // Configuration Functions
    // ============================================================================
    
    EXPORT void EnginePhysics_setRevLimiter(void* engine, int rpm) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->setRevLimiter(rpm);
        }
    }
    
    EXPORT void EnginePhysics_setBoostPressure(void* engine, double psi) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->setBoostPressure(psi);
        }
    }
    
    // ============================================================================
    // Simulation Update
    // ============================================================================
    
    EXPORT void EnginePhysics_update(void* engine, double delta_time) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->update(delta_time);
        }
    }
    
    // ============================================================================
    // State Getters
    // ============================================================================
    
    EXPORT double EnginePhysics_getRPM(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getRPM();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getSpeed(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getSpeed();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getTorque(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getTorque();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getPower(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getPower();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getBoost(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getBoost();
        }
        return 0.0;
    }
    
    EXPORT int EnginePhysics_getCurrentGear(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getCurrentGear();
        }
        return 0;
    }
    
    EXPORT bool EnginePhysics_isEngineRunning(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->isEngineRunning();
        }
        return false;
    }
    
    EXPORT double EnginePhysics_getThrottlePosition(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getThrottlePosition();
        }
        return 0.0;
    }
    
    // ============================================================================
    // Temperature Getters
    // ============================================================================
    
    EXPORT double EnginePhysics_getOilTemp(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getOilTemp();
        }
        return 20.0;
    }
    
    EXPORT double EnginePhysics_getCoolantTemp(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getCoolantTemp();
        }
        return 20.0;
    }
    
    EXPORT double EnginePhysics_getIntakeTemp(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getIntakeTemp();
        }
        return 20.0;
    }
    
    // ============================================================================
    // Fuel and Health Getters
    // ============================================================================
    
    EXPORT double EnginePhysics_getFuelLevel(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getFuelLevel();
        }
        return 100.0;
    }
    
    EXPORT double EnginePhysics_getFuelConsumption(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getFuelConsumption();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getEngineWear(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getEngineWear();
        }
        return 0.0;
    }
    
    // ============================================================================
    // Performance Getters
    // ============================================================================
    
    EXPORT double EnginePhysics_getBest0To100Time(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getBest0To100Time();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getTotalDistance(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getTotalDistance();
        }
        return 0.0;
    }
    
    EXPORT double EnginePhysics_getRuntime(void* engine) {
        if (engine) {
            return static_cast<EnginePhysics*>(engine)->getRuntime();
        }
        return 0.0;
    }
    
    // ============================================================================
    // Session Management
    // ============================================================================
    
    EXPORT void EnginePhysics_resetSession(void* engine) {
        if (engine) {
            static_cast<EnginePhysics*>(engine)->resetSession();
        }
    }
}