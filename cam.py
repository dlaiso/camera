import os
import pygame
from picamera2 import Picamera2
from datetime import datetime

# Initialize Pygame and the camera
pygame.init()
picam2 = Picamera2()

# Set up display
screen = pygame.display.set_mode((480, 320))  # Adjust to your screen resolution
pygame.display.set_caption("Camera Application")

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Directories for saving images
IMAGE_DIR = "images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

# Application states
CAPTURE_MODE = "capture"
GALLERY_MODE = "gallery"
mode = CAPTURE_MODE

# Status indicator
status_color = GREEN

# Gallery variables
images = sorted(os.listdir(IMAGE_DIR))
current_image_index = len(images) - 1

def capture_image():
    global images, current_image_index
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(IMAGE_DIR, f"{timestamp}.jpg")
    picam2.capture_file(image_path)
    images = sorted(os.listdir(IMAGE_DIR))
    current_image_index = len(images) - 1
    return image_path

def display_image(image_path):
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (480, 320))  # Adjust to your screen resolution
    screen.blit(image, (0, 0))
    pygame.display.update()

def update_status(color):
    pygame.draw.rect(screen, color, (0, 0, 50, 50))
    pygame.display.update()

def main():
    global mode, status_color, current_image_index

    running = True
    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if mode == CAPTURE_MODE:
                    if x < 240:  # Left side of the screen
                        # Capture image
                        update_status(RED)
                        pygame.display.update()
                        capture_image()
                        update_status(GREEN)
                    elif x > 430 and y > 270:  # Bottom right corner
                        # Switch to gallery mode
                        mode = GALLERY_MODE
                elif mode == GALLERY_MODE:
                    if x < 240:  # Left half
                        # Previous image
                        if current_image_index > 0:
                            current_image_index -= 1
                    else:  # Right half
                        # Next image
                        if current_image_index < len(images) - 1:
                            current_image_index += 1
                    if x > 430 and y > 270:  # Bottom right corner
                        # Return to capture mode
                        mode = CAPTURE_MODE

        if mode == CAPTURE_MODE:
            # Draw capture UI
            pygame.draw.rect(screen, status_color, (0, 0, 50, 50))  # Status indicator
            pygame.draw.rect(screen, BLACK, (430, 270, 50, 50))  # Gallery button
            pygame.display.update()
        elif mode == GALLERY_MODE and images:
            # Display current image
            image_path = os.path.join(IMAGE_DIR, images[current_image_index])
            display_image(image_path)

    pygame.quit()

if __name__ == "__main__":
    main()
