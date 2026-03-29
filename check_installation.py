#!/usr/bin/env python3
"""
Verify that all dependencies for AI Virtual Mouse are installed correctly
"""

import sys
import importlib

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = [
        'cv2',
        'mediapipe',
        'pyautogui',
        'numpy',
        'PIL'
    ]

    missing_packages = []

    for package in required_packages:
        try:
            if package == 'cv2':
                importlib.import_module('cv2')
                print("✅ OpenCV (cv2) is installed")
            elif package == 'PIL':
                importlib.import_module('PIL')
                print("✅ Pillow (PIL) is installed")
            else:
                importlib.import_module(package)
                print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is NOT installed")

    return len(missing_packages) == 0

def check_camera():
    """Test camera access"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)

        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                height, width = frame.shape[:2]
                print(f"✅ Camera access successful ({width}x{height})")
                cap.release()
                return True
            else:
                print("❌ Could not read frame from camera")
                cap.release()
                return False
        else:
            print("❌ Could not open camera")
            return False
    except Exception as e:
        print(f"❌ Camera check failed: {e}")
        return False

def check_python_version():
    """Check Python version compatibility"""
    python_version = sys.version_info
    if python_version >= (3, 7):
        print(f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {python_version.major}.{python_version.minor} is not compatible (need 3.7+)")
        return False

def check_screen_size():
    """Check if we can get screen dimensions"""
    try:
        import pyautogui
        width, height = pyautogui.size()
        print(f"✅ Screen size detected: {width}x{height}")
        return True
    except Exception as e:
        print(f"❌ Could not get screen size: {e}")
        return False

def main():
    """Main verification function"""
    print("🔍 AI Virtual Mouse - Installation Verification")
    print("=" * 50)

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Camera Access", check_camera),
        ("Screen Size", check_screen_size)
    ]

    results = []

    for check_name, check_func in checks:
        print(f"\n{check_name} Check:")
        print("-" * 30)
        result = check_func()
        results.append(result)

    # Summary
    print("\n📋 Summary:")
    print("=" * 30)
    if all(results):
        print("✅ All checks passed! Ready to run AI Virtual Mouse.")
        print("\nRun the application with:")
        print("  python main.py")
    else:
        failed_checks = [name for (name, _), good in zip(checks, results) if good is False]
        print(f"❌ Some checks failed: {', '.join(failed_checks)}")
        
        if sys.platform == "darwin":
            print("\n💡 macOS Tips:")
            print("- Ensure you are using the virtual environment: source .venv/bin/activate")
            print("- If Screen Size or Mouse Control fails, go to:")
            print("  System Settings > Privacy & Security > Accessibility and enable your Terminal/IDE.")
            
        print("\nFix the issues above before running the application.")

if __name__ == "__main__":
    main()