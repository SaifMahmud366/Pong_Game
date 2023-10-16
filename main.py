import pygame
import os
import random
import sys

pygame.init()

screen_width = 1280
screen_height = 720

icon = pygame.image.load(os.path.join('Assets', 'icon.png'))
ball_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
bar_hit_sound = pygame.mixer.Sound(os.path.join('Assets', 'bar_hit.mp3'))
font_path = os.path.join('Assets', 'VCR_OSD_MONO.ttf')

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Pong Game')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()

fps = 60
velocity = 5
object_width = 5
object_height = 60
line_width = screen_width
line_height = 5

line_start = (screen_width // 2, 0)
line_end = (screen_width // 2, screen_height)

#BLUE object
blue_x = 10
blue_y = (screen_height // 2) - (object_height // 2)

#RED object
red_x = screen_width - 15
red_y = (screen_height // 2) - (object_height // 2)

#Ball
ball_x = screen_width // 2
ball_y = screen_height // 2
ball_velocity_x = 4
ball_velocity_y = 4

# Score
blue_score = 0
red_score = 0
win_score = 5

def home_screen():
    title_font = pygame.font.Font(font_path, 48)
    font = pygame.font.Font(font_path, 32)
    title_text = title_font.render("PONG GAME", True, pygame.Color('white'))
    play_text = font.render("Play", True, pygame.Color('white'))
    play_rect = play_text.get_rect(center=(screen_width // 2, screen_height // 2))

    # Load and play the background music
    pygame.mixer.music.load(os.path.join('Assets', 'A Lonely Cherry Tree.mp3'))  # Adjust the music file path
    pygame.mixer.music.play(-1)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(pygame.mouse.get_pos()):
                    pygame.mixer.music.stop()
                    return  # Return to start the game

        screen.fill('black')  # Clear the screen

        # Blit title_text and play_text onto the screen
        screen.blit(title_text, (screen_width // 2 - title_text.get_width() // 2, 100))
        screen.blit(play_text, play_rect)

        pygame.display.flip()  # Update the display
        clock.tick(fps)

def ball_movement():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y, blue_score, red_score

    ball_x += ball_velocity_x
    ball_y += ball_velocity_y

    # Check if the ball hits the top or bottom boundary
    if ball_y <= 0 or ball_y >= screen_height:
        ball_velocity_y *= -1
        bar_hit_sound.play()

    # Check collision with the blue paddle
    if blue_x <= ball_x <= blue_x + object_width and blue_y <= ball_y <= blue_y + object_height:
        ball_x = blue_x + object_width  # Move the ball to the right edge of the blue paddle
        ball_velocity_x *= -1
        ball_hit_sound.play()

    # Check collision with the red paddle
    if red_x <= ball_x <= red_x + object_width and red_y <= ball_y <= red_y + object_height:
        ball_x = red_x - 8  # Move the ball to the left edge of the red paddle (subtract 8 to avoid overlap)
        ball_velocity_x *= -1
        ball_hit_sound.play()

    # Check if the ball goes beyond the paddles and update scores
    if ball_x <= 0:
        red_score += 1
        reset_ball()
    elif ball_x >= screen_width:
        blue_score += 1
        reset_ball()

def reset_ball():
    global ball_x, ball_y, ball_velocity_x, ball_velocity_y
    ball_x = screen_width // 2
    ball_y = screen_height // 2
    ball_velocity_x = random.choice([-1, 1]) * random.randint(3, 5)
    ball_velocity_y = random.choice([-1, 1]) * random.randint(3, 5)

def main():
    global blue_y, red_y, ball_velocity_x, ball_velocity_y, blue_score, red_score
    home_screen()

    ball_velocity_x = random.choice([-1, 1]) * random.randint(3, 5)
    ball_velocity_y = random.choice([-1, 1]) * random.randint(3, 5)
    
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False

        key_pressd = pygame.key.get_pressed()
        if key_pressd[pygame.K_w] and blue_y > 0:
            blue_y -= velocity
        if key_pressd[pygame.K_s] and  blue_y < (screen_height - object_height):
            blue_y += velocity
        if key_pressd[pygame.K_UP] and red_y > 0:
            red_y -= velocity
        if key_pressd[pygame.K_DOWN] and red_y < (screen_height - object_height):
            red_y += velocity

        screen.fill('black')  # Clear the screen

        ball_movement()

        # Draw scores on the screen
        font = pygame.font.Font(None, 36)
        blue_score_text = font.render(f"Blue: {blue_score}", True, pygame.Color('white'))
        red_score_text = font.render(f"Red: {red_score}", True, pygame.Color('white'))
        screen.blit(blue_score_text, (10, 10))
        screen.blit(red_score_text, (screen_width - red_score_text.get_width() - 10, 10))

        pygame.draw.line(screen, 'white', line_start, line_end, 2)
        pygame.draw.circle(screen, 'lime', (ball_x, ball_y), 8)
        pygame.draw.rect(screen, '#54E2E6', pygame.Rect(blue_x, blue_y, object_width, object_height))
        pygame.draw.rect(screen, '#FA4343', pygame.Rect(red_x, red_y, object_width, object_height))
        pygame.draw.rect(screen, '#A3A3A3', pygame.Rect(0, 0, line_width, line_height))
        pygame.draw.rect(screen, '#A3A3A3', pygame.Rect(0, (screen_height - 5) , line_width, line_height))
        
        pygame.display.flip()
        clock.tick(fps)

        # Check for win condition
        if blue_score >= win_score or red_score >= win_score:
            run = False

    # Determine the winner and display the result
    winner = "Blue" if blue_score >= win_score else "Red"
    winner_font = pygame.font.Font(font_path, 60)
    winner_text = winner_font.render(f"{winner} Wins!", True, pygame.Color('white'))
    winner_rect = winner_text.get_rect(center=(screen_width // 2, screen_height // 2))

    screen.fill('black')
    screen.blit(winner_text, winner_rect)
    pygame.display.flip()

    pygame.time.wait(3000)  # Display the winner for 3 seconds

    pygame.quit()

if __name__ == '__main__':
    main()
