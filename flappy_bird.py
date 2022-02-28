import pygame
import sys
import random


def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, 900))
    screen.blit(floor_surface, (floor_x_pos + 576, 900))


def create_pipe():
    random_pipe_pos = random.choice(pipe_heights)
    bottom_pipe = pipe_surface.get_rect(midtop=(700, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))

    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    visible_pipes = [pipe for pipe in pipes if pipe.right > -50]

    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 1024:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)


def check_collision(pipes):
    global flag_score

    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            death_sound.play()
            flag_score = True
            return False

    if bird_rect.top <= -100 or bird_rect.bottom >= 900:
        flag_score = True
        return False

    return True


def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)

    return new_bird


def bird_animation():
    new_bird = bird_flaps[bird_ind]
    new_bird_rect = new_bird.get_rect(center=(100, bird_rect.centery))

    return new_bird, new_bird_rect


def score_display(game_state):
    if game_state == 'main_game_loop':
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(288, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'Best score: {int(best_score)}', True,
                                              (255, 255, 255))
        high_score_rect = high_score_surface.get_rect(center=(288, 850))
        screen.blit(high_score_surface, high_score_rect)


def update_score(score_arr, high_score):
    if score_arr > high_score:
        high_score = score_arr

    return high_score


def check_pipe_score():
    global score, flag_score

    if pipe_list:
        for pipe in pipe_list:
            if 95 < pipe.centerx < 105 and flag_score:
                score += 1
                score_sound.play()
                flag_score = False
            if pipe.centerx < 0:
                flag_score = True


pygame.init()
screen = pygame.display.set_mode((576, 1024))
clock = pygame.time.Clock()
game_font = pygame.font.Font('04B_19.ttf', 40)
pygame.display.set_caption('Flappy Bird')

gravity = 0.25
bird_movement = 0
running = True
game_running = True
score = 0
best_score = 0
flag_score = True
bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_surface = pygame.transform.scale2x(bg_surface)

floor_surface = pygame.image.load('assets/base.png').convert()
floor_surface = pygame.transform.scale2x(floor_surface)
floor_x_pos = 0

bird_downflap = pygame.transform.scale2x(
    pygame.image.load('assets/redbird-downflap.png').convert_alpha())
bird_midflap = pygame.transform.scale2x(
    pygame.image.load('assets/redbird-midflap.png').convert_alpha())
bird_upflap = pygame.transform.scale2x(
    pygame.image.load('assets/redbird-upflap.png').convert_alpha())
bird_flaps = [bird_downflap, bird_midflap, bird_upflap]
bird_ind = 0
bird_surface = bird_flaps[bird_ind]
bird_rect = bird_surface.get_rect(center=(100, 512))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

pipe_surface = pygame.image.load('assets/pipe-green.png')
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_list = []

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)
pipe_heights = [400, 600, 800]

game_over_surface = pygame.transform.scale2x(pygame.image.load('assets/message.png').convert_alpha())
game_over_rect = game_over_surface.get_rect(center=(288, 512))

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
death_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')

score_sound_count = 100
SCOREEVENT = pygame.USEREVENT + 2
pygame.time.set_timer(SCOREEVENT, 100)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_running:
                bird_movement = 0
                bird_movement -= 10
                flap_sound.play()
            if event.key == pygame.K_SPACE and (not game_running):
                game_running = True
                pipe_list.clear()
                bird_rect.center = (100, 512)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_ind < 2:
                bird_ind += 1
            else:
                bird_ind = 0
            bird_surface, bird_rect = bird_animation()

    screen.blit(bg_surface, (0, 0))

    if game_running:
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect)
        game_running = check_collision(pipe_list)

        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        check_pipe_score()
        score_display('main_game_loop')
    else:
        screen.blit(game_over_surface, game_over_rect)
        best_score = update_score(score, best_score)
        score_display('game_over')

    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -576:
        floor_x_pos = 0

    pygame.display.update()
    clock.tick(120)

pygame.quit()
