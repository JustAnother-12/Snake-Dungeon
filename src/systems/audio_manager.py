import pygame
import os

class AudioManager:
    def __init__(self):
        self.sounds = {}  # Dictionary to store sound effects
        self.music = {}   # Dictionary to store music tracks
        self.current_music = None
        self.sound_volume = 1.0  # Default full volume
        self.music_volume = 0.5  # Default half volume
        self.sound_channels = {}  # To track which sound is playing on which channel
        self.channel_count = 16   # Default number of channels for Pygame
        
    def initialize(self):
        """Initialize the audio system"""
        pygame.mixer.init()
        pygame.mixer.set_num_channels(self.channel_count)
        
    def set_channels(self, count):
        """Set the number of sound channels available for simultaneous playback"""
        self.channel_count = count
        pygame.mixer.set_num_channels(count)
        
    def load_sound(self, name, file_path):
        """Load a sound effect from file"""
        try:
            sound = pygame.mixer.Sound(file_path)
            sound.set_volume(self.sound_volume)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Error loading sound {file_path}: {e}")
    
    def load_sound_with_volume(self, name, file_path, volume_override=None):
        """Load a sound effect with an optional specific volume level"""
        try:
            sound = pygame.mixer.Sound(file_path)
            # Use provided volume or default sound volume
            sound.set_volume(volume_override if volume_override is not None else self.sound_volume)
            self.sounds[name] = sound
        except pygame.error as e:
            print(f"Error loading sound {file_path}: {e}")
    
    def load_music(self, name, file_path):
        """Load a music track from file"""
        if os.path.exists(file_path):
            self.music[name] = file_path
        else:
            print(f"Music file not found: {file_path}")
    
    def play_sound(self, name, loops=0, maxtime=0, fade_ms=0):
        """
        Play a sound effect, potentially simultaneously with other sounds
        Returns the channel object if successful, None otherwise
        """
        if name in self.sounds:
            # Get the next available channel
            channel = pygame.mixer.find_channel()
            if channel is None:
                # All channels busy, try to force allocation
                channel = pygame.mixer.Channel(0)  # Use the oldest channel
            
            # Play the sound and track it
            channel.play(self.sounds[name], loops, maxtime, fade_ms)
            self.sound_channels[name] = channel
            return channel
        else:
            print(f"Sound {name} not found")
            return None
    
    def stop_sound(self, name, fade_ms=0):
        """Stop a specific sound effect"""
        if name in self.sound_channels and self.sound_channels[name].get_busy():
            if fade_ms > 0:
                self.sound_channels[name].fadeout(fade_ms)
            else:
                self.sound_channels[name].stop()
            return True
        return False
    
    def is_sound_playing(self, name):
        """Check if a specific sound is currently playing"""
        if name in self.sound_channels:
            return self.sound_channels[name].get_busy()
        return False
    
    def stop_all_sounds(self):
        """Stop all currently playing sound effects"""
        pygame.mixer.stop()  # Stops all channels
        self.sound_channels.clear()
        
    def get_busy_channel_count(self):
        """Returns the number of channels currently playing sounds"""
        count = 0
        for i in range(pygame.mixer.get_num_channels()):
            if pygame.mixer.Channel(i).get_busy():
                count += 1
        return count
    
    def play_music(self, name, loops=-1):
        """Play a music track, looping by default"""
        if name in self.music:
            try:
                pygame.mixer.music.load(self.music[name])
                pygame.mixer.music.set_volume(self.music_volume)
                pygame.mixer.music.play(loops)
                self.current_music = name
            except pygame.error as e:
                print(f"Error playing music {name}: {e}")
        else:
            print(f"Music {name} not found")
    
    def stop_music(self, fade_ms=0):
        """Stop current music playback"""
        if fade_ms > 0:
            pygame.mixer.music.fadeout(fade_ms)
        else:
            pygame.mixer.music.stop()
        self.current_music = None
    
    def pause_music(self):
        """Pause current music playback"""
        pygame.mixer.music.pause()
    
    def unpause_music(self):
        """Unpause current music playback"""
        pygame.mixer.music.unpause()
    
    def set_sound_volume(self, volume):
        """Set volume for sound effects (0.0 to 1.0)"""
        self.sound_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sound_volume)
    
    def set_music_volume(self, volume):
        """Set volume for music (0.0 to 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        pygame.mixer.music.set_volume(self.music_volume)
    
    def load_all_sounds(self, directory):
        """Load all sound files from a directory"""
        for filename in os.listdir(directory):
            if filename.endswith(('.wav', '.ogg', '.mp3')):
                name = os.path.splitext(filename)[0]
                self.load_sound(name, os.path.join(directory, filename))
    
    def load_all_music(self, directory):
        """Load all music files from a directory"""
        for filename in os.listdir(directory):
            if filename.endswith(('.wav', '.ogg', '.mp3')):
                name = os.path.splitext(filename)[0]
                self.load_music(name, os.path.join(directory, filename))
