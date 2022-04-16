from __future__ import annotations

import argparse

import pygame as pg
# Place a picture called "sheet.png" in the same folder as this program!
# Zoom with mousewheel, pan with left mouse button
# Print a snapshot of the screen with "P"
parser = argparse.ArgumentParser(description='View image RGBA')
parser.add_argument('-p', '--path', required=True, type=str)

args = parser.parse_args()

sprite_sheet = pg.image.load(args.path)
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pg.time.Clock()
zoom_event = False
scale_up = 1.2
scale_down = 0.8


class GameState:
    def __init__(self) -> None:
        self.tab = 1
        self.zoom = 1.0
        self.world_offset_x = 0.0
        self.world_offset_y = 0.0
        self.update_screen = True
        self.panning = False
        self.pan_start_pos = (None, None)
        self.legacy_screen = pg.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))


game_state = GameState()


def screen_2_world(screen_x: int, screen_y: int) -> list[float]:
    world_x = (screen_x / game_state.zoom) + game_state.world_offset_x
    world_y = (screen_y / game_state.zoom) + game_state.world_offset_y
    return [world_x, world_y]


# game loop
try:
    while 1:
        # Banner FPS
        # pg.display.set_caption('(%d FPS)' % (clock.get_fps()))
        # Mouse screen coords
        mouse_x, mouse_y = pg.mouse.get_pos()

        # event handler
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if game_state.tab == 1:
                        game_state.tab = 2
                    elif game_state.tab == 2:
                        game_state.tab = 1
                elif event.key == pg.K_p:
                    pg.image.save(screen, 'NEW.png')

            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 4 or event.button == 5:
                    # X and Y before the zoom
                    mouseworld_x_before, mouseworld_y_before = screen_2_world(mouse_x, mouse_y)

                    # ZOOM IN/OUT
                    if event.button == 4 and game_state.zoom < 50.0:
                        game_state.zoom *= scale_up
                    elif event.button == 5 and game_state.zoom > 0.5:
                        game_state.zoom *= scale_down

                    # X and Y after the zoom
                    mouseworld_x_after, mouseworld_y_after = screen_2_world(mouse_x, mouse_y)

                    # Do the difference between before and after, and add it to the offset
                    game_state.world_offset_x += mouseworld_x_before - mouseworld_x_after
                    game_state.world_offset_y += mouseworld_y_before - mouseworld_y_after

                elif event.button == 1:
                    # PAN START
                    game_state.panning = True
                    game_state.pan_start_pos = mouse_x, mouse_y

            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1 and game_state.panning:
                    # PAN STOP
                    game_state.panning = False

        if game_state.panning:
            # Pans the screen if the left mouse button is held
            game_state.world_offset_x -= (mouse_x - game_state.pan_start_pos[0]) / game_state.zoom
            game_state.world_offset_y -= (mouse_y - game_state.pan_start_pos[1]) / game_state.zoom
            game_state.pan_start_pos = mouse_x, mouse_y

        # Draw the screen
        if game_state.tab == 1:
            if game_state.update_screen:
                # Updates the legacy screen if something has changed in the image data
                game_state.legacy_screen.blit(sprite_sheet, (0, 0))
                game_state.update_screen = False

            # Sets variables for the section of the legacy screen to be zoomed
            world_left, world_top = screen_2_world(0, 0)
            world_right, world_bottom = SCREEN_WIDTH / game_state.zoom, SCREEN_HEIGHT / game_state.zoom

            # Makes a temp surface with the dimensions of a smaller section of the legacy screen (for zooming).
            new_screen = pg.Surface((world_right, world_bottom))
            # Blits the smaller section of the legacy screen to the temp screen
            new_screen.blit(game_state.legacy_screen, (0, 0), (world_left, world_top, world_right + 1, world_bottom + 1))
            # Blits the final cut-out to the main screen, and scales the image to fit with the screen height and width
            screen.fill((255, 255, 255))
            screen.blit(
                pg.transform.scale(
                    new_screen, (
                        int(SCREEN_WIDTH + game_state.zoom),
                        int(SCREEN_HEIGHT + game_state.zoom),
                    ),
                ),
                (-(world_left % 1) * game_state.zoom, -(world_top % 1) * game_state.zoom),
            )
            try:
                mouse_x, mouse_y = pg.mouse.get_pos()
                pg.display.set_caption(f'RGBA: {screen.get_at((mouse_x,mouse_y))}')

            except Exception:
                print('[WARN] Mouse not detected.')

        # looping
        pg.display.update()
        clock.tick(30)
except pg.error:
    print('Goodbye!')
except Exception as e:
    print(e)
