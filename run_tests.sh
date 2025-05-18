#/bin/bash

# Continue even if a command fails
set +e

declare -A results
errors=()

echo "============================"
echo " Running full test suite"
echo "============================"

echo
echo "--- Unit Tests ---"
pytest -v
rc=$?
results["Unit Tests"]=$rc
if [ $rc -ne 0 ]; then errors+=("Unit Tests"); fi

echo
echo "--- Formatting Check (black) ---"
black --check .
rc=$?
results["Formatting (black)"]=$rc
if [ $rc -ne 0 ]; then errors+=("Formatting (black)"); fi

echo
echo "--- Security Analysis (Bandit) ---"
bandit -r . --exclude ./venv -lll
rc=$?
results["Security (Bandit)"]=$rc
if [ $rc -ne 0 ]; then errors+=("Security (Bandit)"); fi

echo
echo "--- Dependency Vulnerabilities (pip-audit) ---"
pip-audit -r requirements.txt
rc=$?
results["Dependency Vulnerabilities (pip-audit)"]=$rc
if [ $rc -ne 0 ]; then errors+=("Dependency Vulnerabilities (pip-audit)"); fi

echo
echo "============================"
echo " Test Suite Summary"
echo "============================"
for name in "${!results[@]}"; do
  if [ ${results[$name]} -eq 0 ]; then
    printf "[PASS] %s\n" "$name"
  else
    printf "[FAIL] %s\n" "$name"
  fi
done

if [ ${#errors[@]} -ne 0 ]; then
  echo
  echo "The following steps failed:"
  for step in "${errors[@]}"; do
    echo " - $step"
  done
  exit 1
else
  echo
  echo "All steps passed successfully."
  exit 0
fi
