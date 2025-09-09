#!/usr/bin/env python3
"""
Simple Headphone Test - GUI Version
Lightweight headphone left/right channel tester with GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import sounddevice as sd
import threading
import time

class HeadphoneTestGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🎧 Headphone Tester")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Default settings
        self.frequency = tk.IntVar(value=440)
        self.duration = tk.DoubleVar(value=2.0)
        self.sample_rate = 44100
        self.is_playing = False
        
        self.setup_gui()
        self.update_devices()
        
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title = ttk.Label(main_frame, text="🎧 Headphone Channel Tester", 
                         font=('Arial', 16, 'bold'))
        title.grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Settings frame
        settings_frame = ttk.LabelFrame(main_frame, text="Settings", padding="10")
        settings_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Frequency
        ttk.Label(settings_frame, text="Frequency (Hz):").grid(row=0, column=0, sticky=tk.W, pady=5)
        freq_frame = ttk.Frame(settings_frame)
        freq_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        self.freq_scale = ttk.Scale(freq_frame, from_=100, to=2000, 
                                   variable=self.frequency, orient=tk.HORIZONTAL)
        self.freq_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.freq_label = ttk.Label(freq_frame, text="440 Hz")
        self.freq_label.grid(row=0, column=1, padx=(10, 0))
        freq_frame.columnconfigure(0, weight=1)
        
        # Duration
        ttk.Label(settings_frame, text="Duration (sec):").grid(row=1, column=0, sticky=tk.W, pady=5)
        dur_frame = ttk.Frame(settings_frame)
        dur_frame.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        self.dur_scale = ttk.Scale(dur_frame, from_=0.5, to=5.0, 
                                  variable=self.duration, orient=tk.HORIZONTAL)
        self.dur_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        self.dur_label = ttk.Label(dur_frame, text="2.0 s")
        self.dur_label.grid(row=0, column=1, padx=(10, 0))
        dur_frame.columnconfigure(0, weight=1)
        
        settings_frame.columnconfigure(1, weight=1)
        
        # Audio device selection
        device_frame = ttk.LabelFrame(main_frame, text="Audio Device", padding="10")
        device_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        self.device_var = tk.StringVar()
        self.device_combo = ttk.Combobox(device_frame, textvariable=self.device_var, 
                                        state="readonly", width=50)
        self.device_combo.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 10))
        
        refresh_btn = ttk.Button(device_frame, text="🔄", width=3, 
                               command=self.update_devices)
        refresh_btn.grid(row=0, column=1)
        device_frame.columnconfigure(0, weight=1)
        
        # Test buttons frame
        test_frame = ttk.LabelFrame(main_frame, text="Tests", padding="15")
        test_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 15))
        
        # Create test buttons
        buttons = [
            ("🔊 Both Channels", lambda: self.play_test('both'), 0, 0, 2),
            ("⬅️ Left Only", lambda: self.play_test('left'), 1, 0, 1),
            ("➡️ Right Only", lambda: self.play_test('right'), 1, 1, 1),
            ("🔄 Alternating", lambda: self.play_test('alternate'), 2, 0, 2),
            ("⏹️ Stop", self.stop_audio, 3, 0, 2)
        ]
        
        for text, command, row, col, span in buttons:
            btn = ttk.Button(test_frame, text=text, command=command, width=15)
            btn.grid(row=row, column=col, columnspan=span, padx=5, pady=5, sticky=(tk.W, tk.E))
        
        test_frame.columnconfigure(0, weight=1)
        test_frame.columnconfigure(1, weight=1)
        
        # Status
        self.status_var = tk.StringVar(value="Ready")
        status_label = ttk.Label(main_frame, textvariable=self.status_var, 
                               font=('Arial', 10, 'italic'))
        status_label.grid(row=4, column=0, columnspan=2, pady=(0, 10))
        
        # Quick presets
        presets_frame = ttk.LabelFrame(main_frame, text="Quick Presets", padding="10")
        presets_frame.grid(row=5, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        preset_buttons = [
            ("Low (220Hz)", lambda: self.set_preset(220, 2)),
            ("Mid (440Hz)", lambda: self.set_preset(440, 2)), 
            ("High (880Hz)", lambda: self.set_preset(880, 2))
        ]
        
        for i, (text, command) in enumerate(preset_buttons):
            btn = ttk.Button(presets_frame, text=text, command=command, width=12)
            btn.grid(row=0, column=i, padx=5, sticky=(tk.W, tk.E))
        
        for i in range(3):
            presets_frame.columnconfigure(i, weight=1)
        
        # Bind scale updates
        self.freq_scale.configure(command=self.update_freq_label)
        self.dur_scale.configure(command=self.update_dur_label)
        
        main_frame.columnconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
    
    def update_freq_label(self, value):
        self.freq_label.config(text=f"{int(float(value))} Hz")
    
    def update_dur_label(self, value):
        self.dur_label.config(text=f"{float(value):.1f} s")
    
    def set_preset(self, freq, dur):
        self.frequency.set(freq)
        self.duration.set(dur)
        self.update_freq_label(freq)
        self.update_dur_label(dur)
    
    def update_devices(self):
        try:
            devices = sd.query_devices()
            output_devices = [f"{i}: {d['name']}" for i, d in enumerate(devices) 
                            if d['max_output_channels'] > 0]
            self.device_combo['values'] = output_devices
            if output_devices:
                self.device_combo.current(0)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to get audio devices: {e}")
    
    def generate_tone(self, freq, duration):
        t = np.linspace(0, duration, int(self.sample_rate * duration), False)
        tone = 0.3 * np.sin(2 * np.pi * freq * t)  # Lower volume
        
        # Quick fade to prevent clicks
        fade = int(0.05 * self.sample_rate)
        tone[:fade] *= np.linspace(0, 1, fade)
        tone[-fade:] *= np.linspace(1, 0, fade)
        return tone
    
    def play_test(self, test_type):
        if self.is_playing:
            return
            
        def run_test():
            try:
                self.is_playing = True
                device_id = None
                if self.device_var.get():
                    device_id = int(self.device_var.get().split(':')[0])
                
                freq = self.frequency.get()
                dur = self.duration.get()
                
                if test_type == 'both':
                    self.status_var.set("Playing both channels...")
                    tone = self.generate_tone(freq, dur)
                    stereo = np.column_stack([tone, tone])
                    sd.play(stereo, self.sample_rate, device=device_id)
                    sd.wait()
                    
                elif test_type == 'left':
                    self.status_var.set("Playing left channel...")
                    tone = self.generate_tone(freq, dur)
                    stereo = np.column_stack([tone, np.zeros_like(tone)])
                    sd.play(stereo, self.sample_rate, device=device_id)
                    sd.wait()
                    
                elif test_type == 'right':
                    self.status_var.set("Playing right channel...")
                    tone = self.generate_tone(freq, dur)
                    stereo = np.column_stack([np.zeros_like(tone), tone])
                    sd.play(stereo, self.sample_rate, device=device_id)
                    sd.wait()
                    
                elif test_type == 'alternate':
                    self.status_var.set("Alternating channels...")
                    short_tone = self.generate_tone(freq, dur/2)
                    
                    for i in range(4):  # 4 alternations
                        if not self.is_playing:
                            break
                            
                        # Left
                        stereo = np.column_stack([short_tone, np.zeros_like(short_tone)])
                        sd.play(stereo, self.sample_rate, device=device_id)
                        sd.wait()
                        
                        if not self.is_playing:
                            break
                            
                        time.sleep(0.1)
                        
                        # Right
                        stereo = np.column_stack([np.zeros_like(short_tone), short_tone])
                        sd.play(stereo, self.sample_rate, device=device_id)
                        sd.wait()
                        
                        time.sleep(0.1)
                
                self.status_var.set("Test completed ✓")
                
            except Exception as e:
                self.status_var.set(f"Error: {str(e)}")
                messagebox.showerror("Audio Error", 
                    f"Failed to play audio: {e}\n\nTry selecting a different audio device.")
            finally:
                self.is_playing = False
                
        thread = threading.Thread(target=run_test)
        thread.daemon = True
        thread.start()
    
    def stop_audio(self):
        self.is_playing = False
        sd.stop()
        self.status_var.set("Stopped")
    
    def run(self):
        self.root.mainloop()

def main():
    try:
        app = HeadphoneTestGUI()
        app.run()
    except ImportError as e:
        print(f"Missing required library: {e}")
        print("Install with: pip install sounddevice numpy")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
