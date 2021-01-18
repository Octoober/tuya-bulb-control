"""
A simple Tkinter example demonstrating colour change and state switching.
Only two buttons:
    toggle_status_btn - Turning ON or OFF the light bulb.
    change_colour_btn - Opens a window with a palette.
"""

import colorsys
import json
from typing import NoReturn
from tkinter import Tk, Button, colorchooser
from tuya_bulb_control import Bulb

bulb = Bulb(
    client_id="121121212",
    secret_key="1212121212",
    device_id="121212212121212",
    region_key="eu",
)


def change_colour() -> NoReturn:
    # Get current HSV colour
    current_colour = json.loads(bulb.current_value("colour_data_v2"))

    # Conversion current HSV to RGB
    current_colour = colorsys.hsv_to_rgb(
        h=current_colour["h"] / 360,
        s=current_colour["s"] / 1000,
        v=current_colour["v"] / 1000,
    )
    # Convert the current RGB to format 0-255
    current_colour = tuple(map(lambda x: int(x * 255), current_colour))

    # Get new RGB colour
    new_colour = colorchooser.askcolor(color=current_colour)[0]
    # Convert RGB coordinates to int
    new_colour = tuple(map(lambda x: int(x), new_colour))

    # Set colour ✨
    bulb.set_colour_v2(new_colour)


def toggle_status(button) -> NoReturn:
    # Turn ON or OFF
    bulb.set_toggle()

    # Change button text
    button["text"] = "ON" if button["text"] == "OFF" else "OFF"


def init_ui() -> NoReturn:
    # Switch button
    toggle_status_btn = Button(
        text="ON"
        if not bulb.current_value("switch_led")
        else "OFF",  # Text depends on state
        width=20,
        command=lambda: toggle_status(toggle_status_btn),
    )
    # Colour selection button
    change_colour_btn = Button(text="Change colour", width=20, command=change_colour)

    # Positioning the buttons
    toggle_status_btn.pack(side="left", padx=5, pady=5, ipady=6)
    change_colour_btn.pack(side="right", padx=5, pady=5, ipady=6)


if __name__ == "__main__":
    tk = Tk()
    tk.title("Colour change example")
    init_ui()
    tk.mainloop()
