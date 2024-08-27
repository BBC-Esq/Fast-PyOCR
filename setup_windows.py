import sys
import subprocess
import time
import os

start_time = time.time()

def upgrade_pip_setuptools_wheel(max_retries=5, delay=3):
    upgrade_commands = [
        [sys.executable, "-m", "pip", "install", "--upgrade", "pip", "--no-cache-dir"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "setuptools", "--no-cache-dir"],
        [sys.executable, "-m", "pip", "install", "--upgrade", "wheel", "--no-cache-dir"]
    ]

    for command in upgrade_commands:
        package = command[5]
        for attempt in range(max_retries):
            try:
                print(f"\nAttempt {attempt + 1} of {max_retries}: Upgrading {package}...")
                process = subprocess.run(command, check=True, capture_output=True, text=True, timeout=240)
                print(f"Successfully upgraded {package}")
                break
            except subprocess.CalledProcessError as e:
                print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to upgrade {package} after {max_retries} attempts.")
            except Exception as e:
                print(f"An unexpected error occurred while upgrading {package}: {str(e)}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {delay} seconds...")
                    time.sleep(delay)
                else:
                    print(f"Failed to upgrade {package} after {max_retries} attempts due to unexpected errors.")

def pip_install_with_retry(library, max_retries=5, delay=3):
    pip_args = ["uv", "pip", "install", library, "--no-deps"]

    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1} of {max_retries}: Installing {library}")
            print(f"Running command: {' '.join(pip_args)}")
            result = subprocess.run(pip_args, check=True, capture_output=True, text=True, timeout=240)
            print(f"Successfully installed {library}")
            return attempt + 1
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to install {library} after {max_retries} attempts.")
                return 0

def install_libraries(libraries):
    failed_installations = []
    multiple_attempts = []

    for library in libraries:
        attempts = pip_install_with_retry(library)
        if attempts == 0:
            failed_installations.append(library)
        elif attempts > 1:
            multiple_attempts.append((library, attempts))
        time.sleep(0.1)

    return failed_installations, multiple_attempts

def pip_install_with_deps(library, max_retries=5, delay=3):
    pip_args = ["uv", "pip", "install", library]

    for attempt in range(max_retries):
        try:
            print(f"\nAttempt {attempt + 1} of {max_retries}: Installing {library} with dependencies")
            print(f"Running command: {' '.join(pip_args)}")
            result = subprocess.run(pip_args, check=True, capture_output=True, text=True, timeout=300)
            print(f"Successfully installed {library} with dependencies")
            return attempt + 1
        except subprocess.CalledProcessError as e:
            print(f"Attempt {attempt + 1} failed. Error: {e.stderr.strip()}")
            if attempt < max_retries - 1:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                print(f"Failed to install {library} after {max_retries} attempts.")
                return 0

def install_libraries_with_deps(libraries):
    failed_installations = []
    multiple_attempts = []

    for library in libraries:
        attempts = pip_install_with_deps(library)
        if attempts == 0:
            failed_installations.append(library)
        elif attempts > 1:
            multiple_attempts.append((library, attempts))
        time.sleep(0.1)

    return failed_installations, multiple_attempts

other_libraries = [
    "https://github.com/simonflueckiger/tesserocr-windows_build/releases/download/tesserocr-v2.7.0-tesseract-5.3.4/tesserocr-2.7.0-cp311-cp311-win_amd64.whl",
    "tessdata==1.0.0",
    "tessdata.eng==1.0.0",
    "pillow==10.4.0"
]

full_install_libraries = [
    "pymupdf==1.24.9"
]

# 1. upgrade pip, setuptools, wheel
print("\033[92mUpgrading pip, setuptools, and wheel:\033[0m")
upgrade_pip_setuptools_wheel()

# 2. install uv
print("\033[92mInstalling uv:\033[0m")
subprocess.run(["pip", "install", "uv"], check=True)

# 3. install other_libraries
print("\033[92m\nInstalling other libraries:\033[0m")
other_failed, other_multiple = install_libraries(other_libraries)

# 4. install full_install_libraries
print("\033[92m\nInstalling libraries with dependencies:\033[0m")
full_install_failed, full_install_multiple = install_libraries_with_deps(full_install_libraries)

print("\n----- Installation Summary -----")

all_failed = other_failed + full_install_failed
all_multiple = other_multiple + full_install_multiple

if all_failed:
    print(f"\033[91m\nThe following libraries failed to install:\033[0m")
    for lib in all_failed:
        print(f"\033[91m- {lib}\033[0m")

if all_multiple:
    print(f"\033[93m\nThe following libraries required multiple attempts to install:\033[0m")
    for lib, attempts in all_multiple:
        print(f"\033[93m- {lib} (took {attempts} attempts)\033[0m")

if not all_failed and not all_multiple:
    print(f"\033[93m\nAll libraries installed successfully on the first attempt.\033[0m")
elif not all_failed:
    print(f"\033[93m\nAll libraries were eventually installed successfully.\033[0m")

if all_failed:
    sys.exit(1)

end_time = time.time()
total_time = end_time - start_time
hours, rem = divmod(total_time, 3600)
minutes, seconds = divmod(rem, 60)

print(f"\033[92m\nTotal installation time: {int(hours):02d}:{int(minutes):02d}:{seconds:05.2f}\033[0m")