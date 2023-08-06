from candiy.presenter.event_manager import EventManager
from candiy.presenter.events import EventID
from candiy.presenter.presenter import Presenter
from candiy.views.main_view import MainView
from candiy.views.view import View


class Candiy(Presenter):
    def __init__(self, view: View, event_manager: EventManager) -> None:
        self.view = view
        self.event_manager = event_manager
        self.event_manager.subscribe(EventID.HEARTBEAT, self.heartbeat)
        self.counter = 0

    def heartbeat(self) -> None:
        self.counter += 1
        self.view.update_text(f"Heartbeat {self.counter}")

    def run(self) -> None:
        self.view.mainloop()


def main() -> None:
    event_manager = EventManager()
    view = MainView(event_manager)
    Candiy(view, event_manager).run()


if __name__ == "__main__":
    main()
