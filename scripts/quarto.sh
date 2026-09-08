#!/usr/bin/env bash
set -euo pipefail
site_root="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$site_root"
mkdir -p .local-state/tmp .local-state/cache .local-state/config .local-state/data
export TMPDIR="$site_root/.local-state/tmp"
export XDG_CACHE_HOME="$site_root/.local-state/cache"
export XDG_CONFIG_HOME="$site_root/.local-state/config"
export XDG_DATA_HOME="$site_root/.local-state/data"
export MPLCONFIGDIR="$site_root/.local-state/config/matplotlib"
export JUPYTER_CONFIG_DIR="$site_root/.local-state/config/jupyter"
export IPYTHONDIR="$site_root/.local-state/config/ipython"
export JUPYTER_RUNTIME_DIR="$site_root/.local-state/tmp/jupyter"
export JUPYTER_DATA_DIR="$site_root/.local-state/data/jupyter"
if [[ -z "${QUARTO_PYTHON:-}" && -x "$site_root/../.tools/website-authoring-env/bin/python" ]]; then
  export QUARTO_PYTHON="$site_root/../.tools/website-authoring-env/bin/python"
fi
if [[ -n "${QUARTO_PYTHON:-}" ]]; then
  export PATH="$(dirname -- "$QUARTO_PYTHON"):$PATH"
fi
if [[ -n "${QUARTO_BIN:-}" ]]; then
  quarto_executable="$QUARTO_BIN"
elif command -v quarto >/dev/null 2>&1; then
  quarto_executable="$(command -v quarto)"
elif [[ -x "$site_root/../.tools/quarto-1.10.18/bin/quarto" ]]; then
  quarto_executable="$site_root/../.tools/quarto-1.10.18/bin/quarto"
else
  echo 'Install Quarto 1.10.18, or set QUARTO_BIN to its executable.' >&2
  exit 1
fi
exec "$quarto_executable" "$@"
