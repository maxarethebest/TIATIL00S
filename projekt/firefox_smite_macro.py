import time
import argparse
import ctypes

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


def click_at(x: int, y: int) -> None:
	# Move cursor and perform a left click (Windows)
	ctypes.windll.user32.SetCursorPos(x, y)
	ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
	time.sleep(0.02)
	ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


def main():
	parser = argparse.ArgumentParser(description="Click at 1600,50 a number of times")
	parser.add_argument("--count", type=int, default=1, help="how many clicks to perform")
	parser.add_argument("--delay", type=float, default=0.2, help="seconds to wait before starting (countdown)")
	args = parser.parse_args()
	print(f"Will click at (1600,50) {args.count} time(s) after {args.delay}s countdown.")
	for i in range(int(args.delay), 0, -1):
		print(i, end="... ", flush=True)
		time.sleep(1)
	print("Go!")

	for i in range(args.count):
		click_at(1600, 50)
		if i != args.count - 1:
			time.sleep(0.2)


if __name__ == "__main__":
	main()