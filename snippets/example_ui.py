"""Example UI module demonstrating FreeSimpleGUI patterns and features.

This module provides reusable UI patterns including:
- Toggle switches with custom images
- Multi-page/column navigation
- Input validation and cleaning
- Async event loop integration
- Config file updates
- Subprocess execution from UI
"""

__author__ = "Bruce Iverson"

import asyncio
import base64
import logging
import subprocess
import sys
from io import BytesIO
from typing import Any

import FreeSimpleGUI as psg
import matplotlib

logger = logging.getLogger("common." + __name__)
logger.setLevel(logging.INFO)


# Formatting constants for consistent UI styling
TEXT_INPUT_KWDS = {"font": ("Arial Bold", 14), "expand_x": True, "justification": "right"}
INPUT_LABEL_KWDS = {"font": ("Arial Bold", 14), "justification": "left"}
BUTTON_KWDS = {"font": ("Arial Bold", 18)}

# Unicode characters for custom checkboxes (scales with font size unlike psg checkbox)
CHECKED = "☑"
UNCHECKED = "☐"

DEFAULT_STATUS_MSG = "Configure parameters and press 'Start' to begin."


class ToggleSwitchInfo:
    """Holds toggle switch state. Supports True, False, or None (disabled)."""

    def __init__(self, state: bool = True):
        self.state = state


# Base64 encoded toggle switch images
ON_IMAGE = b"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"
OFF_IMAGE = b"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"
OFF_IMAGE_DISABLED = b"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"
ON_IMAGE_DISABLED = b"iVBORw0KGgoAAAANSUhEUgAAAFoAAAAnCAYAAACPFF8dAAAAAXNSR0IArs4c6QAAAARnQU1BAACxjwv8YQUAAAAJcEhZcwAADsIAAA7CARUoSoAAAAVLSURBVGhD7Zu7TytHFMbHyxvsJeb9kjCiCihRpJAobaqblFGUJmXqKMofkyZpaKhS5HaJIgUpRZQmoqAhSgEUSBZgsAE/uJhX5ht80LmH8e56fdde7PuTPu0yj/XMt7Nnd2aXxPr6uuKMjIx84LruR47jJGtJbeeVplQqOaOjo+8ODAwk7u7uyrWsWIF2FYvFf3Rbt/HnQ+oDj0Ynk8kPl5eXf9Amf6L7pW5vb9X9/b3Jaye5XE719fWpubk51dPTY/bjijba+KbN3t7d3f324uLir1rWg9HpdPrFysrKy0KhMJTNZtX19XUtu/0sLi6qyclJlUqlcLWpRCJRy4knNzc3ShusKpXKq52dnS/z+fyvSE9sbGxMrq2t/Xd8fJw+PDw0hf1oRWdxNY2Pj6tMJqMmJiZUf3//Y3ocrjQJPOG+nJ2dYWSXt7a23tMRYt+Zn5//rlqteppMB5EHi5rZ2VmEtEeTAUzGJRo3yZOv7ydo94j293v8ndjW6JDxvh7RpoBEGtsKo9FofdNTq6urampqSvX29tZynhcIIUdHR//qUb3iDA4OZnDzs0Gm0khulQCMBs/VZIC2Dw8Pv6v71OvoO7lri3nUYb5tlToRp7Z9Deos37ZanYbVaA7vON/qCU1k6kQC94oMhxFk+FuCU9doPnptkPFRqBN5YjTvKO1LE3iZtwSjMwNiDGnYaD6aEa/1czieFdXQ0JB1wQfPw5C8Cii9Wwg9omHw2NiYmSLDaCz4YNoJ8ScHpGNBCGU4SIe6hVBGY+0BBmOiUy6XzQIKpptY9cOohrESjHg+y+u2ON+w0TAXpgGYfHl5aZYGq9WqMRsLLDDbNnXGyelWQsVoisUwl4OTQGvZPF5TOsxHyOlGQsdogNEroTQZGkqlktkiLnfq7M+LpnpsM4zS5EIVXvFUKhVzAmC2zH+OoA/1JGnYaByEwoN8PONhBXFbgngOw1GvnaNamhJWjdBwb2EmDAP0/EwvTV3XNQbiRNDJ4KBxuIGGQXayGXlhKx9WnFDDCjdBGEZhIJ1Om+dnmI2RXCwWayWfgrpXV1e1v4IhG10P2dEwCoKtnpQkVOgAGNX5fN7c5LCP+IvHOzxT85sk0uUoxt+oh7ygyI7Y5IetTlSSNBUoYSheg8E4mCYf9wDy5asyqlfvFZrE1pFGhd+0pYdRPbzKPTGaF6B9WVEeJGro95uRH7Y6jcqLuiOaKvIDyP2oFBRb3bDywlbeT5LAocPvQFEif5sUBFu9RuVHkDq+RvOK/ECIeW8y7nHZsJULIj9sdRpVEKxGU2W+lftRywtb+bDywlY+qCTGaLkuAagw39pGcBSjWoJJkFe+hJdtRn7Y6kBAznwdZPCVNg5V4gegfS4KI29KgB4VMWVHo7nZtjpcvG1hZTuulK0eID/RdpQDjn7+PcfMrh5UGciDRiVA69w03UfjMdVHw9EB5EUp/IaXbHXQdrwUQTsB2q5nwZc6/T6xubn5WyaT+Wxvb08VCgVTwAtbmIkCNHpmZkYtLCyY76P5iwQ6GXGE/MHMFzPlg4ODP/f39z91Tk9Pfzw/P1dLS0tqenra10h0shUC+JQYbTs5OXltfQRtjKvQdhhMyuVyP5k244t/PXJ+0aPmCywM4dLEohAuD1S0QUa0ApiMD9LxMTrCB1SvXe0GnuHegi1M1m3/I5vNvtBZd8Zo3fCkNvvnZDL5OV41Ic7EqTM48RjReOdo+3QhLmAAwmis4ejQ8bu+Ir/SaWYpk/9XViKVSn3tuu43ujMf67t8975JDYk29UrfAP/WA2NdawNJDzlK/Q9RjPZ1HEiBtwAAAABJRU5ErkJggg=="


def dict_item_to_layout_as_input(layout: list, key: str, default_value: str):
    """Add a dictionary item to the layout as a labeled input field.

    Args:
        layout: The layout list to append to
        key: The key name (will be formatted as display label)
        default_value: The default value for the input field
    """
    display_label = key[0].upper() + key[1:].replace("_", " ")
    layout.append(
        [
            psg.Text(display_label, **INPUT_LABEL_KWDS),
            psg.InputText(default_value, enable_events=True, key=f"-{key}-", **TEXT_INPUT_KWDS),
        ]
    )


def make_start_layout(config: dict) -> list:
    """Create the start/configuration page layout.

    Args:
        config: Configuration dictionary with form field values

    Returns:
        Layout list for the start page
    """
    start_layout = [
        [psg.Button("Start", key="-start-", font=("Arial Bold", 24))],
        [psg.Text(DEFAULT_STATUS_MSG, key="-msg_output-", font=("Arial Bold", 16), expand_x=True)],
        [psg.Text()],
        # Navigation buttons
        [
            psg.Button("Go to Settings", **BUTTON_KWDS),
            psg.Button("Open Secondary View", **BUTTON_KWDS),
        ],
        [psg.Button("Reset Connection", **BUTTON_KWDS)],
        # Toggle switch example
        [
            psg.Text("Enable Feature:", font=("Arial Bold", 14), expand_x=True),
            psg.Button(
                image_data=ON_IMAGE,
                k="-feature-toggle-",
                border_width=0,
                button_color=(psg.theme_background_color(), psg.theme_background_color()),
                disabled_button_color=(psg.theme_background_color(), psg.theme_background_color()),
                metadata=ToggleSwitchInfo(),
            ),
        ],
        # Dropdown example
        [
            psg.Text("Select Option:", font=("Arial Bold", 14), expand_x=True),
            psg.Combo(
                ["Option A", "Option B", "Option C"],
                font=("Arial Bold", 14),
                expand_x=True,
                enable_events=True,
                readonly=False,
                key="-option-select-",
            ),
        ],
        [psg.Text()],
    ]

    # Add input fields from config
    for key, value in config.items():
        dict_item_to_layout_as_input(start_layout, key, value)

    start_layout.append([psg.Text()])
    return start_layout


def make_ui(config: dict) -> psg.Window:
    """Create the main UI window with multiple page columns.

    Args:
        config: Configuration dictionary for form fields

    Returns:
        The configured psg.Window object
    """
    start_layout = make_start_layout(config)

    # Running/progress layout
    run_layout = [
        [psg.Text("Processing...", font=("Arial Bold", 24), key="-progress-text-")],
        [psg.ProgressBar(100, orientation="h", size=(40, 20), key="-progress-bar-")],
        [psg.Button("Cancel", button_color=("white", "red"), **BUTTON_KWDS)],
    ]

    # Completion layout
    complete_layout = [
        [psg.Text("Complete!", font=("Arial Bold", 24), expand_x=True, justification="center")],
        [psg.Button("Return to Home", key="-reset-", **BUTTON_KWDS, enable_events=True)],
        [psg.Text("Results:", key="-results-info-", font=("Arial Bold", 16), expand_x=True)],
    ]

    # Settings layout
    settings_layout = [
        [psg.Text("Settings", font=("Arial Bold", 24))],
        [
            psg.Text("Setting 1:", font=("Arial Bold", 14)),
            psg.InputText("default", key="-setting1-", font=("Arial Bold", 14)),
        ],
        [
            psg.Text("Setting 2:", font=("Arial Bold", 14)),
            psg.InputText("default", key="-setting2-", font=("Arial Bold", 14)),
        ],
        [psg.Button("Save Settings", **BUTTON_KWDS)],
        [psg.Button("Return to Home", **BUTTON_KWDS)],
    ]

    # Secondary view layout
    secondary_layout = [
        [psg.Button("Action A", **BUTTON_KWDS)],
        [psg.Button("Action B", **BUTTON_KWDS)],
        [psg.Button("Action C", **BUTTON_KWDS)],
        [psg.Text("")],
        [psg.Button("Return to Home", **BUTTON_KWDS)],
    ]

    # Long text output layout
    long_text_layout = [
        [psg.Button("Return to Home", **BUTTON_KWDS)],
        [psg.Text(key="-long_text_output-", font=("Arial Bold", 16), expand_x=True)],
    ]

    # Main layout with all columns
    layout = [
        [psg.VPush()],
        [
            psg.Column(start_layout, key="-start_col-", element_justification="center"),
            psg.Column(run_layout, visible=False, key="-running_col-", element_justification="center"),
            psg.Column(complete_layout, visible=False, key="-complete_col-", element_justification="center"),
            psg.Column(settings_layout, visible=False, key="-settings_col-", element_justification="center"),
            psg.Column(secondary_layout, visible=False, key="-secondary_col-", element_justification="center"),
            psg.Column(long_text_layout, visible=False, key="-long_text_col-", element_justification="center"),
        ],
        [psg.Text("")],
        [psg.Button("Exit Program", font=("Arial Bold", 20))],
        [psg.VPush()],
    ]

    window = psg.Window(
        "Example Application",
        layout,
        size=(1200, 800),
        resizable=True,
        enable_close_attempted_event=True,
        element_justification="c",
    )
    window.Finalize()
    return window


def encode_img_for_pysimplegui(fig: matplotlib.figure.Figure) -> str:
    """Encode a matplotlib figure as base64 for display in PySimpleGUI.

    Args:
        fig: matplotlib figure object

    Returns:
        Base64 encoded string of the figure
    """
    image = BytesIO()
    fig.savefig(image, format="png")
    return base64.encodebytes(image.getvalue())


def validate_and_clean_inputs(window: psg.Window, raw_values: dict[str, Any]) -> tuple[dict, bool]:
    """Validate and clean user inputs from the UI.

    Args:
        window: The window object for updating status messages
        raw_values: Raw values from the UI

    Returns:
        Tuple of (cleaned values dict, validity boolean)
    """
    logger.info(f"Validating inputs: {raw_values}")

    # Clean up key names (remove dashes)
    cleaned = {k.replace("-", ""): v for k, v in raw_values.items()}

    # Check for missing required values
    required_fields = ["name", "value"]  # Customize as needed
    for field in required_fields:
        if field in cleaned and (cleaned[field] is None or cleaned[field] == ""):
            window["-msg_output-"].update(f"Missing required field: {field}")
            logger.error(f"Missing required field: {field}")
            return None, False

    # Type conversion examples
    integer_fields = ["count", "quantity"]
    float_fields = ["price", "rate"]

    try:
        for k in integer_fields:
            if k in cleaned and cleaned[k]:
                cleaned[k] = int(cleaned[k])

        for k in float_fields:
            if k in cleaned and cleaned[k]:
                cleaned[k] = float(cleaned[k])
    except ValueError as e:
        msg = f"Error converting input to number: {e}"
        window["-msg_output-"].update(msg)
        logger.error(msg)
        return None, False

    logger.info(f"Validated inputs: {cleaned}")
    return cleaned, True


async def run_external_script(window: psg.Window, script_path: str):
    """Run an external Python script and display output in the UI.

    Args:
        window: The window object for updating UI
        script_path: Path to the script to run
    """
    logger.info(f"Running script: {script_path}")
    python_executable = sys.executable

    try:
        result = subprocess.run(
            [python_executable, script_path],
            capture_output=True,
            text=True,
            timeout=10
        )
        logger.info(f"Script result: {result}")

        if result.returncode != 0:
            logger.error(f"Script returned non-zero exit code: {result.returncode}")
            window["-msg_output-"].update(f"Script error: {result.returncode}")
            return

        window["-long_text_output-"].update(result.stdout)
        window["-long_text_col-"].update(visible=True)
        window["-start_col-"].update(visible=False)

    except subprocess.TimeoutExpired as e:
        logger.error(f"Script timeout: {e}")
        window["-msg_output-"].update(f"Script timeout: {e}")
    except Exception as e:
        logger.error(f"Script error: {e}")
        window["-msg_output-"].update(f"Script error: {e}")


# ============== Event Handlers ==============

async def handle_navigation(event: str, window: psg.Window):
    """Handle navigation between UI pages.

    Args:
        event: The event string from the window
        window: The window object
    """
    # Hide all columns helper
    def hide_all():
        for col in ["-start_col-", "-running_col-", "-complete_col-",
                    "-settings_col-", "-secondary_col-", "-long_text_col-"]:
            window[col].update(visible=False)

    if "-reset" in event or "Return to Home" in event:
        logger.info("Navigating to home")
        window["-msg_output-"].update(DEFAULT_STATUS_MSG)
        hide_all()
        window["-start_col-"].update(visible=True)

    elif event == "Go to Settings":
        logger.info("Navigating to settings")
        hide_all()
        window["-settings_col-"].update(visible=True)

    elif event == "Open Secondary View":
        logger.info("Navigating to secondary view")
        hide_all()
        window["-secondary_col-"].update(visible=True)


async def handle_task_events(
    event: str,
    values: dict,
    window: psg.Window,
    event_loop: asyncio.AbstractEventLoop,
    task_function: callable,
):
    """Handle task start/cancel events.

    Args:
        event: The event string
        values: Current UI values
        window: The window object
        event_loop: The asyncio event loop
        task_function: The async function to run as a task
    """
    global current_task

    if event == "-start-":
        cleaned, valid = validate_and_clean_inputs(window, values)
        if valid:
            window["-start_col-"].update(visible=False)
            window["-running_col-"].update(visible=True)
            logger.info("Starting task")
            current_task = asyncio.run_coroutine_threadsafe(
                task_function(window, cleaned), event_loop
            )

    elif event == "Cancel":
        logger.info("Cancelling task")
        window["-running_col-"].update(visible=False)
        window["-start_col-"].update(visible=True)
        if current_task:
            current_task.cancel()
            current_task = None


# Global task reference
current_task: asyncio.Task = None


async def ui_event_loop(
    window: psg.Window,
    loop: asyncio.AbstractEventLoop,
    task_function: callable = None,
):
    """Main UI event loop with async support.

    Args:
        window: The window object
        loop: The asyncio event loop
        task_function: Optional async function to run on start
    """
    global current_task

    try:
        while True:
            await asyncio.sleep(0.001)
            event, values = window.read(timeout=100)

            # Log non-timeout events
            if event != psg.TIMEOUT_KEY:
                logger.debug(f"Event: {event}, Values: {values}")
                if not event.startswith("-") or event in ["-start-", "-reset-"]:
                    logger.info(f"Event: {event}")

            # Exit conditions
            if event in (psg.WIN_CLOSED, "Exit Program", "-WINDOW CLOSE ATTEMPTED-"):
                if current_task is not None:
                    current_task.cancel()
                    await asyncio.sleep(0.01)
                break

            # Toggle switch handling
            if "toggle" in event:
                window[event].metadata.state = not window[event].metadata.state
                window[event].update(
                    image_data=ON_IMAGE if window[event].metadata.state else OFF_IMAGE
                )

            # Check for task completion
            if current_task is not None and current_task.done():
                logger.info("Task completed")
                window["-running_col-"].update(visible=False)
                window["-complete_col-"].update(visible=True)
                current_task = None

            # Handle events
            await handle_navigation(event, window)
            if task_function:
                await handle_task_events(event, values, window, loop, task_function)

            await asyncio.sleep(0.001)

    except Exception as e:
        logger.exception(e)
        raise
    finally:
        window.close()


# ============== Example Usage ==============

async def example_task(window: psg.Window, params: dict):
    """Example async task that updates progress bar.

    Args:
        window: The window for UI updates
        params: Task parameters
    """
    for i in range(101):
        await asyncio.sleep(0.05)
        window["-progress-bar-"].update(i)
        window["-progress-text-"].update(f"Processing... {i}%")
    return True


def main():
    """Example main function demonstrating UI usage."""
    # Example configuration
    config = {
        "name": "Example",
        "value": "100",
        "description": "A sample configuration",
    }

    window = make_ui(config)
    loop = asyncio.new_event_loop()

    try:
        loop.run_until_complete(ui_event_loop(window, loop, example_task))
    finally:
        loop.close()


if __name__ == "__main__":
    main()
