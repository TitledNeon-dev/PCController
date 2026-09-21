"""
Model Context Protocol (MCP) Server for PCController (Peak Performance Edition).
Exposes 26 ultra-low latency PC automation, vision, and hardware perception tools to AI Assistants.
Supports stdio (default) and SSE transports.
"""
import sys
import json
import argparse
from typing import Optional, List

try:
    from mcp.server.mcpserver import MCPServer, Image
except ImportError:
    from mcp.server.fastmcp import FastMCP as MCPServer, Image

import pc_controller

mcp = MCPServer("PCController")


# ==============================================================================
# SYSTEM & STATUS
# ==============================================================================

@mcp.tool()
def get_system_info() -> str:
    """Returns a full real-time snapshot of system state: resolution, mouse position, active window, window count."""
    info = pc_controller.get_system_info()
    return json.dumps(info, ensure_ascii=False)


@mcp.tool()
def get_screen_size() -> str:
    """Returns primary screen width and height in pixels."""
    size = pc_controller.get_screen_size()
    return json.dumps(size)


# ==============================================================================
# VISION & SCREENSHOTS
# ==============================================================================

@mcp.tool()
def take_screenshot(filename: str = "screen.jpg", quality: int = 80, max_width: int = 0) -> str:
    """
    Takes an ultra-fast full-screen screenshot and saves it to captures directory.
    Default JPEG format provides 3-5x faster capture and 10x smaller file size than PNG.
    max_width: If > 0, resizes screenshot to max_width (e.g. 1280) to save disk/bandwidth.
    Returns the absolute file path of saved image.
    """
    mw = max_width if max_width > 0 else None
    path = pc_controller.take_screenshot(filename, quality=quality, max_width=mw)
    return f"Screenshot saved to: {path}"


@mcp.tool()
def capture_screen_vision(quality: int = 75, max_width: int = 1280) -> Image:
    """
    Direct multimodal vision tool: captures the screen and returns it as a native MCP Image
    so the AI can immediately SEE the screen contents in full fidelity without reading files from disk.
    """
    data = pc_controller.capture_screen_bytes(quality=quality, max_width=max_width)
    return Image(data=data, format="jpeg")


@mcp.tool()
def find_image_on_screen(template_path: str, threshold: float = 0.8) -> str:
    """
    Locates an image template (icon, button) on the screen using OpenCV template matching.
    Returns center coordinate (x, y), dimensions, and match confidence.
    """
    res = pc_controller.find_image_on_screen(template_path, threshold=threshold)
    if res:
        return json.dumps({"status": "found", "match": res})
    return json.dumps({"status": "not_found", "threshold": threshold})


@mcp.tool()
def click_image(template_path: str, threshold: float = 0.8, clicks: int = 1, button: str = "left") -> str:
    """
    Finds an image template on screen and clicks on it immediately in one step.
    """
    res = pc_controller.click_image(template_path, threshold=threshold, clicks=clicks, button=button)
    return json.dumps(res)


# ==============================================================================
# MOUSE CONTROL
# ==============================================================================

@mcp.tool()
def get_mouse_position() -> str:
    """Returns current (x, y) coordinates of mouse cursor via native Win32 API."""
    pos = pc_controller.get_mouse_position()
    return json.dumps(pos)


@mcp.tool()
def mouse_move(x: int, y: int, duration: float = 0.0) -> str:
    """
    Moves mouse cursor to (x, y).
    duration=0.0 performs instantaneous move (< 0.01ms).
    """
    res = pc_controller.mouse_move(x, y, duration=duration)
    return json.dumps(res)


@mcp.tool()
def mouse_click(x: int = -1, y: int = -1, button: str = "left", clicks: int = 1) -> str:
    """
    Clicks mouse instantaneously via native Win32 mouse_event (< 0.05ms).
    If x and y are >= 0, moves to (x, y) before clicking.
    button: 'left', 'right', or 'middle'.
    clicks: 1 for single click, 2 for double click.
    """
    if x >= 0 and y >= 0:
        res = pc_controller.mouse_click(x=x, y=y, button=button, clicks=clicks)
    else:
        res = pc_controller.mouse_click(button=button, clicks=clicks)
    return json.dumps(res)


@mcp.tool()
def mouse_drag(to_x: int, to_y: int, from_x: int = -1, from_y: int = -1, duration: float = 0.15, button: str = "left") -> str:
    """
    Drags mouse from current position (or from_x, from_y) to (to_x, to_y).
    """
    fx = from_x if from_x >= 0 else None
    fy = from_y if from_y >= 0 else None
    res = pc_controller.mouse_drag(to_x=to_x, to_y=to_y, from_x=fx, from_y=fy, duration=duration, button=button)
    return json.dumps(res)


@mcp.tool()
def mouse_scroll(clicks: int = -3) -> str:
    """
    Scrolls mouse wheel.
    Negative values scroll down, positive values scroll up.
    """
    res = pc_controller.mouse_scroll(clicks=clicks)
    return json.dumps(res)


# ==============================================================================
# KEYBOARD CONTROL
# ==============================================================================

@mcp.tool()
def keyboard_type(text: str, interval: float = 0.0) -> str:
    """
    Instantaneous batch typing into active window via Windows SendInput API (< 0.1ms).
    Supports full Unicode (Russian, English, digits, symbols, emojis).
    """
    res = pc_controller.keyboard_type(text, interval=interval)
    return json.dumps(res)


@mcp.tool()
def keyboard_press(key: str) -> str:
    """
    Presses a single key (e.g. 'enter', 'esc', 'tab', 'space', 'backspace', 'win', 'f5').
    """
    res = pc_controller.keyboard_press(key)
    return json.dumps(res)


@mcp.tool()
def keyboard_hotkey(keys: List[str]) -> str:
    """
    Presses a hotkey combination, e.g. ['ctrl', 'c'], ['alt', 'tab'], ['win', 'r'].
    Automatically ensures all modifier keys are cleanly released.
    """
    res = pc_controller.keyboard_hotkey(*keys)
    return json.dumps(res)


# ==============================================================================
# CLIPBOARD
# ==============================================================================

@mcp.tool()
def clipboard_get() -> str:
    """Gets the current plain text from the system clipboard."""
    return pc_controller.clipboard_get()


@mcp.tool()
def clipboard_set(text: str) -> str:
    """Sets the system clipboard to the specified text."""
    res = pc_controller.clipboard_set(text)
    return json.dumps(res)


# ==============================================================================
# WINDOW & APP MANAGEMENT
# ==============================================================================

@mcp.tool()
def list_windows() -> str:
    """Lists currently open and visible desktop application windows with their positions and dimensions."""
    windows = pc_controller.list_windows()
    return json.dumps(windows, ensure_ascii=False)


@mcp.tool()
def get_active_window() -> str:
    """Returns the title and geometry of currently active/focused window."""
    w = pc_controller.get_active_window()
    return json.dumps(w, ensure_ascii=False)


@mcp.tool()
def focus_window(title_keyword: str, maximize: bool = False) -> str:
    """
    Brings the window matching `title_keyword` to foreground.
    maximize: If True, maximizes the window across the screen.
    """
    res = pc_controller.focus_window(title_keyword, maximize=maximize)
    return json.dumps(res, ensure_ascii=False)


@mcp.tool()
def minimize_window(title_keyword: str) -> str:
    """Minimizes the window matching `title_keyword`."""
    res = pc_controller.minimize_window(title_keyword)
    return json.dumps(res, ensure_ascii=False)


@mcp.tool()
def close_window(title_keyword: str) -> str:
    """Gracefully closes the window matching `title_keyword`."""
    res = pc_controller.close_window(title_keyword)
    return json.dumps(res, ensure_ascii=False)


@mcp.tool()
def wait_for_window(title_keyword: str, timeout: float = 5.0) -> str:
    """
    Smart-polls until window containing `title_keyword` appears or timeout expires.
    Returns JSON window info or error status.
    """
    res = pc_controller.wait_for_window(title_keyword, timeout=timeout)
    if res:
        return json.dumps({"status": "found", "window": res}, ensure_ascii=False)
    return json.dumps({"status": "timeout", "keyword": title_keyword})


@mcp.tool()
def launch_app(command: str, wait_for_title: str = "", timeout: float = 5.0) -> str:
    """
    Asynchronously launches any Windows application (e.g. 'chrome https://google.com', 'notepad', 'calc').
    If wait_for_title is specified, smart-polls until window appears and focuses it.
    """
    wt = wait_for_title.strip() if wait_for_title else None
    res = pc_controller.launch_app(command, wait_for_title=wt, timeout=timeout)
    return json.dumps(res, ensure_ascii=False)


# ==============================================================================
# HARDWARE PERCEPTION (WEBCAM & MIC)
# ==============================================================================

@mcp.tool()
def get_media_devices() -> str:
    """
    Discovers all available microphones (with channel counts) and connected webcam devices.
    """
    devices = pc_controller.get_media_devices()
    return json.dumps(devices, ensure_ascii=False)


@mcp.tool()
def capture_webcam(filename: str = "webcam.jpg", camera_index: int = 0) -> str:
    """
    Captures a single snapshot from webcam.
    Returns the absolute path to saved image.
    """
    path = pc_controller.capture_webcam(filename=filename, camera_index=camera_index)
    return f"Webcam photo saved to: {path}"


@mcp.tool()
def record_mic(filename: str = "mic.wav", duration: int = 5, device_index: int = -1) -> str:
    """
    Records audio from microphone for `duration` seconds.
    device_index: Optional specific microphone index from get_media_devices (-1 = default).
    Returns JSON with file path, duration, peak amplitude, and whether voice/sound was detected.
    """
    dev = device_index if device_index >= 0 else None
    res = pc_controller.record_audio(filename=filename, duration=duration, device_index=dev)
    return json.dumps(res, ensure_ascii=False)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="PCController Peak Performance MCP Server")
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse"],
        default="stdio",
        help="Transport protocol (default: stdio)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for SSE transport (default: 8000)")
    args = parser.parse_args()

    if args.transport == "sse":
        print(f"Starting PCController MCP server on SSE transport at port {args.port}...")
        mcp.run(transport="sse", port=args.port)
    else:
        mcp.run(transport="stdio")
