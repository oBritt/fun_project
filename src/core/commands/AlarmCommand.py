import array
import asyncio
import ctypes
import json
import math
import os
import tempfile
import time
import wave
import winsound

from src.core.commands import Command

DEFAULT_SECONDS = 5
MAX_SECONDS = 60

VK_VOLUME_UP = 0xAF
KEYEVENTF_KEYUP = 0x0002


def _make_siren_wav(path: str, seconds: int) -> None:
    """Generates a full-amplitude two-tone siren as a WAV file."""
    rate = 44100
    samples = array.array("h")
    for i in range(rate * seconds):
        t = i / rate
        freq = 1400 if int(t * 4) % 2 == 0 else 700  # switch tone every 0.25s
        samples.append(32767 if math.sin(2 * math.pi * freq * t) >= 0 else -32767)
    with wave.open(path, "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(rate)
        w.writeframes(samples.tobytes())


def _volume_via_pycaw() -> None:
    import comtypes
    from comtypes import CLSCTX_ALL
    from ctypes import POINTER, cast
    from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

    comtypes.CoInitialize()
    try:
        speakers = AudioUtilities.GetSpeakers()
        if hasattr(speakers, "EndpointVolume"):  # newer pycaw
            endpoint = speakers.EndpointVolume
        else:  # older pycaw
            interface = speakers.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            endpoint = cast(interface, POINTER(IAudioEndpointVolume))
        endpoint.SetMute(0, None)
        endpoint.SetMasterVolumeLevelScalar(1.0, None)
    finally:
        comtypes.CoUninitialize()


def _volume_via_keys() -> None:
    """Fallback without dependencies: volume-up presses unmute and raise volume."""
    user32 = ctypes.windll.user32
    for _ in range(55):  # 50 presses = 100%, a few extra to be safe
        user32.keybd_event(VK_VOLUME_UP, 0, 0, 0)
        user32.keybd_event(VK_VOLUME_UP, 0, KEYEVENTF_KEYUP, 0)
        time.sleep(0.01)


def _set_max_volume() -> None:
    try:
        _volume_via_pycaw()
    except Exception:
        _volume_via_keys()


def _run_alarm(seconds: int) -> None:
    _set_max_volume()
    fd, path = tempfile.mkstemp(suffix=".wav")
    os.close(fd)
    try:
        _make_siren_wav(path, seconds)
        winsound.PlaySound(path, winsound.SND_FILENAME)  # blocks until finished
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


class AlarmCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "alarm"

    @classmethod
    def description(cls) -> str:
        return "Unmute, set volume to 100% and play a loud siren (default 5 seconds)"

    @classmethod
    def is_server_side(cls) -> bool:
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        if len(args) == 0:
            return True
        if len(args) == 1 and args[0].isdigit():
            return 1 <= int(args[0]) <= MAX_SECONDS
        return False

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:
        seconds = int(args[0]) if args else DEFAULT_SECONDS
        try:
            await asyncio.to_thread(_run_alarm, seconds)
            return f"Alarm played for {seconds} seconds."
        except Exception as e:
            return f"Failed to play alarm: {str(e)}"