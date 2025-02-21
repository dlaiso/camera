import os
import pygame
from picamera2 import Picamera2
from datetime import datetime

# Initialize Pygame and the camera
pygame.init()
picam2 = Picamera2()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 480, 320  # Adjust to your screen resolution
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
current_image_index = max(len(images) - 1, 0)  # Ensure a valid index

def capture_image():
    """ Captures an image, updates the image list, and sets status indicator. """
    global images, current_image_index, status_color

    # Update status to indicate capturing
    status_color = RED
    draw_capture_ui()
    pygame.display.update()

    # Generate timestamped filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    image_path = os.path.join(IMAGE_DIR, f"{timestamp}.jpg")

    # Capture the image
    picam2.capture_file(image_path)

    # Refresh image list and set index to latest image
    images = sorted(os.listdir(IMAGE_DIR))
    current_image_index = max(len(images) - 1, 0)  # Ensure index is valid

    # Update status to indicate ready
    status_color = GREEN
    draw_capture_ui()
    pygame.display.update()

def draw_capture_ui():
    """ Draws the UI for capture mode. """
    screen.fill(WHITE)
    pygame.draw.rect(screen, status_color, (0, 0, 50, 50))  # Status indicator
    pygame.draw.rect(screen, BLACK, (SCREEN_WIDTH - 50, SCREEN_HEIGHT - 50, 50, 50))  # Gallery button
    pygame.display.update()

def display_image(image_path):
    """ Displays an image on the screen. """
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(image, (0, 0))
    pygame.display.update()

def main():
    """ Main event loop handling touch input and mode switching. """
    global mode, current_image_index

    running = True
    while running:
        if mode == CAPTURE_MODE:
            draw_capture_ui()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()

                if mode == CAPTURE_MODE:
                    if x < SCREEN_WIDTH / 2:  # Left side of screen -> Capture Image
                        capture_image()
                    elif x > SCREEN_WIDTH - 50 and y > SCREEN_HEIGHT - 50:  # Bottom-right -> Enter Gallery Mode
                        if images:  # Ensure at least one image exists
                            mode = GALLERY_MODE
                            display_image(os.path.join(IMAGE_DIR, images[current_image_index]))

                elif mode == GALLERY_MODE:
                    if x < SCREEN_WIDTH / 2:  # Left half -> Previous image
                        if current_image_index > 0:
                            current_image_index -= 1
                    else:  # Right half -> Next image
                        if current_image_index < len(images) - 1:
                            current_image_index += 1

                    if x > SCREEN_WIDTH - 50 and y > SCREEN_HEIGHT - 50:  # Bottom-right -> Return to Capture Mode
                        mode = CAPTURE_MODE
                    else:
                        display_image(os.path.join(IMAGE_DIR, images[current_image_index]))

    pygame.quit()

if __name__ == "__main__":
    main()
