import subprocess
import sys


def run_command(description, command):
    print(f"\n🔍 {description}...")
    result = subprocess.run(["pytest", "test_main.py"])
    if result.returncode != 0:
        print(f"❌ {description} failed.")
        return False
    print(f"✅ {description} passed.")
    return True


def main():
    checks = [
        ("Running unit tests with pytest", "pytest test_main.py"),
        ("Checking code format with black", "black --check ."),
        ("Scanning for secrets with detect-secrets", "detect-secrets scan ."),
        ("Running bandit security scan", "bandit -r . --exclude ./venv -lll"),
        ("Running pip-audit", "pip-audit -r requirements.txt"),
    ]

    all_passed = True
    for description, command in checks:
        success = run_command(description, command)
        all_passed = all_passed and success

    if all_passed:
        print("\n✅✅ All checks passed!")
        sys.exit(0)
    else:
        print("\n❌ Some checks failed.")
        sys.exit(1)


if __name__ == "__main__":
    main()
