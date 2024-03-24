# Example file showing a basic pygame "game loop"
import pygame

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()
running = True
origsurf = pygame.Surface((16, 16), 0, 24)
origsurf.fill("black")
scalsurf = pygame.Surface((512, 512), 0, 24)
pixels = pygame.surfarray.pixels3d(origsurf)
pixels[0, 0] = (255, 255, 255)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("purple")

    # RENDER YOUR GAME HERE
    pygame.transform.scale(origsurf, scalsurf.get_size(), scalsurf)
    screen.blit(scalsurf, (0, 0))

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(24)  # limits FPS to 60

pygame.quit()
