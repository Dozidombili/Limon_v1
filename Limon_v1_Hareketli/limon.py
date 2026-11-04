"""Limon: fixed image, gently animated smile; Python 3 standard library only."""
from pathlib import Path
import math
import tkinter as tk

BASE = Path(__file__).resolve().parent
IMAGE = BASE / "limon_sabit.png"

root = tk.Tk()
root.title("Limon 🍋 — Hareketli Gülümseme")
root.configure(bg="white")
root.resizable(False, False)

photo = tk.PhotoImage(file=str(IMAGE))
w, h = photo.width(), photo.height()
canvas = tk.Canvas(root, width=w, height=h, bg="white", highlightthickness=0)
canvas.pack(padx=16, pady=(12, 4))
canvas.create_image(0, 0, anchor="nw", image=photo)

# Only this black line changes. Image, eyes, leaf and skin stay perfectly still.
segments = 48
x0, x1 = 190, 250
smile_y, depth = 283, 17
xs = [x0 + (x1-x0) * i / segments for i in range(segments+1)]
line = canvas.create_line(0, 0, 0, 0, fill="#181818", width=4.8, capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True, splinesteps=14)

running = False
phase = 0.0

def animate():
    global phase
    phase += 0.16
    pts = []
    for x in xs:
        u = (x-x0)/(x1-x0)
        curve = smile_y + 4 * depth * u * (1-u)
        # Fade the waveform to zero at both corners of the smile.
        envelope = math.sin(math.pi*u) ** 1.25
        wave = (3.6 * math.sin(u*5*math.pi-phase) + 1.0 * math.sin(u*9*math.pi+phase*.6)) * envelope if running else 0
        pts.extend((x, curve+wave))
    canvas.coords(line, *pts)
    root.after(33, animate)

def toggle():
    global running
    running = not running
    btn.config(text="⏸  Durdur" if running else "〰  Konuşma hareketini dene")
    status.config(text="Sadece ağız dalgalanıyor" if running else "Limon gülümsüyor")

btn = tk.Button(root, text="〰  Konuşma hareketini dene", command=toggle,
                font=("Helvetica", 14), fg="#292518", bg="#ffe66d", padx=14, pady=10)
btn.pack(pady=(8, 6))
status = tk.Label(root, text="Limon gülümsüyor", bg="white", fg="#626262", font=("Helvetica", 12))
status.pack(pady=(0, 14))

animate()
root.mainloop()
