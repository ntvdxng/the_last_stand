# import thu vien
import pygame
import math
import random
import os
from enemy import Enemy
import button

# khoi tao pygame
pygame.init()

# kich thuoc cua so
screen_width = 900
screen_height = 600

# tao cua so game
screen = pygame.display.set_mode((screen_width, screen_height)) # kich thuoc
pygame.display.set_caption('The Last Stand') # tieu de cua so

clock = pygame.time.Clock()
fps = 60

# define game variables
level = 1
high_score = 0 # diem cao nhat
level_difficulty = 0 # do kho
target_difficulty = 1000 # do kho muc tieu
difficulty_multiplier = 1.175 # he so do kho
game_over = False # bien kiem tra game over
next_level = False # bien kiem tra chuyen level
enemy_timer = 1000 # thoi gian tao enemy moi
last_enemy = pygame.time.get_ticks() # thoi gian tao enemy cuoi cung
enemies_alive = 0 # so luong enemy con song
max_towers = 8 # so luong thap canh toi da
tower_cost = 10000 # gia thap canh
tower_positions = []
number_of_towers = 0 # so luong thap canh da tao
x_start = screen_width - 300
y_start = 350
x_spacing = 80

for i in range(max_towers):
    tower_positions.append([x_start - i * x_spacing, y_start]) # tao danh sach vi tri thap canh

# load diem cao nhat
if os.path.exists('high_score.txt'): # kiem tra file diem cao nhat ton tai
    with open('high_score.txt', 'r') as file:
        high_score = int(file.read()) # doc diem cao nhat tu file

# mau sac
WHITE = (255, 255, 255)
TEXT = (14, 34, 57)

# define font
font = pygame.font.SysFont('papyrus',20)
font_60 = pygame.font.SysFont('Castellar',60)

# them anh vao game
background = pygame.image.load('images/background.jpg').convert_alpha() # anh nen
background = pygame.transform.scale(background, (screen_width, screen_height)) # thay doi kich thuoc anh nen
# anh lau dai
castle_100 = pygame.image.load('images/castle/castle_100.png').convert_alpha() # anh lau dai 100 hp
castle_50 = pygame.image.load('images/castle/castle_50.png').convert_alpha() # anh lau dai 50 hp
castle_25 = pygame.image.load('images/castle/castle_25.png').convert_alpha() # anh lau dai 25 hp

# anh thap canh
tower_image = pygame.image.load('images/tower.png').convert_alpha() # anh thap canh 100 hp

# anh dan
bullet_image = pygame.image.load('images/bullet.png').convert_alpha()
bullet_width = bullet_image.get_width()
bullet_height = bullet_image.get_height()
bullet_image = pygame.transform.scale(bullet_image, (int(bullet_width * 0.075), int(bullet_height *0.075))) # thay doi kich thuoc dan

# them quan dich
enemy_animations = [] # danh sach chua cac hinh anh chinh
enemy_types = ['young_orc', 'orc', 'bat_orc', 'knight_orc', 'toxin', 'tron', 'purple_cyclop','bee'] # danh sach cac loai quai
enemy_health = [100, 150, 200, 250, 300, 350, 400, 100] # mau cua tung loai quai

animation_types = ['walk', 'attack', 'die'] # cac hinh anh di chuyen, tan cong, chet
for enemy in enemy_types: # duyet qua tung loai quai
    # tao danh sach chua cac hinh anh
    animation_list = []
    for animation in animation_types: # duyet qua tung loai hanh dong
        # reset danh sach tam thoi hinh anh
        temp_list = []
        # xac dinh so khung hinh
        number_of_frames = 20 # so khung hinh
        for i in range(number_of_frames):
            image = pygame.image.load(f'images/enemies/{enemy}/{animation}/{i}.png').convert_alpha() # load hinh anh
            enemy_width = image.get_width()
            enemy_height = image.get_height()
            image = pygame.transform.scale(image, (int(enemy_width * 0.2), int(enemy_height * 0.2))) # thay doi kich thuoc hinh anh
            temp_list.append(image) # them hinh anh vao danh sach tam thoi
        animation_list.append(temp_list) # them danh sach tam thoi vao danh sach hinh anh
    enemy_animations.append(animation_list) # them danh sach hinh anh vao danh sach chinh


# anh button
repair_image = pygame.image.load("images/repair.png").convert_alpha() # repair
armor_image = pygame.image.load("images/armor.png").convert_alpha() # armor
add_tower_image = pygame.image.load("images/add_tower.png").convert_alpha() # tower


# ham hien text len man hinh
def draw_text(text, font, text_color, x, y):
    img = font.render(text, True, text_color) # tao hinh anh tu text
    screen.blit(img, (x, y)) # ve hinh anh tai vi tri x, y
    
    
# ham hien thi trang thai
def show_info():
    draw_text('Money: ' + str(castle.money), font, WHITE, 10, 10)
    draw_text('Score: ' + str(castle.score), font, WHITE, 180, 10)
    draw_text('High Score: ' + str(high_score), font, WHITE, 180, 40)
    draw_text('Level: ' + str(level), font, WHITE, screen_width // 2, 10)
    draw_text('Health: ' + str(castle.health) + '/' + str(castle.max_health), font, TEXT, screen_width - 210, screen_height - 60)
    draw_text('1000', font, WHITE, screen_width - 210, 60)
    draw_text(str(tower_cost), font, WHITE, screen_width - 143, 60)
    draw_text('4000', font, WHITE, screen_width - 65, 60)
    draw_text(str(number_of_towers) + '/' + str(max_towers), font, WHITE, screen_width - 143, 80)
    
# lop castle
class Castle():
    def __init__(self, image100, image50, image25, x, y, scale):
        self.health = 1000
        self.max_health = self.health
        self.fired = False # bien kiem tra da ban hay chua
        self.money = 500000
        self.score = 0
        
        width = image100.get_width()
        height = image100.get_height()
        
        self.image100 = pygame.transform.scale(image100, (int(width * scale), int(height * scale)))
        self.image50 = pygame.transform.scale(image50, (int(width * scale), int(height * scale)))
        self.image25 = pygame.transform.scale(image25, (int(width * scale), int(height * scale)))
        self.rect = self.image100.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
    def shoot(self):
        pos = pygame.mouse.get_pos() # lay vi tri chuot
        x_distance = pos[0] - self.rect.midleft[0] # khoang cach theo truc x
        y_distance = -(pos[1] - self.rect.midleft[1]) # khoang cach theo truc y
        self.angle = math.degrees(math.atan2(y_distance, x_distance)) # tinh goc ban
        # lay su kien nhap chuot
        if pygame.mouse.get_pressed()[0] and self.fired == False and pos[1] > 75: # neu nhan chuot trai va chua ban va vi tri chuot phai lon hon 50
            self.fired = True # da ban
            bullet = Bullet(bullet_image, self.rect.midleft[0],self.rect.midleft[1], self.angle) # tao dan tai vi tri lau dai
            bullet_group.add(bullet) # them dan vao group
        # tao lai su kien nhan chuot
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False # chua ban
        # pygame.draw.line(screen, RED, (self.rect.midleft[0], self.rect.midleft[1]), (pos)) # ve duong thang tu lau dai den vi tri chuot
        
        
    def draw(self):
        # kiem tra anh su dung dua tren mau cua lau dai
        if self.health <= 250:
            self.image = self.image25
        elif self.health <= 500:
            self.image = self.image50
        else:
            self.image = self.image100

        screen.blit(self.image, self.rect) # ve lau dai tai vi tri rect
    
    def repair(self):
        if self.money >= 1000 and self.health < self.max_health: # kiem tra neu co du tien va mau chua day
            self.health += 500
            self.money -= 1000
            if self.health > self.max_health:
                self.health = self.max_health
                
    def armor(self):
        if self.money >= 4000:
            self.max_health += 250
            self.money -= 4000


# tower class
class Tower(pygame.sprite.Sprite): # ke thua tu lop sprite
    def __init__(self, image, x, y, scale):
        pygame.sprite.Sprite.__init__(self)
        
        self.got_target = False # bien kiem tra da co muc tieu hay chua
        self.angle = 0 # goc ban
        self.last_shot = pygame.time.get_ticks() # thoi gian ban cuoi cung
        
        width = image.get_width()
        height = image.get_height()
        
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.image = self.image # mac dinh la hinh 100
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        
        
    def update(self, enemy_group):
        self.got_target = False # mac dinh chua co muc tieu
        
        for e in enemy_group: # duyet qua tung enemy
            if e.alive and e.is_flying == False:
                target_x, target_y = e.rect.midbottom # lay vi tri enemy
                self.got_target = True # da co muc tieu
                break
            
        if self.got_target:
            x_distance = target_x - self.rect.midleft[0] # khoang cach theo truc x
            y_distance = -(target_y - self.rect.midleft[1]) # khoang cach theo truc y
            self.angle = math.degrees(math.atan2(y_distance, x_distance)) # tinh goc ban
        
            shot_cooldown = 2000 # thoi gian ban
            # ban dan
            if pygame.time.get_ticks() - self.last_shot > shot_cooldown: # neu thoi gian ban lon hon thoi gian cho phep ban
                self.last_shot = pygame.time.get_ticks() # cap nhat thoi gian ban cuoi cung
                bullet = Bullet(bullet_image, self.rect.center[0],self.rect.center[1], self.angle) # tao dan tai vi tri thap canh
                bullet_group.add(bullet) # them dan vao group
                
        
            
# bullet class
class Bullet(pygame.sprite.Sprite): # ke thua tu lop sprite
    def __init__(self, image, x, y, angle):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.angle = math.radians(angle) # chuyen goc sang radian
        self.speed = 10 # tat ca dan deu co toc do 10
        # tinh toan toc do theo chieu doc va ngang dua theo goc
        self.dx = math.cos(self.angle) * self.speed # delta x tinh toc do theo chieu ngang
        self.dy = -(math.sin(self.angle) * self.speed) # delta y tinh toc do theo chieu doc
        
        
    def update(self):
        # kiem tra dan da ra khoi man hinh hay chua
        if self.rect.right < 0 or self.rect.left > screen_width or self.rect.top < 0 or self.rect.bottom > screen_height - 80:
            self.kill() # xoa dan khoi group
        
        # di chuyen dan
        self.rect.x += self.dx
        self.rect.y += self.dy
    


class Crosshair():
    def __init__(self, scale):
        image = pygame.image.load('images/crosshair.png').convert_alpha()
        width = image.get_width()
        height = image.get_height()
        
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale))) # thay doi kich thuoc hinh chuot
        self.rect = self.image.get_rect()
        
        # khong hien chuot
        pygame.mouse.set_visible(False)
        
        
    def draw(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.rect.center = (mouse_x, mouse_y)
        screen.blit(self.image, self.rect)
        
        

# create castle
castle = Castle(castle_100, castle_50, castle_25, screen_width - 240, screen_height - 300, 0.2)

#create crosshair
crosshair = Crosshair(0.025)

#create buttons
repair_button = button.Button(screen_width - 220, 10, repair_image, 0.5) # tao button sua chua
tower_button = button.Button(screen_width - 145, 10, add_tower_image, 0.5) # tao button thap canh
armor_button = button.Button(screen_width - 75, 10, armor_image, 0.5) # tao button giap

# create groups
tower_group = pygame.sprite.Group() # tao group cho tower
bullet_group = pygame.sprite.Group() # tao group cho dan
enemy_group = pygame.sprite.Group() # tao group cho enemy


# game loop
running = True
while running:
    
    clock.tick(fps) # thiet lap fps
    
    if game_over == False:
        screen.blit(background, (0, 0)) # ve anh nen tai vi tri 0 0
        
        # ve lau dai
        castle.draw()
        castle.shoot() # ban quai
        # ve thap canh
        tower_group.draw(screen)
        tower_group.update(enemy_group)
        
        # ve dan
        bullet_group.update() # cap nhat vi tri dan
        bullet_group.draw(screen)

        # ve quan dich
        enemy_group.update(screen, castle, bullet_group) # cap nhat vi tri enemy
        
        # hien thi thong tin
        show_info()
        
        # ve nut
        if repair_button.draw(screen) or pygame.key.get_just_pressed()[pygame.K_1]:
            castle.repair()
        if  tower_button.draw(screen) or pygame.key.get_just_pressed()[pygame.K_2]:
            # kiem tra co du tien khong de tao thap canh
            if castle.money >= tower_cost and len(tower_group) < max_towers:
                tower = Tower(
                    tower_image,
                    tower_positions[len(tower_group)][0],
                    tower_positions[len(tower_group)][1],
                    0.2
                )   
                tower_group.add(tower) # them tower vao group
                #tru tien
                castle.money -= tower_cost
                number_of_towers +=1
        if armor_button.draw(screen) or pygame.key.get_just_pressed()[pygame.K_3]:
            castle.armor()
            
        # ve crosshair
        crosshair.draw()
            
        # tao ke dich
        # kiem tra neu da tao toi da so luong ke dich
        if level_difficulty < target_difficulty:
            if pygame.time.get_ticks() - last_enemy > enemy_timer:
                # tao ra enemy
                e = random.randint(0, len(enemy_types) - 1) # random enemy
                if enemy_types[e] == 'bee':
                    enemy = Enemy(enemy_health[e], enemy_animations[e], -50, screen_height - 250, 1, is_flying=True) # enemy bay
                else:
                    enemy = Enemy(enemy_health[e], enemy_animations[e], -50, screen_height - 120, 1, is_flying=False) # enemy khong bay
                enemy_group.add(enemy) # them enemy vao group
                # cap nhat thoi gian tao enemy cuoi cung
                last_enemy = pygame.time.get_ticks()
                # tang muc do kho theo mau cua dich
                level_difficulty += enemy_health[e]
                
                
        # kiem tra neu tat ca ke dich da spawn
        if level_difficulty >= target_difficulty:
            # kiem tra so luong enemy con song
            enemies_alive = 0
            for e in enemy_group:
                if e.alive == True:
                    enemies_alive += 1
            # neu tat ca ke dich da chet thi level da hoan thanh
            if enemies_alive == 0 and next_level == False:
                next_level = True
                level_reset_time = pygame.time.get_ticks()
        
        # chuyen level tiep theo
        if next_level == True:
            draw_text("LEVEL COMPLETE!", font_60, TEXT, 161.5, 100) # ve text "LEVEL COMPLETED"
            # cap nhat diem cao nhat
            if castle.score > high_score:
                high_score = castle.score
                with open('high_score.txt', 'w') as file:
                    file.write(str(high_score))
            if pygame.time.get_ticks() - level_reset_time >= 2000: # neu da qua 2 giay thi chuyen level
                next_level = False
                level += 1
                last_enemy = pygame.time.get_ticks() # cap nhat thoi gian tao enemy cuoi cung
                target_difficulty = int(target_difficulty * difficulty_multiplier)
                level_difficulty = 0 # reset do kho
                enemy_group.empty()
                  
        # check game over
        if castle.health <= 0:
            game_over = True
            
    else:
        draw_text("GAME OVER!", font_60, TEXT, 244, 100) # ve text "GAME OVER"
        draw_text("Press ENTER to restart", font, TEXT, 335.5, 180)
        pygame.mouse.set_visible(True) # hien chuot
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            # reset game variables
            game_over = False
            level = 1
            target_difficulty = 1000
            level_difficulty = 0
            last_enemy = pygame.time.get_ticks()
            enemy_group.empty()
            tower_group.empty()
            bullet_group.empty()
            castle.score = 0
            castle.health = 1000
            castle.money = 0
            castle.max_health = 1000
            pygame.mouse.set_visible(False)
    
     
    # xu ly su kien
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # cap nhat cua so game
    pygame.display.update()
            
pygame.quit() # thoat game