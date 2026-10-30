
import tkinter as tk
import random

from src.core.commands import Command


class BlueScreenCommand(Command):

    @classmethod
    def name(cls) -> str:
        return "bluescreen"

    @classmethod
    def description(cls) -> str:
        return "Show a fake fullscreen Windows blue screen"

    @classmethod
    def is_server_side(cls) -> bool:
        return False

    @classmethod
    def validate_args(cls, args: list[str]) -> bool:
        return True

    @classmethod
    def to_json(cls, args: list[str]) -> str:
        import json
        return json.dumps({
            "action": cls.name(),
            "args": args
        })

    @classmethod
    async def execute(cls, args: list[str], server=None) -> str:

        def show_bsod():
            root = tk.Tk()
            root.title("Fake Blue Screen")
            root.configure(bg="#0078D7")

            root.attributes("-fullscreen", True)
            root.attributes("-topmost", True)

            frame = tk.Frame(root, bg="#0078D7")
            frame.pack(
                expand=True,
                fill="both",
                padx=100,
                pady=60
            )

            tk.Label(
                frame,
                text=":(",
                font=("Segoe UI Light", 85),
                fg="white",
                bg="#0078D7"
            ).pack(anchor="w", pady=(0, 20))

            tk.Label(
                frame,
                text="Your PC ran into a problem and needs to restart.",
                font=("Segoe UI", 24),
                fg="white",
                bg="#0078D7",
                wraplength=1000,
                justify="left"
            ).pack(anchor="w", pady=10)

            tk.Label(
                frame,
                text="We're just collecting some error info, and then we'll restart for you.",
                font=("Segoe UI", 15),
                fg="white",
                bg="#0078D7",
                wraplength=1000,
                justify="left"
            ).pack(anchor="w", pady=5)

            progress = tk.Label(
                frame,
                text="0% complete",
                font=("Segoe UI", 15),
                fg="white",
                bg="#0078D7"
            )
            progress.pack(anchor="w", pady=15)

            stop_code = tk.Label(
                frame,
                text="Stop code: CRITICAL_PROCESS_DIED",
                font=("Segoe UI", 12),
                fg="white",
                bg="#0078D7"
            )
            stop_code.pack(anchor="w", pady=5)

            percent = [0]

            def update_progress():
                percent[0] += random.randint(1, 4)

                if percent[0] >= 100:
                    percent[0] = 100

                progress.config(
                    text=f"{percent[0]}% complete"
                )

                if percent[0] < 100:
                    root.after(
                        random.randint(200, 700),
                        update_progress
                    )
                else:
                    progress.config(
                        text="100% complete — Simulation finished"
                    )

            def close(event=None):
                root.destroy()

            root.bind("<Escape>", close)
            root.bind("<Key>", close)
            root.bind("<Button-1>", close)

            root.after(1000, update_progress)

            root.mainloop()

        try:
            # Run the GUI in a separate thread.
            import asyncio
            await asyncio.to_thread(show_bsod)

            return "Blue screen simulation closed."

        except Exception as e:
            return f"Failed to show blue screen: {e}"
