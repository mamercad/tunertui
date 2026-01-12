"""
CLI entry point for TunerTUI
"""

import sys
from textual.app import ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer

from tunertui.ui import TunerApp


class TunerApplication(Container):
    """Main application container"""

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield TunerApp()
        yield Footer()


def main() -> None:
    """Main entry point"""
    try:
        from textual.app import App

        class TunerTextualApp(App):
            CSS = """
            Screen {
                background: $surface;
                color: $text;
            }
            
            #tuner-display {
                width: 60;
                height: auto;
                border: solid $primary;
            }
            
            #instrument-selector {
                width: 1fr;
                height: auto;
                border: solid $accent;
                padding: 1;
            }
            
            #string-list {
                width: 1fr;
                height: auto;
                border: solid $accent;
                padding: 1;
            }
            
            Button {
                margin: 1 2;
            }
            """

            def compose(self) -> ComposeResult:
                yield TunerApp()

        app = TunerTextualApp()
        app.run()

    except KeyboardInterrupt:
        print("\nShutting down...", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
