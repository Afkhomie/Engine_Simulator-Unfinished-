#!/usr/bin/env python3
"""
Engine Simulator Launcher
Handles compilation of C++ code and launches the application
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def check_python_dependencies():
    """Check if required Python packages are installed"""
    print("[*] Checking Python dependencies...")
    
    required = {
        'numpy': 'numpy',
        'tkinter': 'tk'  # Built-in with Python
    }
    
    missing = []
    
    try:
        import numpy
        print("  ✓ NumPy found")
    except ImportError:
        missing.append('numpy')
        print("  ✗ NumPy not found")
    
    try:
        import tkinter
        print("  ✓ Tkinter found")
    except ImportError:
        missing.append('tkinter')
        print("  ✗ Tkinter not found (install python-tk package)")
    
    try:
        import pyaudio
        print("  ✓ PyAudio found (audio will work)")
    except ImportError:
        print("  ⚠ PyAudio not found (audio disabled, install with: pip install pyaudio)")
    
    if missing:
        print("\n[!] Missing dependencies. Install with:")
        print(f"    pip install {' '.join(missing)}")
        return False
    
    return True

def check_cpp_compiler():
    """Check if C++ compiler is available"""
    print("\n[*] Checking C++ compiler...")
    
    if platform.system() == 'Windows':
        compilers = {
            'MSVC': 'cl.exe',
            'MinGW': 'g++.exe',
            'Clang': 'clang++.exe'
        }
    else:
        compilers = {
            'GCC': 'g++',
            'Clang': 'clang++'
        }
    
    for name, cmd in compilers.items():
        try:
            result = subprocess.run([cmd, '--version'], 
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                print(f"  ✓ {name} found: {cmd}")
                return name, cmd
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
    
    print("  ⚠ No C++ compiler found (physics will use Python fallback)")
    return None, None

def compile_cpp_engine(compiler_name, compiler_cmd):
    """Compile the C++ physics engine"""
    print(f"\n[*] Compiling C++ physics engine with {compiler_name}...")
    
    project_dir = Path(__file__).parent
    cpp_files = [
        'engine_physics.cpp',
        'engine_physics_wrapper.cpp'
    ]
    
    # Check if files exist
    for cpp_file in cpp_files:
        if not (project_dir / cpp_file).exists():
            print(f"  ✗ {cpp_file} not found")
            return False
    
    # Build command based on compiler
    if compiler_name == 'MSVC':
        cmd = [compiler_cmd, '/LD', '/O2'] + cpp_files + ['/Fe:engine_physics.dll']
    elif compiler_name == 'MinGW':
        cmd = [compiler_cmd, '-shared', '-fPIC', '-O3', '-o', 'engine_physics.dll'] + cpp_files
    elif compiler_name == 'Clang':
        cmd = [compiler_cmd, '-shared', '-O3', '-o', 'engine_physics.dll'] + cpp_files
    else:
        cmd = [compiler_cmd, '-shared', '-O3', '-o', 'engine_physics.dll'] + cpp_files
    
    try:
        # Change to project directory
        old_cwd = os.getcwd()
        os.chdir(project_dir)
        
        print(f"  Running: {' '.join(cmd)}")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        os.chdir(old_cwd)
        
        if result.returncode == 0:
            dll_path = project_dir / 'engine_physics.dll'
            if dll_path.exists():
                print(f"  ✓ Compilation successful: {dll_path}")
                return True
            else:
                print("  ⚠ Compilation completed but DLL not found")
                return False
        else:
            print(f"  ✗ Compilation failed:")
            print(f"    STDERR: {result.stderr[:500]}")
            return False
    
    except subprocess.TimeoutExpired:
        os.chdir(old_cwd)
        print("  ✗ Compilation timed out")
        return False
    except Exception as e:
        os.chdir(old_cwd)
        print(f"  ✗ Compilation error: {e}")
        return False

def check_dll_exists():
    """Check if compiled DLL already exists"""
    project_dir = Path(__file__).parent
    dll_path = project_dir / 'engine_physics.dll'
    
    if dll_path.exists():
        print(f"\n[*] Physics engine DLL found: {dll_path}")
        return True
    
    return False

def launch_application():
    """Launch the main application"""
    print("\n[*] Launching Engine Simulator...")
    
    project_dir = Path(__file__).parent
    main_app = project_dir / 'main_app.py'
    
    if not main_app.exists():
        print(f"[!] Error: main_app.py not found at {main_app}")
        return False
    
    try:
        subprocess.run([sys.executable, str(main_app)], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Application failed: {e}")
        return False
    except Exception as e:
        print(f"[!] Error launching application: {e}")
        return False

def main():
    """Main launcher function"""
    print("=" * 60)
    print("  ENGINE SIMULATOR v1.0 - Launcher")
    print("=" * 60)
    
    # Check Python dependencies
    if not check_python_dependencies():
        print("\n[!] Critical dependencies missing. Cannot continue.")
        sys.exit(1)
    
    # Check for C++ compiler and DLL
    compiler_name, compiler_cmd = check_cpp_compiler()
    dll_exists = check_dll_exists()
    
    # Compile if needed
    if not dll_exists and compiler_name:
        user_input = input("\n[?] Would you like to compile the C++ physics engine? (y/n): ").lower()
        if user_input == 'y':
            if not compile_cpp_engine(compiler_name, compiler_cmd):
                print("\n[!] Compilation failed. App will use Python fallback (slower)")
        else:
            print("[*] Skipping compilation. App will use Python fallback")
    elif not dll_exists and not compiler_name:
        print("\n[!] No C++ compiler found. App will use Python fallback (slower)")
        print("    Install MinGW or Visual C++ Build Tools for better performance")
    
    # Launch application
    print("\n" + "=" * 60)
    if launch_application():
        print("\n[✓] Application closed normally")
    else:
        print("\n[!] Application closed with errors")
        sys.exit(1)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[*] Launcher interrupted by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Unexpected error: {e}")
        sys.exit(1)
