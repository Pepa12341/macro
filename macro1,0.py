import tkinter as tk
from tkinter import ttk
import threading
import time
import ctypes
from pynput import mouse, keyboard

# Enable High DPI awareness for crisp fonts on Windows
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)
except Exception:
    try:
        ctypes.windll.user32.SetProcessDPIAware()
    except Exception:
        pass  # Fallback for non-Windows platforms

class PrecisionMacroGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AeroMacro v6.0")
        self.root.geometry("480x590") # Increased height slightly for speed controls
        self.root.resizable(False, False)
        
        # Enable Always on Top by default
        self.root.attributes("-topmost", True)
        
        # Color Palette (Modern Dark Theme)
        self.bg_main = "#1e1e24"
        self.bg_card = "#2a2a35"
        self.fg_light = "#f8f9fa"
        self.fg_muted = "#95a5a6"
        self.accent_green = "#2ecc71"
        self.accent_blue = "#3498db"
        self.accent_red = "#e74c3c"
        self.accent_orange = "#e67e22"

        self.root.configure(bg=self.bg_main)
        
        # Macro State Variables
        self.recording = False
        self.playing = False
        self.events = []
        self.start_time = 0
        
        # Default Hotkeys (Binds)
        self.record_bind = keyboard.Key.f9
        self.play_bind = keyboard.Key.f10
        self.binding_target = None  # Tracks active rebind ('record' or 'play')
        
        self.setup_styles()
        self.setup_ui()
        
        # Initialize background listeners for global tracking
        self.key_listener = keyboard.Listener(on_press=self.global_on_press, on_release=self.global_on_release)
        self.key_listener.daemon = True
        self.key_listener.start()
        
        self.mouse_listener = mouse.Listener(on_move=self.global_on_move, on_click=self.global_on_click, on_scroll=self.global_on_scroll)
        self.mouse_listener.daemon = True
        self.mouse_listener.start()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Main container style
        style.configure("Main.TFrame", background=self.bg_main)
        
        # Section Card styles
        style.configure("Card.TLabelframe", background=self.bg_card, bordercolor="#3a3a4a", borderwidth=1)
        style.configure("Card.TLabelframe.Label", background=self.bg_card, foreground=self.accent_blue, font=("Segoe UI", 10, "bold"))
        style.configure("Inner.TFrame", background=self.bg_card)
        
        # Label styles
        style.configure("Light.TLabel", background=self.bg_card, foreground=self.fg_light, font=("Segoe UI", 10))
        style.configure("Muted.TLabel", background=self.bg_main, foreground=self.fg_muted, font=("Segoe UI", 9, "italic"))
        
        # Notebook / Tabs style
        style.configure("TNotebook", background=self.bg_main, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.bg_card, foreground=self.fg_muted, font=("Segoe UI", 9, "bold"), padding=6)
        style.map("TNotebook.Tab", background=[("selected", self.bg_main)], foreground=[("selected", self.fg_light)])
        
        # Button & Spinbox styles
        style.configure("TButton", background="#3a3a4a", foreground=self.fg_light, borderwidth=0, font=("Segoe UI", 9, "bold"), padding=6)
        style.map("TButton", background=[("active", "#4a4a5a")])
        style.configure("TSpinbox", fieldbackground="#3a3a4a", background="#3a3a4a", foreground=self.fg_light, borderwidth=0, font=("Segoe UI", 10))
        
        # Checkbutton style
        style.configure("TCheckbutton", background=self.bg_card, foreground=self.fg_muted, font=("Segoe UI", 9))
        style.map("TCheckbutton", foreground=[("selected", self.fg_light)])
        
        # Action Buttons
        style.configure("ActionRed.TButton", background=self.accent_red, foreground=self.fg_light, font=("Segoe UI", 10, "bold"), padding=10)
        style.map("ActionRed.TButton", background=[("active", "#b3392b")])
        style.configure("ActionBlue.TButton", background=self.accent_blue, foreground=self.fg_light, font=("Segoe UI", 10, "bold"), padding=10)
        style.map("ActionBlue.TButton", background=[("active", "#2980b9")])

    def setup_ui(self):
        # Create Notebook for Tabs
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # TAB 1: MACRO CONTROLLER
        macro_frame = ttk.Frame(self.notebook, style="Main.TFrame", padding="15")
        self.notebook.add(macro_frame, text=" Macro Engine ")
        
        # 1. STATUS PANEL
        status_card = ttk.LabelFrame(macro_frame, text=" ENGINE STATUS ", style="Card.TLabelframe", padding="12")
        status_card.pack(fill=tk.X, pady=(0, 10))
        
        self.lbl_status = tk.Label(status_card, text="READY", font=("Segoe UI", 16, "bold"), fg=self.accent_green, bg=self.bg_card)
        self.lbl_status.pack(pady=(0, 6))
        
        self.always_on_top_var = tk.BooleanVar(value=True)
        self.chk_ontop = ttk.Checkbutton(status_card, text="Keep window always on top", variable=self.always_on_top_var, command=self.toggle_always_on_top, style="TCheckbutton")
        self.chk_ontop.pack()
        
        # 2. HOTKEYS CONFIGURATION
        binds_card = ttk.LabelFrame(macro_frame, text=" GLOBAL HOTKEYS ", style="Card.TLabelframe", padding="12")
        binds_card.pack(fill=tk.X, pady=10)
        
        inner_binds = ttk.Frame(binds_card, style="Inner.TFrame")
        inner_binds.pack(fill=tk.X)
        
        ttk.Label(inner_binds, text="Record / Stop:", style="Light.TLabel").grid(row=0, column=0, sticky=tk.W, pady=6)
        self.btn_record_bind = ttk.Button(inner_binds, text=self.format_key(self.record_bind), command=lambda: self.start_binding('record'))
        self.btn_record_bind.grid(row=0, column=1, sticky=tk.E, pady=6)
        
        ttk.Label(inner_binds, text="Playback / Stop:", style="Light.TLabel").grid(row=1, column=0, sticky=tk.W, pady=6)
        self.btn_play_bind = ttk.Button(inner_binds, text=self.format_key(self.play_bind), command=lambda: self.start_binding('play'))
        self.btn_play_bind.grid(row=1, column=1, sticky=tk.E, pady=6)
        inner_binds.grid_columnconfigure(1, weight=1)
        
        # 3. PLAYBACK SETTINGS
        settings_card = ttk.LabelFrame(macro_frame, text=" PLAYBACK OPTIONS ", style="Card.TLabelframe", padding="12")
        settings_card.pack(fill=tk.X, pady=10)
        
        inner_settings = ttk.Frame(settings_card, style="Inner.TFrame")
        inner_settings.pack(fill=tk.X)
        
        # Repeat Count Row
        ttk.Label(inner_settings, text="Repeat count (0 = Infinite loop):", style="Light.TLabel").grid(row=0, column=0, sticky=tk.W, pady=4)
        self.ent_loops = ttk.Spinbox(inner_settings, from_=0, to=99999, width=8, style="TSpinbox")
        self.ent_loops.set(1)
        self.ent_loops.grid(row=0, column=1, sticky=tk.E, pady=4)
        
        # Speed Multiplier Row
        ttk.Label(inner_settings, text="Speed Multiplier (0.1x - 10.0x):", style="Light.TLabel").grid(row=1, column=0, sticky=tk.W, pady=4)
        self.ent_speed = ttk.Spinbox(inner_settings, from_=0.1, to=10.0, increment=0.1, width=8, style="TSpinbox")
        self.ent_speed.set(1.0)
        self.ent_speed.grid(row=1, column=1, sticky=tk.E, pady=4)
        inner_settings.grid_columnconfigure(1, weight=1)
        
        # 4. MANUAL CONTROLS
        ctrl_frame = ttk.Frame(macro_frame, style="Main.TFrame")
        ctrl_frame.pack(fill=tk.X, pady=(15, 5))
        
        self.btn_manual_record = ttk.Button(ctrl_frame, text="Start Recording", style="ActionRed.TButton", command=self.toggle_record)
        self.btn_manual_record.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 8))
        
        self.btn_manual_play = ttk.Button(ctrl_frame, text="Run Macro", style="ActionBlue.TButton", command=self.toggle_playback)
        self.btn_manual_play.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(8, 0))
        
        ttk.Label(macro_frame, text="Open Source Utility • Safe & Local Execution", style="Muted.TLabel").pack(side=tk.BOTTOM, pady=(5, 0))

        # TAB 2: GUIDE / HELP
        guide_frame = ttk.Frame(self.notebook, style="Main.TFrame", padding="20")
        self.notebook.add(guide_frame, text=" Help & Tutorial ")
        
        guide_text = (
            "🚀 Quick Start Guide\n"
            "--------------------------------------------------\n\n"
            "1. CONFIGURE HOTKEYS\n"
            "   Click the key-display buttons under 'GLOBAL HOTKEYS' "
            "to custom-bind macro execution shortcuts to any key on your keyboard.\n\n"
            "2. RECORDING A SEQUENCE\n"
            "   Press your Record hotkey (Default: F9) or click 'Start Recording'. "
            "Perform your actions. Press the hotkey again to save your mouse tracks, "
            "exact delays, holds, and key sequences.\n\n"
            "3. SETTING REPEATS & SPEED\n"
            "   Adjust the loop counter (0 for infinite loops). "
            "Use the 'Speed Multiplier' to scale playback timing. "
            "2.0x executes everything twice as fast, while 0.5x cuts execution speed in half.\n\n"
            "4. PLAYBACK & HALTING\n"
            "   Press your Playback hotkey (Default: F10) or click 'Run Macro'. "
            "To instantly stop execution mid-macro, tap the playback hotkey again.\n\n"
            "--------------------------------------------------\n"
            "ℹ️ Fix Note: Mouse click delivery updated to ensure registration "
            "inside background windows and game clients."
        )
        
        txt_box = tk.Text(guide_frame, bg=self.bg_card, fg=self.fg_light, font=("Segoe UI", 10), wrap=tk.WORD, bd=0, padx=10, pady=10)
        txt_box.insert(tk.END, guide_text)
        txt_box.config(state=tk.DISABLED) # Make read-only
        txt_box.pack(fill=tk.BOTH, expand=True)

    def toggle_always_on_top(self):
        is_checked = self.always_on_top_var.get()
        self.root.attributes("-topmost", is_checked)

    def format_key(self, key):
        if key is None:
            return " NOT SET "
        if hasattr(key, 'char') and key.char is not None:
            return f"  {key.char.upper()}  "
        else:
            s = str(key).replace("Key.", "")
            return f"  {s.upper()}  "

    def update_status(self, text, color):
        self.root.after(0, lambda: self.lbl_status.config(text=text, fg=color))

    def start_binding(self, target):
        if self.recording or self.playing:
            return
        self.binding_target = target
        self.update_status("PRESS ANY KEY...", self.accent_orange)
        if target == 'record':
            self.btn_record_bind.config(text="Listening...")
        else:
            self.btn_play_bind.config(text="Listening...")

    def toggle_record(self):
        if self.playing:
            return
        if not self.recording:
            self.events = []
            self.start_time = time.time()
            self.recording = True
            self.update_status("RECORDING ACTIVE", self.accent_red)
            self.btn_manual_record.config(text="Stop Recording")
        else:
            self.recording = False
            self.update_status("RECORDING SAVED / READY", self.accent_green)
            self.btn_manual_record.config(text="Start Recording")

    def toggle_playback(self):
        if self.recording:
            return
        if not self.playing:
            if not self.events:
                self.update_status("NO DATA TO PLAY!", self.accent_red)
                return
            threading.Thread(target=self.play_macro, daemon=True).start()
        else:
            self.playing = False
            self.update_status("HALTING ENGINE...", self.accent_orange)

    # --- INPUT CAPTURE ENGINE ---

    def global_on_press(self, key):
        if self.binding_target:
            if self.binding_target == 'record':
                self.record_bind = key
                self.root.after(0, lambda: self.btn_record_bind.config(text=self.format_key(key)))
            elif self.binding_target == 'play':
                self.play_bind = key
                self.root.after(0, lambda: self.btn_play_bind.config(text=self.format_key(key)))
            self.binding_target = None
            self.update_status("HOTKEY SAVED", self.accent_green)
            return

        if key == self.record_bind:
            self.root.after(0, self.toggle_record)
            return
        elif key == self.play_bind:
            self.root.after(0, self.toggle_playback)
            return

        if self.recording:
            self.events.append(('key_press', time.time() - self.start_time, key))

    def global_on_release(self, key):
        if self.recording and key != self.record_bind and key != self.play_bind:
            self.events.append(('key_release', time.time() - self.start_time, key))

    def global_on_move(self, x, y):
        if self.recording:
            self.events.append(('mouse_move', time.time() - self.start_time, (x, y)))

    def global_on_click(self, x, y, button, pressed):
        if self.recording:
            self.events.append(('mouse_click', time.time() - self.start_time, (x, y, button, pressed)))

    def global_on_scroll(self, x, y, dx, dy):
        if self.recording:
            self.events.append(('mouse_scroll', time.time() - self.start_time, (x, y, dx, dy)))

    # --- SIMULATION ENGINE (With Speed Modifiers) ---

    def play_macro(self):
        self.playing = True
        try:
            loops = int(self.ent_loops.get())
        except ValueError:
            loops = 1

        try:
            speed_mult = float(self.ent_speed.get())
            if speed_mult <= 0:
                speed_mult = 1.0
        except ValueError:
            speed_mult = 1.0

        mouse_ctrl = mouse.Controller()
        key_ctrl = keyboard.Controller()
        
        loop_count = 0
        infinite = (loops == 0)

        while infinite or loop_count < loops:
            if not self.playing:
                break
                
            loop_count += 1
            status_text = f"PLAYING (Loop {loop_count})" if infinite else f"PLAYING ({loop_count}/{loops})"
            self.update_status(status_text, self.accent_blue)
            
            playback_start = time.time()
            
            for event_type, event_time, data in self.events:
                if not self.playing:
                    break
                
                # Dynamic speed calculation scaling the timeline event target
                scaled_event_time = event_time / speed_mult
                
                # High-fidelity time alignment
                while True:
                    if not self.playing:
                        break
                    elapsed = time.time() - playback_start
                    if elapsed >= scaled_event_time:
                        break
                    remaining = scaled_event_time - elapsed
                    if remaining > 0.01:
                        time.sleep(remaining - 0.005)
                
                if not self.playing:
                    break

                # Execution logic
                if event_type == 'key_press':
                    key_ctrl.press(data)
                elif event_type == 'key_release':
                    key_ctrl.release(data)
                elif event_type == 'mouse_move':
                    mouse_ctrl.position = data
                elif event_type == 'mouse_click':
                    x, y, button, pressed = data
                    mouse_ctrl.position = (x, y)
                    
                    if pressed:
                        mouse_ctrl.press(button)
                    else:
                        # Scaled tiny buffer cushion for human click registration safety
                        time.sleep(max(0.002, 0.012 / speed_mult)) 
                        mouse_ctrl.release(button)
                        
                elif event_type == 'mouse_scroll':
                    x, y, dx, dy = data
                    mouse_ctrl.position = (x, y)
                    mouse_ctrl.scroll(dx, dy)

        self.playing = False
        self.update_status("READY", self.accent_green)

if __name__ == "__main__":
    root = tk.Tk()
    app = PrecisionMacroGUI(root)
    root.mainloop()