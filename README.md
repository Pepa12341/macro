```markdown
# AeroMacro v6.0 🚀

A lightweight, high-fidelity, and fully open-source macro recording and playback utility built with Python. **AeroMacro** captures both mouse and keyboard peripherals with millisecond-level precision using a low-overhead background listener architecture.

Featuring a modern dark-mode user interface, global system-wide hotkeys, dynamic speed scaling, an integrated guide, and an infinite loop engine.

---

## ✨ Key Features

- **🎯 Micro-Actuation Precision:** Features a high-fidelity timeline spin-lock synchronization algorithm to replicate inputs precisely as they were recorded.
- **⚡ Dynamic Speed Scaling:** Adjust reproduction playback speeds anywhere from `0.1x` (slow motion) up to `10.0x` (lightning fast) on the fly.
- **♾️ Infinite Loops:** Inputting `0` in the repeat configuration cycles the execution infinitely until manually halted.
- **📌 Always-on-Top Toggle:** Pin the interface overlaying all other system windows and games, or uncheck it for standard window behavior.
- **⌨️ Universal Hotkey Rebinding:** Rebind macro trigger actions to *any* hardware key (including `Ctrl`, `Caps Lock`, `F-keys`, or multimedia buttons) directly from the GUI.
- **🛠️ Background Click Cushion:** Includes an automated micro-delay mechanism (`0.012s` actuation cushion) ensuring that mouse click releases safely register inside background applications, browsers, and game windows without skipping inputs.
- **📖 Integrated Help Tab:** Built-in interactive documentation directly inside the application for offline troubleshooting and quick-start tutorials.
- **🛡️ Secure & Local:** 100% open-source, client-side execution. It requires zero internet permissions and never uploads telemetry or input data.

---

## 💻 System Requirements & Prerequisites

To launch and execute AeroMacro smoothly, your system must meet the following baseline requirements:

### 1. Operating System
- **Windows 10 / 11** (Fully supported with built-in High DPI awareness to ensure crisp, non-blurry text scaling on 2K/4K monitors).
- **macOS / Linux** (Functional, but universal hotkey listeners may require elevated administrative privileges or terminal permissions depending on desktop security environments).

### 2. Python Environment
- **Python 3.9 or newer** must be installed on your local computer.
- During the Python installation setup, **ensure you check the box that says "Add Python to PATH"** so you can invoke the execution engine directly from your terminal or command prompt.

---

## 🛠️ Installation & Setup Steps

### Step 1: Clone or Download the Project
Clone this repository to your local machine:
```bash
git clone [https://github.com/Pepa12341/macro.git](https://github.com/Pepa12341/macro.git)
cd macro

```

*(Alternatively, if you do not use Git, you can simply download the source file `AeroMacro v6.0.py` directly into a local folder of your choice).*

### Step 2: Install Peripheral Dependencies

AeroMacro relies on the standard `tkinter` library (which comes bundled automatically with official Python distributions) and the external `pynput` package to handle low-overhead cross-platform input capturing and automation.

Open your Terminal (macOS/Linux) or Command Prompt/PowerShell (Windows) and run:

```bash
pip install pynput

```

---

## 🚀 How to Launch and Use

### 1. Booting the Application

Execute the main script via your terminal:

```bash
python "AeroMacro v6.0.py"

```

*(Note: Keep the quotation marks around the filename in your terminal so the command line reads the space in the filename correctly!)*

### 2. Standard Workflow

1. **Configure Hotkeys:** Click on either the **Record / Stop** or **Playback / Stop** buttons within the *Global Hotkeys* container. The status will change to `PRESS ANY KEY...`. Tap any physical button on your keyboard to lock it as your new shortcut.
2. **Recording Sequences:** Tap your designated Record hotkey (Default: `F9`) or click **Start Recording**. Move your mouse, click, and type as needed. Tap the record hotkey again to stop tracking and safely compile the action sequence data.
3. **Set Loops & Speed:**
* **Repeat count:** Define your cycle repetition constraint. Set it to `1` for single execution, or `0` for an endless automated loop.
* **Speed Multiplier:** Set your preferred execution pace. `2.0x` fires inputs twice as fast; `0.5x` slows things down to half speed.


4. **Run & Emergency Halt:** Tap your Playback hotkey (Default: `F10`) or click **Run Macro**. To instantly abort execution mid-macro or safely stop an infinite loop, simply press the playback shortcut again to immediately kill the automation thread.

---

## 📄 License

This project is licensed under the open-source **MIT License** - meaning you are completely free to modify, distribute, share with friends, or utilize it in your own personal or commercial projects.

---

*Developed with focus on local precision control, automation efficiency, and safe code integrity.*

```

```
