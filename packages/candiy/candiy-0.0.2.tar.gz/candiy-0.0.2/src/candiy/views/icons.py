from enum import Enum
from pathlib import Path

import customtkinter
from PIL import Image


class Icons(Enum):
    HEARTBEAT_ON = "Heartbeat_red_42px.png"
    HEARTBEAT_OFF = "Heartbeat_dark_blue_42px.png"
    SPY_ON = "spy_orange_42px.png"
    SPY_OFF = "spy_dark_blue_42px.png"
    TESTER_MODE_ON = "Tools_light_blue_42px.png"
    TESTER_MODE_OFF = "Tools_dark_blue_42px.png"
    POWER_ON = "Power_green_42px.png"
    POWER_OFF = "Power_dark_blue_42px.png"
    LOLLIPOP_ICON = "Lollipop_icon.ico"
    TOGGLE_ON = "Toggle_on_42px.png"
    TOGGLE_OFF = "Toggle_off_42px.png"

    def __init__(self, file_name: str) -> None:
        self.resources_dir = Path(__file__).parent.joinpath("resources")
        self.file = self.resources_dir.joinpath(file_name).as_posix()

    @property
    def image(self) -> customtkinter.CTkImage:
        return customtkinter.CTkImage(
            dark_image=Image.open(self.file),
            size=(30, 30),
        )
