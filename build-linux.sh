#!/usr/bin/env bash

set -euo pipefail

repository_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${repository_root}"

python_executable="${JOVIAL_PYTHON:-python3}"
"${python_executable}" -m PyInstaller --clean --noconfirm jovial.spec

case "$(uname -m)" in
    x86_64|amd64)
        architecture="x86_64"
        ;;
    aarch64|arm64)
        architecture="arm64"
        ;;
    *)
        architecture="$(uname -m)"
        ;;
esac

output_path="dist/jovial-linux-${architecture}"
mv -f dist/jovial "${output_path}"
chmod +x "${output_path}"

"${output_path}" --version
echo "Built ${output_path}"
