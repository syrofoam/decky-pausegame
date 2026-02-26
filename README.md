# Decky Pause Games (Force Pause)

A [Decky Loader](https://github.com/SteamDeckHomebrew/decky-loader) plugin that forces **any** game on the Steam Deck to pause, even if the game itself doesn't allow it.

![Pause Badge](https://img.shields.io/badge/Status-Working-brightgreen) ![Platform](https://img.shields.io/badge/Platform-Steam_Deck-blue)

## 🛑 The Problem
Many games (Elden Ring, Dark Souls, Arcade emulators, cutscenes) do not have a pause function. If you need to step away, the game keeps running, or you risk getting disconnected/killed.

Existing "Pause" plugins often fail because they target the wrong process (e.g., the Steam launcher script instead of the actual game executable).

## ✅ The Solution
This plugin uses a robust **"Process Hunter"** method:
1.  Scans for the specific `.exe` or Linux binary running the game.
2.  Filters out system processes (Proton, Steam, Overlay).
3.  Sends a Linux Kernel signal (**`SIGSTOP`**) to freeze the process instantly.
4.  Sends **`SIGCONT`** to resume exactly where you left off.

It works on:
* **Steam Games** (Elden Ring, God of War, etc.)
* **Non-Steam Games** (Launchers like Heroic, Lutris)
* **Emulators** (Yuzu, Ryujinx, Dolphin, PCSX2, RetroArch)

---

## 📥 Installation

### Option 1: Manual Install (Recommended for Testing)
1.  Download the latest `decky-pausegame.zip` from the **Releases** or **Actions** tab.
2.  Unzip the folder.
3.  Copy the folder to your Steam Deck:
    ```bash
    /home/deck/homebrew/plugins/decky-pausegame
    ```
4.  Restart your Steam Deck or the Decky Loader service.

### Option 2: Build from Source
Requirements: `Node.js`, `pnpm`, and a Linux environment (or WSL).

```bash
# Clone the repo
git clone [https://github.com/YOUR_USERNAME/decky-pausegame.git](https://github.com/YOUR_USERNAME/decky-pausegame.git)
cd decky-pausegame

# Install dependencies
pnpm install

# Build the plugin
pnpm run build
