# Source this directory's env before lake/lean.
# The agent image may export a macOS ELAN_HOME that is not writable here.
export ELAN_HOME="${ELAN_HOME_OVERRIDE:-$HOME/.elan}"
export PATH="$ELAN_HOME/bin:$PATH"
