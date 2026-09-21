"""
PCController: Comprehensive Diagnostic & Live End-to-End Benchmark.
Combines subsystem micro-benchmarks with the live automation pipeline.
"""
import sys
import time
import random
from pathlib import Path

# Fix console encoding on Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import cv2
import pc_controller

def run_subsystem_diagnostics():
    print("===============================================================")
    print("   [PART 1] SUBSYSTEM LATENCY & HARDWARE DIAGNOSTICS")
    print("===============================================================\n")

    # 1. System Snapshot
    info = pc_controller.get_system_info()
    print(f"[1] System State: {info['screen_resolution']} | Cursor: ({info['mouse_cursor']['x']}, {info['mouse_cursor']['y']})")
    print(f"    Active: {info['active_window']} | Open Windows: {info['total_windows_open']}")

    # 2. Mouse SetCursorPos
    t0 = time.perf_counter()
    pc_controller.mouse_move(500, 500, duration=0.0)
    dt_mouse = (time.perf_counter() - t0) * 1000
    print(f"[2] Win32 SetCursorPos: {dt_mouse:.3f} ms")

    # 3. Batch Unicode Typing
    test_str = "Тест скорости ввода: Hello World! 123"
    t0 = time.perf_counter()
    pc_controller.keyboard_type(test_str, interval=0.0)
    dt_type = (time.perf_counter() - t0) * 1000
    print(f"[3] Batch SendInput ({len(test_str)} chars Unicode): {dt_type:.3f} ms")

    # 4. Turbo Screenshot
    t0 = time.perf_counter()
    shot_path = pc_controller.take_screenshot("diag_screen.jpg", quality=80)
    dt_shot = (time.perf_counter() - t0) * 1000
    shot_size_kb = Path(shot_path).stat().st_size / 1024
    print(f"[4] Turbo Screenshot (1080p JPEG): {dt_shot:.2f} ms ({shot_size_kb:.1f} KB)")

    # 5. Multimodal In-Memory Vision Stream
    t0 = time.perf_counter()
    img_bytes = pc_controller.capture_screen_bytes(quality=75, max_width=1280)
    dt_stream = (time.perf_counter() - t0) * 1000
    print(f"[5] Multimodal In-Memory Vision Stream: {dt_stream:.2f} ms ({len(img_bytes)/1024:.1f} KB)")

    # 6. Template Matching
    full_img = cv2.imread(shot_path)
    h, w = full_img.shape[:2]
    crop_x, crop_y = w // 2 - 30, h // 2 - 20
    template_patch = full_img[crop_y:crop_y+40, crop_x:crop_x+60]
    template_file = str(pc_controller.CAPTURES_DIR / "sample_icon.png")
    cv2.imwrite(template_file, template_patch)

    t0 = time.perf_counter()
    match = pc_controller.find_image_on_screen(template_file, threshold=0.85)
    dt_match = (time.perf_counter() - t0) * 1000
    if match:
        print(f"[6] OpenCV Template Matching: {dt_match:.2f} ms (Match: {match['confidence']*100:.1f}%)")

    # 7. Window Enumeration
    t0 = time.perf_counter()
    wins = pc_controller.list_windows()
    dt_wins = (time.perf_counter() - t0) * 1000
    print(f"[7] Window Enumeration ({len(wins)} windows): {dt_wins:.2f} ms\n")


def run_live_benchmark():
    print("===============================================================")
    print("   [PART 2] LIVE END-TO-END AUTOMATION PIPELINE")
    print("===============================================================\n")

    bench_results = {}
    t_pipeline_start = time.perf_counter()

    # Step 1: Focus Chrome
    print("[Step 1] Bringing Chrome to Foreground & Maximizing...")
    t0 = time.perf_counter()
    focus_res = pc_controller.focus_window("Chrome", maximize=True)
    t_focus = (time.perf_counter() - t0) * 1000
    bench_results["1. Window Focus & Maximize"] = f"{t_focus:.2f} ms"
    print(f"  Result: {focus_res.get('title', 'Not found')[:60]}")
    print(f"  Latency: {t_focus:.2f} ms\n")

    # Step 2: Instant Address Bar Click & Batch URL Input
    print("[Step 2] Clicking Address Bar & Typing YouTube URL (< 1ms batch)...")
    t0 = time.perf_counter()
    pc_controller.mouse_click(500, 82)
    pc_controller.keyboard_type("https://www.youtube.com", interval=0.0)
    pc_controller.keyboard_press("enter")
    t_type = (time.perf_counter() - t0) * 1000
    bench_results["2. Click + Batch Type + Enter"] = f"{t_type:.2f} ms"
    print(f"  Latency: {t_type:.2f} ms\n")

    # Step 3: Smart Polling for YouTube Load
    print("[Step 3] Smart-Polling until YouTube page loads...")
    t0 = time.perf_counter()
    win = pc_controller.wait_for_window("YouTube", timeout=5.0, poll_interval=0.05)
    t_poll = (time.perf_counter() - t0) * 1000
    bench_results["3. Smart-Wait for YouTube"] = f"{t_poll:.2f} ms"
    print(f"  YouTube Window Title: {win['title'] if win else 'Timeout'}")
    print(f"  Latency: {t_poll:.2f} ms\n")

    # Step 4: Random Video Thumbnail Selection & Click
    video_targets = [(450, 360), (850, 360), (1250, 360)]
    target_x, target_y = random.choice(video_targets)

    print(f"[Step 4] Instant Click on Random Video Thumbnail at ({target_x}, {target_y})...")
    t0 = time.perf_counter()
    pc_controller.mouse_click(target_x, target_y)
    t_click = (time.perf_counter() - t0) * 1000
    bench_results["4. Instant Video Click"] = f"{t_click:.2f} ms"
    print(f"  Latency: {t_click:.2f} ms\n")

    # Step 5: Wait for playback & capture high-speed JPEG screenshot
    print("[Step 5] Waiting for Video Playback & Capturing Turbo Screenshot...")
    time.sleep(1.2)
    t0 = time.perf_counter()
    shot_path = pc_controller.take_screenshot("live_bench_video.jpg", quality=80)
    t_shot = (time.perf_counter() - t0) * 1000
    bench_results["5. Turbo Screenshot (1080p JPEG)"] = f"{t_shot:.2f} ms"
    shot_size_kb = Path(shot_path).stat().st_size / 1024
    print(f"  Screenshot Saved: {shot_path}")
    print(f"  Screenshot Size: {shot_size_kb:.1f} KB")
    print(f"  Screenshot Latency: {t_shot:.2f} ms\n")

    # Step 6: Verify Active Window after click
    active_win = pc_controller.get_active_window()
    active_title = active_win["title"] if active_win else "Unknown"
    print(f"[Step 6] Verifying Video Active State...")
    print(f"  Current Active Window: {active_title}\n")

    t_total = time.perf_counter() - t_pipeline_start
    bench_results["TOTAL PIPELINE TIME"] = f"{t_total:.2f} s"

    print("===============================================================")
    print("                    BENCHMARK SUMMARY TABLE                    ")
    print("===============================================================")
    for step, duration in bench_results.items():
        print(f"  {step.ljust(36)} : {duration}")
    print("===============================================================\n")


if __name__ == "__main__":
    run_subsystem_diagnostics()
    run_live_benchmark()
