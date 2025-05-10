import pygame

pygame.init()

# Create a font object
font = pygame.font.SysFont("papyrus", 20)  # or use pygame.font.Font("path_to_font.ttf", size)

# The text you want to measure
text = "Press ENTER to restart"

# Get the size of the text
text_size = font.size(text)
width, height = text_size

print(f"Text size: {width}x{height}")
