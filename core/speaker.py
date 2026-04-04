import os
import asyncio
import edge_tts
import pygame
import time

class JarvisSpeaker:
    def __init__(self):
            # "en-GB-RyanNeural" is the best voice for a JARVIS feel
                    self.voice = "en-GB-RyanNeural" 
                            self.output_file = "speech.mp3"

                                async def speak(self, text):
                                        """Converts text to speech and plays it."""
                                                print(f"JARVIS: {text}")
                                                        
                                                                try:
                                                                            # 1. Generate the audio file using Edge-TTS
                                                                                        communicate = edge_tts.Communicate(text, self.voice)
                                                                                                    await communicate.save(self.output_file)

                                                                                                                # 2. Initialize Pygame mixer to play the sound
                                                                                                                            pygame.mixer.init()
                                                                                                                                        pygame.mixer.music.load(self.output_file)
                                                                                                                                                    pygame.mixer.music.play()

                                                                                                                                                                # 3. Wait for the audio to finish playing
                                                                                                                                                                            while pygame.mixer.music.get_busy():
                                                                                                                                                                                            await asyncio.sleep(0.1)
                                                                                                                                                                                                        
                                                                                                                                                                                                                    # 4. Clean up
                                                                                                                                                                                                                                pygame.mixer.quit()
                                                                                                                                                                                                                                            
                                                                                                                                                                                                                                                        # Optional: Delete the file after speaking to save space
                                                                                                                                                                                                                                                                    if os.path.exists(self.output_file):
                                                                                                                                                                                                                                                                                    os.remove(self.output_file)

                                                                                                                                                                                                                                                                                            except Exception as e:
                                                                                                                                                                                                                                                                                                        print(f"Speaker Error: {e}")

                                                                                                                                                                                                                                                                                                        # --- Test Script ---
                                                                                                                                                                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                                                                                                                                            # This part only runs if you play this file directly
                                                                                                                                                                                                                                                                                                                speaker = JarvisSpeaker()
                                                                                                                                                                                                                                                                                                                    test_text = "Systems are recalibrating. Hello Lakshay, I am online and ready."
                                                                                                                                                                                                                                                                                                                        asyncio.run(speaker.speak(test_text))
                                                                                                                                                                                                                                                                                                                        