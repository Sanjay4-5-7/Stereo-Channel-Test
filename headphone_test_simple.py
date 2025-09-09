#!/usr/bin/env python3
"""
Simple Headphone Test - Minimal CLI Version
Ultra-lightweight headphone tester
"""

import numpy as np
import sounddevice as sd
import time

def play_tone(freq=440, duration=2, channel='both'):
    """Play tone to specified channel(s)"""
    t = np.linspace(0, duration, int(44100 * duration), False)
    tone = 0.3 * np.sin(2 * np.pi * freq * t)
    
    # Quick fade
    fade = int(0.05 * 44100)
    tone[:fade] *= np.linspace(0, 1, fade)
    tone[-fade:] *= np.linspace(1, 0, fade)
    
    if channel == 'left':
        stereo = np.column_stack([tone, np.zeros_like(tone)])
    elif channel == 'right':
        stereo = np.column_stack([np.zeros_like(tone), tone])
    else:  # both
        stereo = np.column_stack([tone, tone])
    
    sd.play(stereo, 44100)
    sd.wait()

def quick_test(freq=440, dur=1.5):
    """Run quick alternating test"""
    print(f"🎧 Quick Test - {freq}Hz, {dur}s per channel")
    
    tests = [('Both', 'both'), ('Left', 'left'), ('Right', 'right')]
    
    for name, channel in tests:
        print(f"  → {name}...")
        play_tone(freq, dur, channel)
        time.sleep(0.3)
    
    print("✓ Done!")

def main():
    print("🎧 Simple Headphone Tester")
    print("Commands: test [freq] [duration] | left | right | both | alt | quit")
    
    while True:
        try:
            cmd = input("\n> ").strip().lower().split()
            if not cmd:
                continue
                
            if cmd[0] in ['q', 'quit', 'exit']:
                break
            elif cmd[0] == 'test':
                freq = int(cmd[1]) if len(cmd) > 1 else 440
                dur = float(cmd[2]) if len(cmd) > 2 else 1.5
                quick_test(freq, dur)
            elif cmd[0] == 'left':
                print("Left channel...")
                play_tone(440, 2, 'left')
            elif cmd[0] == 'right':
                print("Right channel...")
                play_tone(440, 2, 'right')
            elif cmd[0] == 'both':
                print("Both channels...")
                play_tone(440, 2, 'both')
            elif cmd[0] in ['alt', 'alternate']:
                print("Alternating...")
                for _ in range(3):
                    play_tone(440, 0.8, 'left')
                    time.sleep(0.1)
                    play_tone(440, 0.8, 'right')
                    time.sleep(0.1)
            else:
                print("Commands: test [freq] [dur] | left | right | both | alt | quit")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
    
    print("Goodbye! 👋")

if __name__ == "__main__":
    main()
