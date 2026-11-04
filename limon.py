"""Limon: fixed image, gently animated smile; Python 3 standard library only."""
from pathlib import Path
import math
import random
import time
import tkinter as tk

BASE = Path(__file__).resolve().parent
IMAGE = BASE / "limon_sabit.png"

root = tk.Tk()
root.title("Limon 🍋 — Doğal Göz Kırpma")
root.configure(bg="white")
root.resizable(False, False)

photo = tk.PhotoImage(file=str(IMAGE))
w, h = photo.width(), photo.height()
canvas = tk.Canvas(root, width=w, height=h, bg="white", highlightthickness=0)
canvas.pack(padx=16, pady=(12, 4))
canvas.create_image(0, 0, anchor="nw", image=photo)

# Only the eye-area overlays change while blinking. The original image remains intact.
half_photo = tk.PhotoImage(file=str(BASE / "goz_half.png"))
closed_photo = tk.PhotoImage(file=str(BASE / "goz_closed.png"))
blink_overlay = canvas.create_image(0, 0, anchor="nw", image=half_photo, state="hidden")
blink_steps = [None, half_photo, closed_photo, half_photo, None]
blink_index = -1
next_blink_at = time.monotonic() + 2.5


# Background photo never changes. A fine black mouth stroke and tiny eye reflections animate.
segments = 48
x0, x1 = 185, 255
smile_y, depth = 283, 17
xs = [x0 + (x1-x0) * i / segments for i in range(segments+1)]
line = canvas.create_line(0, 0, 0, 0, fill="#181818", width=4.3, capstyle=tk.ROUND, joinstyle=tk.ROUND, smooth=True, splinesteps=14)

# The eyes are already in the ORIGINAL photo. We add only tiny moving
# light glints (about 1 pixel), rather than shifting or redrawing the face.
eye_glints = [
    canvas.create_oval(164, 233, 166, 235, outline="", fill="#ece9d9"),
    canvas.create_oval(280, 233, 282, 235, outline="", fill="#ece9d9"),
]
running = False
phase = 0.0

def blink_now():
    global blink_index, next_blink_at
    blink_index = 0
    next_blink_at = time.monotonic() + random.uniform(3.0, 6.0)


def animate():
    global phase, blink_index
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
    # Very gentle eye twinkle: shifts <= 1 px, with no image-frame jumps.
    shift = math.sin(phase * 0.14) * 0.85
    pulse = math.cos(phase * 0.19)
    for dot, cx in zip(eye_glints, (165, 281)):
        radius = 0.85 + 0.15 * pulse
        cy = 234 + 0.45 * math.sin(phase * 0.11)
        canvas.coords(dot, cx + shift - radius, cy - radius,
                      cx + shift + radius, cy + radius)
    # Blink naturally every few seconds, independent of mouth movement.
    if blink_index == -1 and time.monotonic() >= next_blink_at:
        blink_now()
    if blink_index >= 0:
        selected = blink_steps[blink_index]
        if selected is None:
            canvas.itemconfigure(blink_overlay, state="hidden")
        else:
            canvas.itemconfigure(blink_overlay, image=selected, state="normal")
        blink_index += 1
        if blink_index >= len(blink_steps):
            blink_index = -1
    # Keep the drawn mouth above the blinking overlay.
    canvas.tag_raise(line)
    root.after(40, animate)

def toggle():
    global running
    running = not running
    btn.config(text="⏸  Durdur" if running else "〰  Konuşma hareketini dene")
    status.config(text="Ağız dalgalanıyor; gözler ara sıra kırpılıyor" if running else "Limon gülümsüyor")

btn = tk.Button(root, text="〰  Konuşma hareketini dene", command=toggle,
                font=("Helvetica", 14), fg="#292518", bg="#ffe66d", padx=14, pady=10)
btn.pack(pady=(8, 6))
blink_btn = tk.Button(root, text="😉  Göz kırpmayı dene", command=blink_now,
                      font=("Helvetica", 12), fg="#292518", bg="white", padx=12, pady=6)
blink_btn.pack(pady=(0, 6))
status = tk.Label(root, text="Limon gülümsüyor", bg="white", fg="#626262", font=("Helvetica", 12))
status.pack(pady=(0, 14))

animate()
root.mainloop()
