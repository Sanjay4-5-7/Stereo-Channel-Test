#!/usr/bin/env python3
"""
Headphone Left/Right Channel Test Script
This script generates audio tones and plays them to specific channels
to test if your headphones are working correctly.
"""

import numpy as np
import sounddevice as sd
import time
import sys

class HeadphoneTest:
    def __init__(self, sample_rate=44100, duration=3):
        self.sample_rate = sample_rate
        self.duration = duration
        
    def generate_tone(self, frequency=440):
        """Generate a sine wave tone"""
        t = np.linspace(0, self.duration, int(self.sample_rate * self.duration), False)
        # Generate sine wave with fade in/out to avoid clicks
        tone = np.sin(2 * np.pi * frequency * t)
        
        # Apply fade in/out
        fade_samples = int(0.1 * self.sample_rate)  # 0.1 second fade
        tone[:fade_samples] *= np.linspace(0, 1, fade_samples)
        tone[-fade_samples:] *= np.linspace(1, 0, fade_samples)
        
        return tone
    
    def play_left_channel(self, frequency=440):
        """Play tone only in left channel"""
        print(f"🎵 Playing {frequency}Hz tone in LEFT channel...")
        tone = self.generate_tone(frequency)
        stereo_tone = np.column_stack([tone, np.zeros_like(tone)])  # Left channel only
        sd.play(stereo_tone, self.sample_rate)
        sd.wait()
        
    def play_right_channel(self, frequency=440):
        """Play tone only in right channel"""
        print(f"🎵 Playing {frequency}Hz tone in RIGHT channel...")
        tone = self.generate_tone(frequency)
        stereo_tone = np.column_stack([np.zeros_like(tone), tone])  # Right channel only
        sd.play(stereo_tone, self.sample_rate)
        sd.wait()
        
    def play_both_channels(self, frequency=440):
        """Play tone in both channels"""
        print(f"🎵 Playing {frequency}Hz tone in BOTH channels...")
        tone = self.generate_tone(frequency)
        stereo_tone = np.column_stack([tone, tone])  # Both channels
        sd.play(stereo_tone, self.sample_rate)
        sd.wait()
        
    def play_alternating(self, frequency=440, cycles=3):
        """Alternate between left and right channels"""
        print(f"🔄 Alternating between LEFT and RIGHT channels ({cycles} cycles)...")
        tone = self.generate_tone(1)  # 1 second duration for alternating
        
        for i in range(cycles):
            print(f"  Cycle {i+1}/{cycles}")
            # Left
            print("    → LEFT")
            stereo_tone = np.column_stack([tone, np.zeros_like(tone)])
            sd.play(stereo_tone, self.sample_rate)
            sd.wait()
            
            time.sleep(0.2)  # Brief pause
            
            # Right  
            print("    → RIGHT")
            stereo_tone = np.column_stack([np.zeros_like(tone), tone])
            sd.play(stereo_tone, self.sample_rate)
            sd.wait()
            
            time.sleep(0.2)  # Brief pause
    
    def run_full_test(self):
        """Run complete headphone test sequence"""
        print("🎧 HEADPHONE TEST STARTING")
        print("=" * 40)
        print("Make sure your headphones are connected and volume is at a comfortable level.")
        input("Press Enter to start the test...")
        print()
        
        try:
            # Test both channels first
            self.play_both_channels(440)
            time.sleep(1)
            
            # Test left channel
            self.play_left_channel(440)
            time.sleep(1)
            
            # Test right channel  
            self.play_right_channel(440)
            time.sleep(1)
            
            # Test alternating
            self.play_alternating(440, 3)
            time.sleep(1)
            
            # Test with different frequencies
            print("\n🎼 Testing different frequencies...")
            frequencies = [220, 440, 880]  # Low, mid, high
            
            for freq in frequencies:
                print(f"\nTesting {freq}Hz:")
                self.play_left_channel(freq)
                time.sleep(0.5)
                self.play_right_channel(freq)
                time.sleep(0.5)
                
            print("\n✅ Headphone test completed!")
            print("\nDid you hear:")
            print("- Sound in BOTH ears during the stereo test?")
            print("- Sound only in your LEFT ear during left channel test?") 
            print("- Sound only in your RIGHT ear during right channel test?")
            print("- Alternating sound between left and right?")
            print("\nIf yes to all, your headphones are working correctly! 🎉")
            
        except Exception as e:
            print(f"❌ Error during test: {e}")
            print("Make sure you have audio output devices available.")

def main():
    print("🎧 Headphone Left/Right Channel Tester")
    print("=" * 40)
    
    # Check if sounddevice is available
    try:
        import sounddevice as sd
        import numpy as np
    except ImportError:
        print("❌ Required libraries not found!")
        print("Please install them with:")
        print("pip install sounddevice numpy")
        sys.exit(1)
    
    # Show available audio devices
    print("Available audio devices:")
    print(sd.query_devices())
    print()
    
    tester = HeadphoneTest()
    
    while True:
        print("\nChoose a test:")
        print("1. Full headphone test")
        print("2. Left channel only")
        print("3. Right channel only") 
        print("4. Both channels")
        print("5. Alternating channels")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        try:
            if choice == '1':
                tester.run_full_test()
            elif choice == '2':
                tester.play_left_channel()
            elif choice == '3':
                tester.play_right_channel()
            elif choice == '4':
                tester.play_both_channels()
            elif choice == '5':
                tester.play_alternating()
            elif choice == '6':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Invalid choice. Please enter 1-6.")
        except KeyboardInterrupt:
            print("\n\n⏹️ Test interrupted by user.")
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
