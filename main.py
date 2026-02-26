import os
import signal
import subprocess
import decky_plugin

class Plugin:
    # 1. System processes to IGNORE (Never pause these)
    PROTON_SYSTEM_EXES = [
        "explorer.exe", "services.exe", "winedevice.exe", 
        "plugplay.exe", "svchost.exe", "rpcss.exe", 
        "rundll32.exe", "wineboot.exe", "mscorsvw.exe"
    ]

    # 2. Linux Native Emulators to INCLUDE (Add names here if needed)
    LINUX_EMULATORS = [
        "yuzu", "ryujinx", "dolphin-emu", "retroarch", "pcsx2-qt", "citra-qt"
    ]

    async def get_target_process(self):
        """
        Returns a tuple: (pid, state, name)
        State is usually 'R' (Running), 'S' (Sleeping), or 'T' (Stopped/Paused)
        """
        try:
            # Get PID, State, and Command Name for all processes
            cmd = ["ps", "-eo", "pid,state,comm"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            candidates = []

            for line in result.stdout.splitlines():
                parts = line.strip().split()
                if len(parts) < 3: continue
                
                pid, state, name = parts[0], parts[1], parts[2]
                name_lower = name.lower()

                # CHECK 1: Is it a Windows Game? (.exe)
                is_windows_game = (name_lower.endswith(".exe") and 
                                   name_lower not in self.PROTON_SYSTEM_EXES)

                # CHECK 2: Is it a Linux Emulator?
                is_linux_emu = any(emu in name_lower for emu in self.LINUX_EMULATORS)

                if is_windows_game or is_linux_emu:
                    candidates.append((int(pid), state, name))

            # If we found multiple candidates, pick the one with the highest PID
            # (Usually the most recently launched game)
            if candidates:
                candidates.sort(key=lambda x: x[0], reverse=True)
                return candidates[0] # Returns (pid, state, name)
                
            return None

        except Exception as e:
            decky_plugin.logger.error(f"Error finding process: {e}")
            return None

    async def toggle_game(self):
        target = await self.get_target_process()
        
        if target:
            pid, state, name = target
            
            # If state is 'T', the process is currently PAUSED. We must RESUME it.
            if state == 'T':
                os.kill(pid, signal.SIGCONT) # Signal 18 = Continue
                decky_plugin.logger.info(f"Resumed {name} (PID: {pid})")
                return True
            
            # Otherwise (R, S, D), the process is RUNNING. We must PAUSE it.
            else:
                os.kill(pid, signal.SIGSTOP) # Signal 19 = Stop
                decky_plugin.logger.info(f"Paused {name} (PID: {pid})")
                return True
                
        return False
