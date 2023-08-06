from tkinter import END, NO, W, ttk
from typing import Any, Callable, Dict, List, Union

import customtkinter

from candiy.presenter.event_manager import EventManager
from candiy.presenter.events import EventID
from candiy.views.icons import Icons
from candiy.views.view import View

customtkinter.set_appearance_mode("Dark")
customtkinter.set_default_color_theme("blue")


class TraceViewData:
    headings = ["ID", "DLC", "Data", "Channel"]

    def __init__(
        self, id: str, dlc: str, data: List[str], channel: str, timestamp: str
    ) -> None:
        self.id = id
        self.dlc = dlc
        self.data = data
        self.channel = channel
        self.timestamp = timestamp

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TraceViewData):
            return NotImplemented
        return (
            self.id,
            self.dlc,
            self.data,
            self.channel,
            self.timestamp,
        ) == (
            other.id,
            other.dlc,
            other.data,
            other.channel,
            other.timestamp,
        )


class ToggleButton(customtkinter.CTkButton):
    def __init__(
        self,
        master: Any,
        image_on: Icons = Icons.TOGGLE_ON,
        image_off: Icons = Icons.TOGGLE_OFF,
        text: str = "",
        command: Union[Callable[[], None], None] = None,
    ):
        self.state: bool = False
        self.image_on = image_on.image
        self.image_off = image_off.image
        self._user_command = command
        super().__init__(
            master,
            text=text,
            command=self.command,
            fg_color="transparent",
            border_spacing=0,
            hover_color=("gray70", "gray30"),
            compound="top",
            image=self.image_off,
        )

    def command(self) -> None:
        self.state = not self.state
        if self.state:
            self.configure(image=self.image_on)
        else:
            self.configure(image=self.image_off)
        if self._user_command:
            self._user_command()

    def add_user_command(self, command: Callable[[], None]) -> None:
        self._user_command = command


class MainView(View):
    def __init__(self, event_manager: EventManager):
        super().__init__()
        self.root = customtkinter.CTk()
        self.event_manager = event_manager
        self.messages: Dict[str, TraceViewData] = {}

        # configure window
        self.root.title("CANDIY")
        self.root.geometry(f"{1080}x{580}")

        # update app icon
        self.root.iconbitmap(Icons.LOLLIPOP_ICON.file)

        # create menu
        # TODO: Create menu. CTK does not yet have a custom Menu element.
        #  The standard TK element looks awfull.

        # ========================================================
        # create main toolbar
        main_toolbar = customtkinter.CTkFrame(self.root)
        self.populate_main_toolbar_frame(main_toolbar)

        # ========================================================
        # create tabview and populate with frames
        tabview = customtkinter.CTkTabview(self.root)
        self.populate_trace_frame(tabview.add("Trace"))
        self.populate_diagnostics_frame(tabview.add("Diagnostics"))

        # ========================================================
        # create statusbar
        status_frame = customtkinter.CTkFrame(self.root)
        self.populate_status_frame(status_frame)

        # ========================================================
        # configure grid
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=0)
        main_toolbar.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nsew")
        tabview.grid(row=1, column=0, padx=10, sticky="nsew")
        status_frame.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def populate_main_toolbar_frame(self, frame: customtkinter.CTkFrame) -> None:
        heartbeat_button = ToggleButton(
            frame,
            text="Heartbeat",
            command=self.create_button_event_trigger(EventID.HEARTBEAT),
            image_off=Icons.HEARTBEAT_OFF,
            image_on=Icons.HEARTBEAT_ON,
        )
        heartbeat_button.grid(row=0, column=0)

        spy_button = ToggleButton(
            frame,
            text="Spy",
            command=self.create_button_event_trigger(EventID.SPY),
            image_off=Icons.SPY_OFF,
            image_on=Icons.SPY_ON,
        )
        spy_button.grid(row=0, column=1)

        power_button = ToggleButton(
            frame,
            text="Power",
            command=self.create_button_event_trigger(EventID.POWER),
            image_off=Icons.POWER_OFF,
            image_on=Icons.POWER_ON,
        )
        power_button.grid(row=0, column=2)

    def populate_diagnostics_frame(self, frame: customtkinter.CTkFrame) -> None:
        frame.grid_rowconfigure(0, weight=0)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=0)
        frame.grid_columnconfigure(1, weight=1)

        # create diagnostics toolbar
        self.diagnostics_toolbar = customtkinter.CTkFrame(frame)
        self.diagnostics_toolbar.grid(row=0, column=0, sticky="new", columnspan=2)

        self.tester_mode_button = ToggleButton(
            self.diagnostics_toolbar,
            text="Tester mode",
            command=self.create_button_event_trigger(EventID.TESTER_MODE),
        )
        self.tester_mode_button.grid(row=0, column=0)

        self.xcp_mode_button = ToggleButton(
            self.diagnostics_toolbar,
            text="XCP mode",
            command=self.create_button_event_trigger(EventID.XCP_MODE),
        )
        self.xcp_mode_button.grid(row=0, column=1)

        # create diagnostics textbox
        self.diagnostics_textbox = customtkinter.CTkTextbox(
            frame, activate_scrollbars=True
        )
        self.diagnostics_textbox.grid(row=1, column=1, sticky="nsew")
        self.diagnostics_textbox.insert("0.0", "No network activity...")
        self.diagnostics_textbox.configure(state="disabled")
        self.xcp_textbox = customtkinter.CTkTextbox(frame, activate_scrollbars=True)
        self.xcp_send_ecu_info_button = customtkinter.CTkButton(
            frame,
            text="Get ECU Info",
            command=self.create_button_event_trigger(EventID.XCP_GET_ECU_INFO),
        )
        self.xcp_send_ecu_info_button.grid(
            row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="n"
        )

    def populate_trace_frame(self, frame: customtkinter.CTkFrame) -> None:
        frame.grid_rowconfigure(0, weight=10)
        frame.grid_rowconfigure(1, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        # create trace message tree
        # create a Treeview widget
        # vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

        columns = TraceViewData.headings

        style = ttk.Style()
        style.configure(
            "mystyle.Treeview", highlightthickness=0, bd=0, font=("Calibri", 12)
        )  # Modify the font of the body
        style.configure(
            "mystyle.Treeview.Heading", font=("Calibri", 14, "bold")
        )  # Modify the font of the headings

        # create a Treeview widget
        self.trace_treeview = ttk.Treeview(
            frame,
            columns=columns,
            show="tree headings",
            style="mystyle.Treeview",
        )
        self.trace_treeview.grid(row=0, column=0, sticky="nsew")

        # define column headings
        self.trace_treeview.heading("#0", text="Time")
        for column in columns:
            self.trace_treeview.heading(column, text=column, anchor=W)
        self.trace_treeview.column("#0", minwidth=0, width=150, stretch=NO)
        self.trace_treeview.column(columns[0], minwidth=0, width=150, stretch=NO)
        self.trace_treeview.column(columns[1], minwidth=0, width=50, stretch=NO)

        # create trace textbox
        self.trace_textbox = customtkinter.CTkTextbox(frame, activate_scrollbars=True)
        self.trace_textbox.grid(row=1, column=0, sticky="nsew")
        self.trace_textbox.insert("0.0", "No network activity...")
        self.trace_textbox.configure(state="disabled")

    def populate_status_frame(self, status_frame: customtkinter.CTkFrame) -> None:
        self.status_label = customtkinter.CTkLabel(
            status_frame, text="Status unknown..."
        )
        self.status_label.grid(row=0, column=0)

    def update_text(self, text: str) -> None:
        return self.status_label.configure(text=text)

    def mainloop(self) -> None:
        return self.root.mainloop()

    def create_button_event_trigger(self, event_id: EventID) -> Callable[[], None]:
        event_trigger = self.event_manager.create_event_trigger(event_id)

        def create_callback() -> None:
            self.update_text(f"Event {event_id.name} triggered.")
            event_trigger()

        return create_callback

    def update_trace_view(self, messages: Dict[str, TraceViewData]) -> None:
        self.messages.update(messages)
        existing_ids = self.trace_treeview.get_children("")
        for id, message in self.messages.items():
            if id in existing_ids:
                self.trace_treeview.item(
                    id,
                    text=message.timestamp,
                    values=(message.id, message.dlc, message.data, message.channel),
                )
                for index, data in enumerate(message.data):
                    self.trace_treeview.item(
                        f"{id}.{index}",
                        text=f"data {data}",
                        values=[],
                    )
            else:  # new message
                self.trace_treeview.insert(
                    "",
                    END,
                    text=message.timestamp,
                    iid=id,
                    values=(message.id, message.dlc, message.data),
                    open=False,
                )
                for index, data in enumerate(message.data):
                    self.trace_treeview.insert(
                        id,
                        END,
                        iid=f"{id}.{index}",
                        text=f"data {data}",
                        values=[],
                    )

    def update_trace_textbox(self, text: str) -> None:
        self.update_text_box(self.trace_textbox, text)

    def update_xcp_textbox(self, text: str) -> None:
        self.update_text_box(self.xcp_textbox, text)

    @staticmethod
    def update_text_box(text_box: customtkinter.CTkTextbox, text: str) -> None:
        text_box.configure(state="normal")
        text_box.delete(1.0, END)
        text_box.insert("0.0", text)
        text_box.configure(state="disabled")


if __name__ == "__main__":
    MainView(EventManager()).mainloop()
