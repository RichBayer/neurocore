# /mnt/g/ai/projects/neurocore/tools/system/command_runner.py

from __future__ import annotations

import subprocess
from typing import Dict, List, Optional


class CommandRunner:
    """
    Lightweight subprocess execution helper for system tools.

    This is NOT an authority layer.

    It does NOT:
    - authorize execution
    - enforce policy
    - perform validation beyond basic safety checks

    It ONLY:
    - executes commands safely (shell=False)
    - enforces timeout
    - captures stdout / stderr / return code
    """

    DEFAULT_TIMEOUT = 10  # seconds

    @staticmethod
    def run(
        command: List[str],
        timeout: Optional[int] = None,
    ) -> Dict[str, object]:
        """
        Execute a system command safely.

        Args:
            command: list of command parts (e.g., ["ls", "-l"])
            timeout: optional override for timeout (seconds)

        Returns:
            dict with:
                - status: "success" or "error"
                - stdout: str
                - stderr: str
                - returncode: int | None
                - timed_out: bool
        """

        if not isinstance(command, list) or not command:
            raise ValueError("Command must be a non-empty list")

        if not all(isinstance(part, str) and part for part in command):
            raise ValueError("All command elements must be non-empty strings")

        effective_timeout = timeout or CommandRunner.DEFAULT_TIMEOUT

        try:
            result = subprocess.run(
                command,
                shell=False,
                capture_output=True,
                text=True,
                timeout=effective_timeout,
            )

            return {
                "status": "success" if result.returncode == 0 else "error",
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
                "timed_out": False,
            }

        except subprocess.TimeoutExpired as e:
            return {
                "status": "error",
                "stdout": (e.stdout or "").strip() if e.stdout else "",
                "stderr": (e.stderr or "").strip() if e.stderr else "",
                "returncode": None,
                "timed_out": True,
            }

        except Exception as e:
            return {
                "status": "error",
                "stdout": "",
                "stderr": str(e),
                "returncode": None,
                "timed_out": False,
            }