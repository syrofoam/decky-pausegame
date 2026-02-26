import os
import signal
import subprocess
import decky_plugin

class Plugin:
    # These are "fake" Windows processes created by Proton/Wine. 
    # We must NEVER pause these, or the game environment breaks.
    PROTON_SYSTEM_EXES = [
        "explorer.exe", "services.exe", "winedevice.exe", 
        "plugplay.exe", "svchost.exe", "rpcss.exe", 
        "rundll32.exe", "wineboot.exe", "mscorsvw.exe",
        "tabtip.exe", "conhost.exe", "crash_handler.exe"
    ]

    async def get_game_pid(self):
        """
        Finds the PID of a running .exe that is NOT a system process.
        """
        try:
            # We list PID and the Command Name.
            # We don't care about CPU usage anymore.
            cmd = ["ps", "-eo", "pid,comm"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            lines = result.stdout.splitlines()
            
            candidates = []

            for line in lines[1:]:
                parts = line.strip().split(maxsplit=1)
                if len(parts) < 2: continue
                
                pid_str, name = parts
                name_lower = name.lower()

                # 1. MUST end in .exe
                if not name_lower.endswith(".exe"):
                    continue

                # 2. MUST NOT be a known Proton system file
                if name_lower in self.PROTON_SYSTEM_EXES:
                    continue
                
                # If it passed both, it's a user game executable.
                candidates.append((int(pid_str), name))

            # Logic: If we found candidates, usually the LAST one launched 
            # or the one with the highest PID is the actual game 
            # (since launchers usually spawn the game process later).
            # For safety, let's grab the one with the highest PID.
            if candidates:
                candidates.sort(key=lambda x: x[0], reverse=True) # Sort by PID descending
                target_pid, target_name = candidates[0]
                decky_plugin.logger.info(f"Targeting Game: {target_name} (PID: {target_pid})")
                return target_pid
                
            return None

        except Exception as e:
            decky_plugin.logger.error(f"Error finding exe: {e}")
            return None

    async def pause_game(self):
        pid = await self.get_game_pid()
        if pid:
            try:
                os.kill(pid, signal.SIGSTOP) # Signal 19
                return True
            except ProcessLookupError:
                return False
        return False

    async def resume_game(self):
        # To resume, we look for PAUSED (State: T) processes that match our .exe filter
        cmd = ["ps", "-eo", "pid,state,comm"] 
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        for line in result.stdout.splitlines():
             parts = line.strip().split()
             if len(parts) < 3: continue
             
             pid, state, name = parts[0], parts[1], parts[2]
             name_lower = name.lower()

             # Criteria: Ends in .exe, is Paused (T), is not Proton System
             if (state == 'T' and 
                 name_lower.endswith(".exe") and 
                 name_lower not in self.PROTON_SYSTEM_EXES):
                 
                 os.kill(int(pid), signal.SIGCONT) # Signal 18
                 return True
                 
        return False
