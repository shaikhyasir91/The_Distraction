import pygame
from pygame.locals import *
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100,-16,2,512)
mixer.init()
pygame.init()

clock=pygame.time.Clock()
fps=60


screen_width=1000
screen_height=800

screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('The Distraction')


font=pygame.font.SysFont('Bauhaus 93',70)
#define game variables
tile_size=50
game_over=0
main_menu=True
level=1
max_level=3


#define colors
blue=(0,0,255)

#load images
bg_img=pygame.image.load('Brick Wall.jpg')
restart_img=pygame.image.load('restart_btn.png')
start_img=pygame.image.load('start_btn.png')
exit_img=pygame.image.load('exit_btn.png')

#load sounds
pygame.mixer.music.load('music.wav')
pygame.mixer.music.play(-1,0.0,5000)
jump_fx=pygame.mixer.Sound('jump.wav')
jump_fx.set_volume(0.5)
game_over_fx=pygame.mixer.Sound('game_over.wav')
game_over_fx.set_volume(0.5)


def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))



#function to reset level
def reset_level(level):
    player.reset(100, screen_height - 130)
    insta_group.empty()
    platform_group.empty()
    football_group.empty()
    exit_group.empty()
    mobile_group.empty()

    # load in level data and create world
    if path.exists(f'level{level}_data'):
        pickle_in = open(f'level{level}_data', 'rb')
        world_data = pickle.load(pickle_in)
    world=World(world_data)

    return world



class Button():
    def __init__(self,x,y,image):
        self.image=image
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False

    def draw(self):
        action=False

        #get mouse position
        pos=pygame.mouse.get_pos()

        #check mouseover and clicked condition
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                action=True
                self.clicked=True

        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False



        #draw button
        screen.blit(self.image,self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)
        # Load GIF frames
        self.gif_frames = [pygame.image.load(f'football_guy{i}.png') for i in range(1, 6)]
        self.gif_index = 0
        self.show_gif = False
        self.gif_timer = 0
        self.gif_repeats = 0
        self.max_repeats = 5

    def update(self, game_over):
        if self.show_gif:
            self.gif_timer += 1
            if self.gif_timer % 10 == 0:  # Change frame every 10 ticks (adjust as needed for speed)
                self.gif_index += 1
                if self.gif_index >= len(self.gif_frames):
                    self.gif_index = 0
                    self.gif_repeats += 1
                    if self.gif_repeats >= self.max_repeats:
                        self.show_gif = False
                        self.gif_repeats = 0
                        game_over = -1  # Player is distracted, game over
            screen.blit(self.gif_frames[self.gif_index], (self.rect.x, self.rect.y))
            return game_over

        # Existing player update logic...
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            # Get keypresses
            key = pygame.key.get_pressed()
            if key[pygame.K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not key[pygame.K_SPACE]:
                self.jumped = False
            if key[pygame.K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if key[pygame.K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not key[pygame.K_LEFT] and not key[pygame.K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Handle animation
            if self.counter > walk_cooldown:
                self.counter = 0
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            # Add gravity
            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            # Check for collision
            self.in_air = True
            for tile in world.tile_list:
                # Check for collision in x direction
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Check for collision in y direction
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if below the ground i.e. jumping
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    # Check if above the ground i.e. falling
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            # Check for collision with enemies
            if pygame.sprite.spritecollide(self, insta_group, False):
                game_over = -1
                game_over_fx.play()
                # Add different logic for insta enemy if needed

            if pygame.sprite.spritecollide(self, mobile_group, False):
                game_over = -1
                game_over_fx.play()
                # Add different logic for mobile enemy if needed

            if pygame.sprite.spritecollide(self, football_group, False):
                game_over = -1
                game_over_fx.play()
                self.show_gif = True
                self.gif_index = 0
                self.gif_timer = 0
                self.gif_repeats = 0

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            # Check for collision with platforms
            for platform in platform_group:
                # Collision in the x direction
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                # Collision in the y direction
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    # Check if below platform
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    # Check if above platform
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    # Move sideways with the platform
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            # Update player coordinates
            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.distracted_image
            draw_text('DISTRACTED!', font, blue, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        # Draw player onto screen
        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f'guy{num}.png')
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.distracted_image = pygame.image.load('ghost.png')
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World():
    def __init__(self,data):
        self.tile_list=[]

        #load images
        dirt_img=pygame.image.load('dirt.png')
        grass_img=pygame.image.load('grass.png')

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile==1:
                    img=pygame.transform.scale(dirt_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x= col_count*tile_size
                    img_rect.y= row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==2:
                    img=pygame.transform.scale(grass_img,(tile_size,tile_size))
                    img_rect=img.get_rect()
                    img_rect.x= col_count*tile_size
                    img_rect.y= row_count*tile_size
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                if tile==3:
                    football = Football(col_count * tile_size, row_count * tile_size + 15)
                    football_group.add(football)
                if tile==4:
                    platform=Platform(col_count * tile_size, row_count * tile_size,1,0)
                    platform_group.add(platform)
                if tile==5:
                    platform=Platform(col_count * tile_size, row_count * tile_size,0,1)
                    platform_group.add(platform)
                if tile==6:
                    insta = Insta(col_count * tile_size, row_count * tile_size + 9)
                    insta_group.add(insta)
                if tile==7:
                    mobile = Mobile(col_count * tile_size, row_count * tile_size + 5)
                    mobile_group.add(mobile)
                if tile==8:
                    exit=Exit(col_count*tile_size,row_count*tile_size-(tile_size//2))
                    exit_group.add(exit)

                col_count+=1
            row_count+=1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])


class Insta(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('instagram enemy.png')
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_direction=1
        self.move_counter=0

    def update(self):
        self.rect.x+=self.move_direction
        self.move_counter+=1
        if abs(self.move_counter)>50:
            self.move_direction*=-1
            self.move_counter*=-1




class Platform(pygame.sprite.Sprite):
    def __init__(self,x,y,move_x,move_y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('platform.png')
        self.image=pygame.transform.scale(img,(tile_size,tile_size//2))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_counter=0
        self.move_direction=1
        self.move_x=move_x
        self.move_y=move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y

        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1




class Football(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('football1.png')
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1

class Mobile(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.image.load('Mobile_enemy.png')
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.move_direction=1
        self.move_counter=0

    def update(self):
        self.rect.x+=self.move_direction
        self.move_counter+=1
        if abs(self.move_counter)>50:
            self.move_direction*=-1
            self.move_counter*=-1


class Exit(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img=pygame.image.load('exit.png')
        self.image=pygame.transform.scale(img,(tile_size,int(tile_size*1.5)))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y


player=Player(100,screen_height-130)

insta_group=pygame.sprite.Group()
platform_group=pygame.sprite.Group()
football_group=pygame.sprite.Group()
mobile_group=pygame.sprite.Group()
exit_group=pygame.sprite.Group()



#load in level data and create world
if path.exists(f'level{level}_data'):
    pickle_in=open(f'level{level}_data','rb')
    world_data=pickle.load(pickle_in)


world=World(world_data)

#create buttons
restart_button=Button(screen_width//2-50,screen_height//2+100,restart_img)
start_button=Button(screen_width//2-350,screen_height//2,start_img)
exit_button=Button(screen_width//2+100,screen_height//2,exit_img)


run = True
while run:
    clock.tick(fps)
    screen.blit(bg_img, (0, 0))

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            insta_group.update()
            platform_group.update()

        if game_over == 0:
            football_group.update()
            mobile_group.update()

        insta_group.draw(screen)
        football_group.draw(screen)
        mobile_group.draw(screen)
        exit_group.draw(screen)
        platform_group.draw(screen)

        game_over = player.update(game_over)

        # If player has died
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0

        # If player has completed a level
        if game_over == 1:
            level += 1
            if level <= max_level:
                # Reset level
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    world_data = []
                    world = reset_level(level)
                    game_over = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()
