# Build Instructions for Linux MMORPG Launcher

## Prerequisites

- Python 3.13+
- PyQt6
- PyInstaller

## Building the Application

1. **Create virtual environment** (if not already created):
   ```bash
   python -m venv .venv
   ```

2. **Install dependencies**:
   ```bash
   .venv/bin/pip install PyQt6 pyinstaller
   ```

3. **Build the executable**:
   ```bash
   .venv/bin/pyinstaller linuxmmorpg.spec
   ```

   The built executable will be in `dist/linuxmmorpg`

## Running the Application

### Option 1: Direct execution
```bash
./dist/linuxmmorpg
```

### Option 2: Using launch script
```bash
./launch.sh
```

### Option 3: Install desktop entry
```bash
cp linuxmmorpg.desktop ~/.local/share/applications/
```

Then launch from your application menu.

## Output

- **Executable**: `dist/linuxmmorpg` (81 MB)
- **Build artifacts**: `build/` directory
- **Spec file**: `linuxmmorpg.spec`

## Testing

The application should:
- Launch without errors
- Display the PyQt6 GUI interface
- Show the games library
- Allow filtering and searching games
- Support installing/launching games (requires appropriate dependencies)

## Dependencies for Running Games

The launcher requires these system dependencies to install and run games:
- `umu-launcher` - Universal game launcher
- `wine` - Windows compatibility layer
- `steam` - Steam runtime (for Proton)
- `flatpak` - Package manager for some games
- `java` - For some MMO clients

Check dependencies via: **Tools > Check Dependencies** in the app menu.

## Troubleshooting

### Build warnings about ldd permissions
These are harmless warnings and don't affect the build.

### App won't launch
- Check that you have Qt6 libraries installed on your system
- Run from terminal to see error messages: `./dist/linuxmmorpg`

### Missing dependencies
Install missing runtime dependencies:
```bash
sudo pacman -S wine steam flatpak jre-openjdk
yay -S umu-launcher  # AUR package
```
