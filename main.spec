# main.spec
import os
import sys

# --- Script to find hidden data ---
# We need to find the data files for magic and qfluentwidgets
try:
    import magic
    import qfluentwidgets
except ImportError as e:
    print(f"Error: Missing libraries. Did you 'pip install python-magic-bin qfluentwidgets'?")
    print(e)
    sys.exit(1)

# --- NEW FIX: Use the correct folder name '_rc' ---
# Get the directory where the 'magic' package is installed
magic_data_dir = os.path.dirname(magic.__file__)

# Get the directory where 'qfluentwidgets' package is installed
qfluent_dir = os.path.dirname(qfluentwidgets.__file__)
# Manually append the '_rc' folder name (based on your output)
qfluent_res_dir = os.path.join(qfluent_dir, "_rc")
# --------------------------------------------------------

# --- DEBUGGING: Print paths and check if they exist ---
print(f"--- PyInstaller Spec ---")
print(f"Magic data path: {magic_data_dir}")
print(f"QFluentWidgets resource path: {qfluent_res_dir}")

if not os.path.exists(magic_data_dir):
    print(f"FATAL ERROR: Magic data path does not exist: {magic_data_dir}")
    sys.exit(1)

if not os.path.exists(qfluent_res_dir):
    print(f"FATAL ERROR: QFluentWidgets resource path does not exist: {qfluent_res_dir}")
    print("This is the '_rc' folder. If this fails, something is very wrong with the installation.")
    sys.exit(1)

print(f"All data paths found successfully.")
print(f"--------------------------")
# ------------------------------------


# This is the standard PyInstaller spec file
a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    # --- THIS IS THE KEY MODIFICATION ---
    # We add our found data paths here.
    # (source_path, destination_in_exe)
    datas=[
        (magic_data_dir, 'magic'),
        (qfluent_res_dir, 'qfluentwidgets/_rc') # <-- UPDATED to _rc
    ],
    # ------------------------------------
    hiddenimports=['magic.libmagic'], # Helps PyInstaller find this submodule
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='FileScannerApp',  # <-- You can change this to your app's name
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,         # This is the --windowed flag
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,             # <-- You can add an .ico file path here
)

# This section builds the --onefile executable
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='FileScannerApp', # <-- Make sure this name matches the one in EXE
)

