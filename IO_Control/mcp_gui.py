import tkinter as tk
from tkinter import ttk
import board
import busio
import digitalio
from adafruit_mcp230xx.mcp23017 import MCP23017

# Initialize I2C and MCP23017
i2c = busio.I2C(board.SCL, board.SDA)
mcp = MCP23017(i2c, address=0x20)

# Setup A0-A7 as outputs
pins = []
for pin_num in range(8):
    pin = mcp.get_pin(pin_num)
    pin.direction = digitalio.Direction.OUTPUT
    pin.value = False  # start LOW
    pins.append(pin)

# === GUI Setup ===
root = tk.Tk()
root.title("MCP23017 A Pins Controller")
root.geometry("500x300")
root.configure(bg="#2c3e50")

# Header label
header = tk.Label(root, text="MCP23017 A0–A7 Control Panel", font=("Arial", 18, "bold"), bg="#2c3e50", fg="white")
header.pack(pady=10)

# Frame for pin controls
frame = ttk.Frame(root, padding=10)
frame.pack()

# Indicator + button containers
indicators = []
buttons = []

def update_indicators():
    for i, pin in enumerate(pins):
        color = "green" if pin.value else "red"
        indicators[i].config(bg=color)

def toggle_pin(idx):
    pins[idx].value = not pins[idx].value
    update_indicators()

def set_pin(idx, state):
    pins[idx].value = state
    update_indicators()

def show_status():
    status = "\n".join([f"A{i}: {'HIGH' if p.value else 'LOW'}" for i, p in enumerate(pins)])
    status_window = tk.Toplevel(root)
    status_window.title("Pin Status")
    tk.Label(status_window, text=status, font=("Courier", 12)).pack(padx=20, pady=20)

# Create buttons and indicators
for i in range(8):
    row = ttk.Frame(frame, padding=5)
    row.grid(row=i, column=0, sticky="w")

    label = ttk.Label(row, text=f"A{i}", width=4)
    label.pack(side="left")

    indicator = tk.Label(row, text=" ", bg="red", width=2, height=1, relief="groove")
    indicator.pack(side="left", padx=5)
    indicators.append(indicator)

    btn_toggle = ttk.Button(row, text="Toggle", command=lambda idx=i: toggle_pin(idx))
    btn_toggle.pack(side="left", padx=5)

    btn_on = ttk.Button(row, text="ON", command=lambda idx=i: set_pin(idx, True))
    btn_on.pack(side="left", padx=5)

    btn_off = ttk.Button(row, text="OFF", command=lambda idx=i: set_pin(idx, False))
    btn_off.pack(side="left", padx=5)

# Status button
status_btn = ttk.Button(root, text="Show Status", command=show_status)
status_btn.pack(pady=10)

# Exit button
exit_btn = ttk.Button(root, text="Exit", command=root.quit)
exit_btn.pack()

# Initialize indicators
update_indicators()

# Run GUI loop
root.mainloop()
