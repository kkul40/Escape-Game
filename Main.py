from secrets import choice
import pygame , sys, random as rnd, math
from pygame.locals import *
from pygame import mixer

class Ghost(): ### DÜŞMAN HAYALET ###
    def __init__(self):
        # RESİMLERİ İMPORT ETME
        self.ghost_appears_img = pygame.image.load("Assets/ghost/ghost-appears.png").convert_alpha()
        self.ghost_ıdle_img = pygame.image.load("Assets/ghost/ghost-idle.png").convert_alpha()
        self.ghost_shriek_img = pygame.image.load("Assets/ghost/ghost-shriek.png").convert_alpha()
        self.ghost_vanish_img = pygame.image.load("Assets/ghost/ghost-vanish.png").convert_alpha()
        self.ghost_shadow_img = pygame.image.load("Assets/ghost/Shadow.png").convert_alpha()
        self.ghost_shadow_img = pygame.transform.scale(self.ghost_shadow_img, (32,32))

        self.ghost_piksel = 64
        self.ghost_scale = self.ghost_piksel * 1.5
        self.ghost_ıdle_img_2 = pygame.transform.scale(self.ghost_ıdle_img, (self.ghost_scale, self.ghost_scale))
        self.img_h = self.ghost_ıdle_img_2.get_height()/2

        self.ghost_animation_speed = 100
        self.ghost_action = 0
        self.ghost_life = 50
        self.timer = 0
        self.wait = 0
        self.fire_timer = 0
        self.fire_ihtimal_tut = main.fire_ihtimal
        self.fire_ihtimal = rnd.randint(0,self.fire_ihtimal_tut)

        self.fire_range_max = main.fire_range_max
        self.fire_nerde = rnd.randint(250, self.fire_range_max)
        self.fire_atıs_sayısı = main.fire_atıs_sayısı
        self.fire_atıs_sayısı_tut = 0
        self.dead = False
        self.ghost_vel = main.ghost_vel
        self.x = 450
        self.y = 450
        self.temp_vel = 10
        self.temp_vel_tut = 0
        self.dist = 1000 # Verilen değer önemli değil

        self.crash_damage = 5
        self.fire_ball_damage = 15

        # DUDE POSİTİON
        self.dude_x = 0
        self.dude_y = 0

        self.is_dude_dead = False

        # HAYALETİN BAKTIĞI YÖN
        self.l_right = True

        # HAYALETİN BAŞLANGIÇ NOKTASINI BELİRLEME
        self.spaw_point = rnd.randint(0,3)
        if self.spaw_point == 0:
            self.x = -70
            self.y = rnd.randint(0,900)
        elif self.spaw_point == 1:
            self.x = 970
            self.y = rnd.randint(0,900)
        elif self.spaw_point == 2:
            self.y = -70
            self.x = rnd.randint(0,900)
        elif self.spaw_point == 3:
            self.y = 970
            self.x = rnd.randint(0,900)

        # ********************************** GHOST RESİM İŞLEME **********************************
        #  GHOST APPEARS
        self.any_img = self.ghost_appears_img
        self.ghost_appears_animation_list = []
        self.ghost_appears_animation_frame = 6
        self.ghost_appears_animation_frame_tut = 0
        for i in range(self.ghost_appears_animation_frame):
            self.ghost_appears_animation_list.append(self.get_image(i,self.any_img))

        #  GHOST IDLE
        self.any_img = self.ghost_ıdle_img
        self.ghost_ıdle_animation_list = []
        self.ghost_ıdle_animation_frame = 7
        self.ghost_ıdle_animation_frame_tut = 0
        for i in range(self.ghost_ıdle_animation_frame):
            self.ghost_ıdle_animation_list.append(self.get_image(i,self.any_img))
        # ters
        self.ghost_ıdle_img = pygame.transform.flip(self.ghost_ıdle_img, True, False)
        self.any_img = self.ghost_ıdle_img
        self.ghost_ıdle_animation_list_right = []
        for i in range(self.ghost_ıdle_animation_frame):
            self.ghost_ıdle_animation_list_right.append(self.get_image(self.ghost_ıdle_animation_frame -i - 1,self.any_img))
        
        #  GHOST SHRIEK
        self.any_img = self.ghost_shriek_img
        self.ghost_shriek_animation_list = []
        self.ghost_shriek_animation_frame = 8
        self.ghost_shriek_animation_frame_tut = 0
        for i in range(self.ghost_shriek_animation_frame - 4):
            self.ghost_shriek_animation_list.append(self.get_image(i,self.any_img))
        for i in range(self.ghost_shriek_animation_frame - 4): # Reverse
            self.ghost_shriek_animation_list.append(self.get_image(3-i,self.any_img))
        # ters
        self.ghost_shriek_img = pygame.transform.flip(self.ghost_shriek_img, True, False)
        self.any_img = self.ghost_shriek_img
        self.ghost_shriek_animation_list_right = []
        for i in range(self.ghost_shriek_animation_frame - 4):
            self.ghost_shriek_animation_list_right.append(self.get_image(3-i,self.any_img))
        for i in range(self.ghost_shriek_animation_frame - 4):
            self.ghost_shriek_animation_list_right.append(self.get_image(i,self.any_img))
            
        #  GHOST VANISH
        self.any_img = self.ghost_vanish_img
        self.ghost_vanish_animation_list = []
        self.ghost_vanish_animation_frame = 7
        self.ghost_vanish_animation_frame_tut = 0
        for i in range(self.ghost_vanish_animation_frame):
            self.ghost_vanish_animation_list.append(self.get_image(i,self.any_img))
        # ters
        self.ghost_vanish_img = pygame.transform.flip(self.ghost_vanish_img, True, False)
        self.any_img = self.ghost_vanish_img
        self.ghost_vanish_animation_list_right = []
        for i in range(self.ghost_vanish_animation_frame):
            self.ghost_vanish_animation_list_right.append(self.get_image(self.ghost_vanish_animation_frame -i - 1,self.any_img))

    def update(self, pos_x, pos_y):
        # GHOST ANİMASYON KONTROLLERİ
        self.cor_pos_x = self.x - self.img_h
        self.cor_pos_y = self.y - self.img_h

        if main.dude.dead and not self.dead:
            self.ghost_action = 2

        ekran.blit(self.ghost_shadow_img, (self.x - self.ghost_shadow_img.get_width()/2, self.y+40))

        if self.ghost_action == 0:
            self.ghost_spawn(self.cor_pos_x, self.cor_pos_y)
        elif self.ghost_action == 1:
            self.ghost_ıdle(self.cor_pos_x, self.cor_pos_y)
        elif self.ghost_action == 2:
            self.ghost_attack(self.cor_pos_x, self.cor_pos_y)
        elif self.ghost_action == 3:
            self.ghost_dead(self.cor_pos_x, self.cor_pos_y)

        self.draw_lifebar(self.cor_pos_x, self.cor_pos_y)
        self.ghost_move(pos_x, pos_y)
        self.ghost_comming()

        # GHOST HİTPOİNTİ
        if self.ghost_action == 3:
            self.ghost_rect = pygame.Rect(-100,-100,0,0)
        else:
            self.ghost_rect = pygame.Rect(self.cor_pos_x + 25, self.cor_pos_y + 35, self.img_h, self.img_h)
        
        if main.hit_point:
            pygame.draw.rect(ekran, (100,0,0), self.ghost_rect, 1)
            pygame.draw.rect(ekran, (255,255,255), (self.x-2, self.y-2, 4,4))

    def ghost_move(self, pos_x, pos_y):
        if main.supriz:
            if self.temp_vel > 0:
                self.temp_vel_tut -= 10
            else:
                self.temp_vel_tut += 10

            self.x += (-self.ghost_vel + self.temp_vel_tut) * deltaTime
            self.y += (self.ghost_vel + self.temp_vel_tut) * deltaTime

            if abs(self.temp_vel_tut) >= 200:
                self.ghost_vel *= -1
                self.temp_vel *= -1
        else:
            if self.ghost_action == 1:
                dx, dy = self.x - pos_x, self.y - pos_y
                self.dist = math.hypot(dx, dy)
                dx, dy = dx/self.dist, dy/self.dist
                self.x -= dx * (self.ghost_vel * deltaTime)
                self.y -= dy * (self.ghost_vel * deltaTime)

                if self.fire_ihtimal == 0 and self.fire_nerde < round(self.dist) and self.fire_atıs_sayısı_tut < self.fire_atıs_sayısı and pygame.time.get_ticks() - self.wait >= 2000:
                    self.wait = pygame.time.get_ticks()
                    self.ghost_action = 2
                    self.fire_atıs_sayısı_tut += 1
                    self.fire_nerde = rnd.randint(250, self.fire_range_max)

                if dx > 0: # GHOST YÖN DEĞİŞTİRME
                    self.l_right = False
                else:
                    self.l_right = True
    
    def ghost_get_damage(self, damage):
        self.ghost_life -= damage
        if self.ghost_life <= 0:
            main.sound.ghost_dead()
            self.ghost_action = 3
        else: 
            main.sound.ghost_hit()
    # GHOST EKRANA BASMA
    def ghost_comming(self): # GHOST UN GELCEĞİ YERİ ÖNCEDEN BELİRTME
        if self.x < -10:
            pygame.draw.rect(ekran, (255,0,0), (0, self.y, 5, self.img_h))
        elif self.x > 910:
            pygame.draw.rect(ekran, (255,0,0), (895, self.y, 5, self.img_h))
        elif self.y < -10:
            pygame.draw.rect(ekran, (255,0,0), (self.x - self.img_h/2, 0, self.img_h, 5))
        elif self.y > 910:
            pygame.draw.rect(ekran, (255,0,0), (self.x - self.img_h/2, 895, self.img_h, 5))

    def draw_lifebar(self, pos_x, pos_y):
        if self.ghost_action == 3:
            self.heatlh_bar = pygame.Rect(-100,-100,0,0)
            self.heatlh_bar_window = pygame.Rect(-100,-100,0,0)
        else:
            self.heatlh_bar = pygame.Rect(self.x - self.ghost_life/2 - 3, pos_y, self.ghost_life, 6)
            self.heatlh_bar_window = pygame.Rect(pos_x +20, pos_y, 50, 6)

        #self.heatlh_bar = pygame.Rect(pos_x +20, pos_y, self.ghost_life, 6)
        pygame.draw.rect(ekran, (0,150,0), self.heatlh_bar) 
        pygame.draw.rect(ekran, (0,0,0), self.heatlh_bar_window, 1)
    
    def ghost_spawn(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.ghost_animation_speed:
            self.ghost_appears_animation_frame_tut += 1
            self.timer = pygame.time.get_ticks()
            if self.ghost_appears_animation_frame_tut >= len(self.ghost_appears_animation_list):
                self.ghost_appears_animation_frame_tut = 0
                self.ghost_action = 1
        ekran.blit(self.ghost_appears_animation_list[self.ghost_appears_animation_frame_tut], (pos_x, pos_y))

    def ghost_ıdle(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.ghost_animation_speed:
            self.ghost_ıdle_animation_frame_tut += 1
            self.timer = pygame.time.get_ticks()
            if self.ghost_ıdle_animation_frame_tut >= len(self.ghost_ıdle_animation_list):
                self.ghost_ıdle_animation_frame_tut = 0

        if self.l_right:
            ekran.blit(self.ghost_ıdle_animation_list_right[self.ghost_ıdle_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.ghost_ıdle_animation_list[self.ghost_ıdle_animation_frame_tut], (pos_x, pos_y))

    def ghost_attack(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.ghost_animation_speed:
            self.ghost_shriek_animation_frame_tut += 1
            self.timer = pygame.time.get_ticks()
            if self.ghost_shriek_animation_frame_tut == 2 and not main.dude.dead:
                main.fire_ball_list.append(Ghost_Fire_Ball(self.x,self.y))
            if self.ghost_shriek_animation_frame_tut >= len(self.ghost_shriek_animation_list):
                self.ghost_shriek_animation_frame_tut = 0
                if main.dude.dead:
                    self.ghost_action = 2
                else:
                    self.ghost_action = 1

        if self.l_right:
            ekran.blit(self.ghost_shriek_animation_list_right[self.ghost_shriek_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.ghost_shriek_animation_list[self.ghost_shriek_animation_frame_tut], (pos_x, pos_y))

    def ghost_dead(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= 50 and not self.dead:
            self.ghost_vanish_animation_frame_tut += 1
            self.timer = pygame.time.get_ticks()
            if self.ghost_vanish_animation_frame_tut >= len(self.ghost_vanish_animation_list):
                self.ghost_vanish_animation_frame_tut = 6
                self.dead = True
        if not self.dead:
            if self.l_right:
                ekran.blit(self.ghost_vanish_animation_list_right[self.ghost_vanish_animation_frame_tut], (pos_x, pos_y))
            else:
                ekran.blit(self.ghost_vanish_animation_list[self.ghost_vanish_animation_frame_tut], (pos_x, pos_y))

    def random_pos_ver(self):
        self.x = rnd.randint(100,800)
        self.y = rnd.randint(100,800)

    # GHOST İMAGE LİST OLUŞTURMA
    def get_image(self, frame, img):
        image = pygame.Surface((self.ghost_piksel, self.ghost_piksel)).convert_alpha()
        image.blit(img, (0, 0), (self.ghost_piksel * frame, 0, self.ghost_piksel, self.ghost_piksel))
        image = pygame.transform.scale(image, (self.ghost_scale, self.ghost_scale))
        image.set_colorkey("black")
        return image
   
    def get_ghost_rect(self): return self.ghost_rect

class Dude(): ### KARAKTER ###
    def __init__(self):
        # RESİMLERİ İMPORT ETME
        self.dude_run_img = pygame.image.load("Assets\dude\Dude_Monster_run_6.png").convert_alpha()
        self.dude_ıdle_img = pygame.image.load("Assets\dude\Dude_Monster_Idle_4.png").convert_alpha()
        self.dude_death_img = pygame.image.load("Assets\dude\Dude_Monster_Death_8.png").convert_alpha()
        self.dude_back_img = pygame.image.load("Assets\dude\Dude_Monster_Back_4.png").convert_alpha()
        self.dude_throw_img = pygame.image.load("Assets\dude\Dude_Monster_Throw_4.png").convert_alpha()
        self.dude_run_throw_img = pygame.image.load("Assets\dude\Dude_Monster_Walk+Attack_6.png").convert_alpha()
        self.dude_hurt_img = pygame.image.load("Assets\dude\Dude_Monster_Hurt_4.png").convert_alpha()
        self.dude_dust_img = pygame.image.load("Assets\dude\Walk_Run_Push_Dust_6.png").convert_alpha()

        self.dude_timer = 0
        self.one_time = 0
        self.dude_animation_speed = 100
        self.dude_timer2 = 0
        self.dude_animation_speed2 = 100
        self.dude_piksel = 32
        self.dude_scale = self.dude_piksel * 2
        self.img_h = self.dude_ıdle_img.get_height() * 2
        self.img_h_2 = self.img_h/2
        self.dude_action = 0
        self.dude_shift_vel = 0
        self.dude_life = 100
        self.dude_shift = 100
        self.dude_is_shift = False
        self.dude_vel = 0 # mainden kontrol ediliyor
        self.dead = False
        self.run_sound_once = 0

        self.rock_sayısı = 1

        self.dont_get_damage_timer = 500
        self.dont_get_damage_time = 0

        # HAREKET YÖNLERİ
        self.k_up = False
        self.k_down = False
        self.k_left = False
        self.k_right = False

        # KARAKTERİN BAKTIĞI YÖN
        self.l_left = False

        # KARAKTERİN BAŞLANGIÇ NOKTASI
        self.x = 450
        self.y = 450
        self.cor_pos_x = self.x - self.img_h_2
        self.cor_pos_y = self.y - self.img_h_2

        # ********************************** KARAKTER RESİMLERİNİ İŞLEME **********************************
        # DUDE IDLE
        self.any_img = self.dude_ıdle_img
        self.dude_ıdle_animation_list = []
        self.dude_ıdle_animation_frame = 4
        self.dude_ıdle_animation_frame_tut = 0
        for i in range(self.dude_ıdle_animation_frame):
            self.dude_ıdle_animation_list.append(self.get_image(i,self.any_img))
        # Ters
        self.dude_ıdle_img = pygame.transform.flip(self.dude_ıdle_img, True, False)
        self.any_img = self.dude_ıdle_img
        self.dude_ıdle_animation_list_left = []
        for i in range(self.dude_ıdle_animation_frame):
            self.dude_ıdle_animation_list_left.append(self.get_image(self.dude_ıdle_animation_frame -i-1,self.any_img))

        #  DUDE RUN
        self.any_img = self.dude_run_img
        self.dude_run_animation_list = []
        self.dude_run_animation_frame = 6
        self.dude_run_animation_frame_tut = 0
        for i in range(self.dude_run_animation_frame):
            self.dude_run_animation_list.append(self.get_image(i,self.any_img))
        # Ters
        self.dude_run_img = pygame.transform.flip(self.dude_run_img, True, False)
        self.any_img = self.dude_run_img
        self.dude_run_animation_list_left = []
        for i in range(self.dude_run_animation_frame):
            self.dude_run_animation_list_left.append(self.get_image((self.dude_run_animation_frame -i-1),self.any_img))

        # DUDE RUN DUST
        self.any_img = self.dude_dust_img
        self.dude_dust_animation_list = []
        self.dude_dust_animation_frame = 6
        self.dude_dust_animation_frame_tut = 0
        for i in range(self.dude_dust_animation_frame):
            self.dude_dust_animation_list.append(self.get_image(i,self.any_img))
        # Ters
        self.dude_dust_img = pygame.transform.flip(self.dude_dust_img, True, False)
        self.any_img = self.dude_dust_img
        self.dude_dust_animation_list_left = []
        for i in range(self.dude_dust_animation_frame):
            self.dude_dust_animation_list_left.append(self.get_image((self.dude_dust_animation_frame -i-1),self.any_img))

        # DUDE BACK
        self.any_img = self.dude_back_img
        self.dude_back_animation_list = []
        self.dude_back_animation_frame = 4
        self.dude_back_animation_frame_tut = 0
        for i in range(self.dude_back_animation_frame):
            self.dude_back_animation_list.append(self.get_image(i,self.any_img))

        # DUDE HURT
        self.any_img = self.dude_hurt_img
        self.dude_hurt_animation_list = []
        self.dude_hurt_animation_frame = 4
        self.dude_hurt_animation_frame_tut = 0
        for i in range(self.dude_back_animation_frame):
            self.dude_hurt_animation_list.append(self.get_image(i,self.any_img))
        # Ters
        self.dude_hurt_img = pygame.transform.flip(self.dude_hurt_img, True, False)
        self.any_img = self.dude_hurt_img
        self.dude_hurt_animation_list_left = []
        for i in range(self.dude_hurt_animation_frame):
            self.dude_hurt_animation_list_left.append(self.get_image(self.dude_hurt_animation_frame -i-1,self.any_img))
        
        #  DUDE DEATH
        self.any_img = self.dude_death_img
        self.dude_death_animation_list = []
        self.dude_death_animation_frame = 8
        self.dude_death_animation_frame_tut = 0
        for i in range(self.dude_death_animation_frame):
            self.dude_death_animation_list.append(self.get_image(i,self.any_img))
        # ters
        self.dude_death_img = pygame.transform.flip(self.dude_death_img, True, False)
        self.any_img = self.dude_death_img
        self.dude_death_animation_list_left = []
        for i in range(self.dude_death_animation_frame):
            self.dude_death_animation_list_left.append(self.get_image(self.dude_death_animation_frame -i-1, self.any_img))

        # DUDE THROW ROCK
        self.any_img = self.dude_throw_img
        self.dude_throw_animation_list = []
        self.dude_throw_animation_frame = 4
        self.dude_throw_animation_frame_tut = 0
        for i in range(self.dude_throw_animation_frame):
            self.dude_throw_animation_list.append(self.get_image(i,self.any_img))
        # ters
        self.dude_throw_img = pygame.transform.flip(self.dude_throw_img, True, False)
        self.any_img = self.dude_throw_img
        self.dude_throw_animation_list_left = []
        for i in range(self.dude_throw_animation_frame):
            self.dude_throw_animation_list_left.append(self.get_image(self.dude_throw_animation_frame -i -1,self.any_img))

        # DUDE RUN THROW ROCK
        self.any_img = self.dude_run_throw_img
        self.dude_run_throw_animation_list = []
        self.dude_run_throw_animation_frame = 6
        self.dude_run_throw_animation_frame_tut = 0
        for i in range(self.dude_run_throw_animation_frame):
            self.dude_run_throw_animation_list.append(self.get_image(i,self.any_img))
        # Ters
        self.dude_run_throw_img = pygame.transform.flip(self.dude_run_throw_img, True, False)
        self.any_img = self.dude_run_throw_img
        self.dude_run_throw_animation_list_left = []
        for i in range(self.dude_run_throw_animation_frame):
            self.dude_run_throw_animation_list_left.append(self.get_image(self.dude_run_throw_animation_frame -i -1,self.any_img))

    def update(self):
        # KARAKTER ANİMASYON KONTROLLERİ
        self.cor_pos_x = self.x - self.img_h_2
        self.cor_pos_y = self.y - self.img_h_2

        self.is_running = self.k_left or self.k_right or self.k_down or self.k_up

        self.is_dude_dead()
        if self.dead:
            self.x = -500
        
        if self.dude_action == 0:#Idle
            self.draw_dude_ıdle(self.cor_pos_x, self.cor_pos_y)
        elif self.dude_action == 1:#Run
            self.draw_dude_run(self.cor_pos_x, self.cor_pos_y)
        elif self.dude_action == 2:#Run Attack
            self.draw_dude_run_attack(self.cor_pos_x, self.cor_pos_y)
        elif self.dude_action == 3:#Attack
            self.draw_dude_stand_attack(self.cor_pos_x, self.cor_pos_y)
        elif self.dude_action == 4:#Death
            self.draw_dude_death(self.cor_pos_x, self.cor_pos_y)
        elif self.dude_action == 5:#Hurt
            self.draw_dude_hurt(self.cor_pos_x, self.cor_pos_y)

        if self.dude_is_shift and self.is_running and self.dude_shift > 0:
            if self.dude_shift < 1:
                main.dude.dude_is_shift = False
            self.draw_dude_dust(self.cor_pos_x, self.cor_pos_y)
            self.dude_shift_vel = 200
            if self.dude_shift > 0:
                self.dude_shift -= 30 * deltaTime
        else:
            self.dude_shift_vel = 0
            if self.dude_shift < 100:
                self.dude_shift += 10 * deltaTime

        self.draw_lifebar()
        self.draw_shiftbar()
        
        self.dude_move()

        # KARAKTER HASAR ALANI
        self.dude_rect = pygame.Rect(self.cor_pos_x + 10 , self.cor_pos_y + 12, self.img_h - 20, self.img_h - 10)
        if main.hit_point:
            pygame.draw.rect(ekran, (255,0,0), self.dude_rect, 1)
        
    def dude_move(self): # KARAKTER HARETLENDİRME
        if self.dude_action != 4:
            if self.k_up:
                self.y -= (self.dude_vel + self.dude_shift_vel) * deltaTime
            if self.k_down:
                self.y += (self.dude_vel + self.dude_shift_vel) * deltaTime
            if self.k_left:
                self.x -= (self.dude_vel + self.dude_shift_vel) * deltaTime
            if self.k_right:
                self.x += (self.dude_vel + self.dude_shift_vel) * deltaTime

        # DUVARLAR
        if not self.dead:
            if self.x > 900:
                self.x = 900
            elif self.x < 0:
                self.x = 0
            elif self.y > 900:
                self.y = 900
            elif self.y < 0:
                self.y = 0
    # KARAKTERİ EKRANA BASMA
    def draw_lifebar(self):
        self.heatlh_bar = pygame.Rect(690 , 10, self.dude_life * 2, 30)
        self.heatlh_bar_window = pygame.Rect(690 , 10, 200, 30)
        
        pygame.draw.rect(ekran, (0,255,0), self.heatlh_bar) 
        pygame.draw.rect(ekran, (0,0,0), self.heatlh_bar_window, 2)

    def draw_shiftbar(self):
        self.shift_bar = (690, 45, self.dude_shift*2, 30)
        self.shift_bar_window = (690, 45, 200, 30)

        pygame.draw.rect(ekran, (13,117,196), self.shift_bar) 
        pygame.draw.rect(ekran, (0,0,0), self.shift_bar_window,2) 

    def draw_dude_ıdle(self, pos_x, pos_y):
        if self.is_running:
            self.dude_action = 1
        elif pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
            self.dude_ıdle_animation_frame_tut += 1
            self.dude_timer = pygame.time.get_ticks()
            if self.dude_ıdle_animation_frame_tut >= len(self.dude_ıdle_animation_list):
                self.dude_ıdle_animation_frame_tut = 0
                self.dude_action = 0

        if self.l_left:
            ekran.blit(self.dude_ıdle_animation_list_left[self.dude_ıdle_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.dude_ıdle_animation_list[self.dude_ıdle_animation_frame_tut], (pos_x, pos_y))

    def draw_dude_run(self, pos_x, pos_y):
        if self.k_up and not self.k_left and not self.k_right and not self.k_down:
            if pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
                self.dude_back_animation_frame_tut += 1
                self.dude_timer = pygame.time.get_ticks()
                if self.dude_back_animation_frame_tut >= len(self.dude_back_animation_list):
                    self.dude_back_animation_frame_tut = 0
                    self.dude_action = 1

            ekran.blit(self.dude_back_animation_list[self.dude_back_animation_frame_tut], (pos_x, pos_y))
        else:
            if pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
                self.dude_run_animation_frame_tut += 1
                self.dude_timer = pygame.time.get_ticks()
                if self.dude_run_animation_frame_tut >= len(self.dude_run_animation_list):
                    self.dude_run_animation_frame_tut = 0

            if self.l_left or self.k_left:
                ekran.blit(self.dude_run_animation_list_left[self.dude_run_animation_frame_tut], (pos_x, pos_y))
            else:
                ekran.blit(self.dude_run_animation_list[self.dude_run_animation_frame_tut], (pos_x, pos_y))

        if self.is_running:
            self.dude_action = 1
        else:
            self.dude_action = 0

    def draw_dude_dust(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.dude_timer2 >= self.dude_animation_speed2:
            self.dude_dust_animation_frame_tut += 1
            self.dude_timer2 = pygame.time.get_ticks()
            if self.dude_dust_animation_frame_tut >= len(self.dude_dust_animation_list):
                self.dude_dust_animation_frame_tut = 0

        if self.l_left:
            ekran.blit(self.dude_dust_animation_list_left[self.dude_dust_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.dude_dust_animation_list[self.dude_dust_animation_frame_tut], (pos_x, pos_y))

    def draw_dude_stand_attack(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
            self.dude_throw_animation_frame_tut += 1
            self.dude_timer = pygame.time.get_ticks()
            if self.dude_throw_animation_frame_tut == 1:
                if main.mouse_pos[0] > self.x:
                    self.l_left = False
                else:
                    self.l_left = True
            if self.dude_throw_animation_frame_tut >= len(self.dude_throw_animation_list):
                self.dude_throw_animation_frame_tut = 0
                self.dude_action = 0
        if self.l_left:
            ekran.blit(self.dude_throw_animation_list_left[self.dude_throw_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.dude_throw_animation_list[self.dude_throw_animation_frame_tut], (pos_x, pos_y))
    
    def draw_dude_run_attack(self, pos_x, pos_y):
        if not self.is_running:
            self.dude_action = 0
        elif pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
            self.dude_run_throw_animation_frame_tut += 1
            self.dude_timer = pygame.time.get_ticks()
            if self.dude_run_throw_animation_frame_tut == 2:
                if main.mouse_pos[0] > self.x:
                    self.l_left = False
                else:
                    self.l_left = True
            if self.dude_run_throw_animation_frame_tut >= len(self.dude_run_throw_animation_list):
                self.dude_run_throw_animation_frame_tut = 0
                self.dude_action = 0
        if self.l_left:
            ekran.blit(self.dude_run_throw_animation_list_left[self.dude_run_throw_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.dude_run_throw_animation_list[self.dude_run_throw_animation_frame_tut], (pos_x, pos_y))

    def draw_dude_hurt(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
            self.dude_hurt_animation_frame_tut += 1
            self.dude_timer = pygame.time.get_ticks()
            if self.dude_hurt_animation_frame_tut >= len(self.dude_hurt_animation_list):
                self.dude_hurt_animation_frame_tut = 0
                self.dude_action = 0

        if self.l_left:
            ekran.blit(self.dude_hurt_animation_list_left[self.dude_hurt_animation_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.dude_hurt_animation_list[self.dude_hurt_animation_frame_tut], (pos_x, pos_y))

    def draw_dude_death(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.dude_timer >= self.dude_animation_speed:
            self.dude_death_animation_frame_tut += 1
            self.dude_timer = pygame.time.get_ticks()
            if self.dude_death_animation_frame_tut >= len(self.dude_death_animation_list):
                self.dude_death_animation_frame_tut = 0
                # ÖLDÜKTEN SONRA NE YAPILSIN
                self.dead = True
                main.yandın = True
                # ÖLDÜKTEN SONRA NE YAPILSIN
                if self.one_time == 0:
                    main.gecen_sure_tut = main.gecen_sure
                    self.one_time = 1
        if not self.dead: # BUGG OLUŞMASIN DİYE
            if self.l_left:
                ekran.blit(self.dude_death_animation_list_left[self.dude_death_animation_frame_tut], (pos_x, pos_y))
            else:
                ekran.blit(self.dude_death_animation_list[self.dude_death_animation_frame_tut], (pos_x, pos_y))

    def get_dude_damage(self, damage):
        if pygame.time.get_ticks() - self.dont_get_damage_time >= self.dont_get_damage_timer:
            self.dont_get_damage_time = pygame.time.get_ticks()
            self.dude_life -= damage
            self.dude_hurt_animation_frame_tut = 0
            self.dude_action = 5
            main.sound.hit()
    
    def is_dude_dead(self):
        if self.dude_life <= 0:
            self.run_sound_once += 1
            self.dude_action = 4
            if self.run_sound_once == 1:
                main.sound.game_over()
                self.run_sound_once += 1

    def heal_dude_life(self, heal):
        self.dude_life += heal
        if self.dude_life >= 100:
            self.dude_life = 100
    # KARAKTERİ KARE KARE İŞLEME
    def get_image(self, frame, img):
        image = pygame.Surface((self.dude_piksel, self.dude_piksel)).convert_alpha()
        image.blit(img, (0, 0), (self.dude_piksel * frame, 0, self.dude_piksel, self.dude_piksel))
        image = pygame.transform.scale(image, (self.dude_scale, self.dude_scale))
        image.set_colorkey("black")
        return image
    # KARAKTER POZİSYONUNU DÜŞMANA BİLDİRME
    def get_dude_position_x(self): return self.x
        
    def get_dude_position_y(self): return self.y

class Dude_Rock(): # TAŞ
    def __init__(self, pos_x, pos_y):# TAŞIN GİDECEĞİ YÖNÜN GİRDİLERİ
        # TAŞ RESMİ
        self.dude_rock_img = pygame.image.load("Assets\dude\Rock1.png").convert_alpha()
        self.rock_h = self.dude_rock_img.get_height()/2

        # TAŞIN BAŞLANGIÇ NOKTASI
        self.rock_x = main.dude.get_dude_position_x()
        self.rock_y = main.dude.get_dude_position_y()

        self.rock_damage = main.rock_damage
        self.rock_vel = main.rock_vel
        self.sekme_sayisi = main.rock_sekme_sayisi
        self.sekme_say = 0
        self.rock_vurulanlar = []

        # TAŞIN HEDEFİ
        self.m_pos_x = pos_x
        self.m_pos_y = pos_y

        # TAŞ HAREKET GÜZERGAHI
        self.dx, self.dy = self.rock_x - self.m_pos_x, self.rock_y - self.m_pos_y
        self.dist = math.hypot(self.dx, self.dy)
        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist
        # TAŞ RESMİNİ İŞLEME
        self.dude_rock_animation = self.get_img(self.dude_rock_img)

    def update(self):
        # TAŞ KONTROLLERİ
        self.rock_pos_x = self.rock_x - self.rock_h
        self.rock_pos_y = self.rock_y - self.rock_h
        self.draw_rock(self.rock_pos_x, self.rock_pos_y)

        # SEKTİRME
        if self.sekme_sayisi > 0:
            self.sektir()
            
        self.move()

        # TAŞIN HİTPOİNTİ
        self.rock_rect = pygame.Rect(self.rock_pos_x, self.rock_pos_y, self.rock_h*4, self.rock_h*4)
        if main.hit_point:
            pygame.draw.rect(ekran, (100,0,0), self.rock_rect, 1)

    def move(self):
        self.rock_x -= (self.dx * self.rock_vel) * deltaTime
        self.rock_y -= (self.dy * self.rock_vel) * deltaTime
        
    def sektir(self):
        if self.sekme_say < self.sekme_sayisi:
            if self.rock_x > 900 or self.rock_x < 0:
                main.sound.sekme()
                self.dx *= -1
                self.sekme_say += 1
                self.rock_vurulanlar = []
            elif self.rock_y > 900 or self.rock_y < 0:
                main.sound.sekme()
                self.dy *= -1
                self.sekme_say += 1
                self.rock_vurulanlar = []

    def get_img (self, img):
        image = pygame.Surface((8, 8)).convert_alpha()
        image.blit(img, (0, 0), (0, 0, 8, 8))
        image = pygame.transform.scale(image, (15, 15))
        image.set_colorkey("black")
        return image
    # TAŞI EKRANA BASMA
    def draw_rock(self, pos_x, pos_y): ekran.blit(self.dude_rock_animation, (pos_x, pos_y))
        
class Ghost_Fire_Ball():
    def __init__(self,pos_x, pos_y):
        self.fire_ball_img = pygame.image.load("Assets/ghost/fire-ball.png").convert_alpha()
        self.fire_h = self.fire_ball_img.get_height()/2

        self.fire_animation_speed = 100
        self.fire_timer = 0

        self.l_right = False
        self.yok_ol = False

        # FİRE-BALIN BAŞLANGIÇ NOKTASI
        self.fire_x = pos_x
        self.fire_y = pos_y
        
        self.fire_damage = 20
        self.fire_vel = main.fire_ball_vel

        # FİRE-BALIN HEDEFİ
        self.m_pos_x = main.dude.get_dude_position_x()
        self.m_pos_y = main.dude.get_dude_position_y()

        # FİRE-BALL HAREKET GÜZERGAHI
        self.dx, self.dy = self.fire_x - self.m_pos_x, self.fire_y - self.m_pos_y
        self.dist = math.hypot(self.dx, self.dy)
       
        self.cos_a = math.acos(self.dx / self.dist)
        self.rotate = math.degrees(self.cos_a)

        self.dx, self.dy = self.dx/self.dist, self.dy/self.dist

        # FİRE-BALL RESMİNİ İŞLEME
        self.any_img = self.fire_ball_img
        self.ghost_fire_ball_animation_list = []
        self.ghost_fire_ball_animation_frame = 3
        self.ghost_fire_ball_animation_frame_tut = 0
        for i in range(self.ghost_fire_ball_animation_frame):
            self.ghost_fire_ball_animation_list.append(self.get_img(i,self.any_img))
        # ters
        self.fire_ball_img = pygame.transform.flip(self.fire_ball_img, True, False)
        self.any_img = self.fire_ball_img
        self.ghost_fire_ball_animation_list_right = []
        for i in range(self.ghost_fire_ball_animation_frame):
            self.ghost_fire_ball_animation_list_right.append(self.get_img(self.ghost_fire_ball_animation_frame -i - 1,self.any_img))
    
    def update(self):
        # FİRE-BALL KONTROLLERİ
        self.fire_pos_x = self.fire_x - self.fire_h
        self.fire_pos_y = self.fire_y - self.fire_h
        self.draw_fire_ball(self.fire_pos_x, self.fire_pos_y)

        self.move()

        # FİRE-BALIN HİTPOİNTİ
        self.fire_rect = pygame.Rect(self.fire_pos_x + 2, self.fire_pos_y + 5, self.fire_h*3, self.fire_h*3 - 10)
        if main.hit_point:
            pygame.draw.rect(ekran, (100,0,0), self.fire_rect, 1)

    def move(self):
        self.fire_x -= self.dx * (self.fire_vel * deltaTime)
        self.fire_y -= self.dy * (self.fire_vel * deltaTime)

        if self.dx > 0: # DÜŞMANIN BAKTIĞI YÖNÜ DEĞİŞTİRME
            self.l_right = False
        else:
            self.l_right = True

    def draw_fire_ball(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.fire_timer >= self.fire_animation_speed:
            self.ghost_fire_ball_animation_frame_tut += 1
            self.fire_timer = pygame.time.get_ticks()
            if self.ghost_fire_ball_animation_frame_tut >= len(self.ghost_fire_ball_animation_list):
                self.ghost_fire_ball_animation_frame_tut = 0
        ekran.blit(self.ghost_fire_ball_animation_list[self.ghost_fire_ball_animation_frame_tut], (pos_x, pos_y))

    def get_img (self,frame, img):
        image = pygame.Surface((19, 19)).convert_alpha()
        image.blit(img, (0, 0), (19 * frame, 0, 19, 19))
        image = pygame.transform.scale(image, (19*1.5, 19*1.5))
        if self.dx < 0 and self.dy < 0:
            image = pygame.transform.rotate(image, self.rotate)
        elif self.dx < 0 and self.dy > 0:
            image = pygame.transform.rotate(image, -self.rotate)
        elif self.dx > 0 and self.dy < 0:
            image = pygame.transform.rotate(image, self.rotate)
        elif self.dx > 0 and self.dy > 0:
            image = pygame.transform.rotate(image, -self.rotate)
        
        image.set_colorkey("black")
        return image

class Yemek():
    def __init__(self):
        self.bos_tabak_img = pygame.image.load("Assets/food/01_dish.png").convert_alpha()# BOŞ TABAK
        self.bos_tabak_animation = self.get_img(self.bos_tabak_img)
        self.apple_pie_food_img = pygame.image.load("Assets/food/05_apple_pie.png").convert_alpha()
        self.apple_pie_food_animation = self.get_img(self.apple_pie_food_img) #0 TAŞ SEKTİRME
        self.pizza_food_img = pygame.image.load("Assets/food/81_pizza.png").convert_alpha()
        self.pizza_food_animation = self.get_img(self.pizza_food_img) #1 HAREKET HIZI ARTTIRMA
        self.burger_food_img = pygame.image.load("Assets/food/15_burger.png").convert_alpha()
        self.burger_food_animation = self.get_img(self.burger_food_img) #2 CAN DOLDURMA
        self.fruitcake_food_img = pygame.image.load("Assets/food/46_fruitcake.png").convert_alpha()
        self.fruitcake_food_animation = self.get_img(self.fruitcake_food_img) #3 SHİFT BAR DOLDURMA

        self.img_h = self.bos_tabak_img.get_height()/2

        self.x = rnd.randint(0, 900 - self.apple_pie_food_img.get_height())
        self.y = -50
        self.yok_ol = False
        self.yemek_vel = main.yemek_vel
        self.yendi_mi = False
        
        self.food_sec = self.bos_tabak_animation
        self.secim = rnd.randint(0,3)
        self.secim_yap()
        
    def update(self):
        self.cor_pos_x = self.x - self.img_h
        self.cor_pos_y = self.y - self.img_h

        self.draw_food(self.cor_pos_x, self.cor_pos_y)
        self.move()

        # YEMEK HİTPOİNTİ
        self.yemek_rect = pygame.Rect(self.cor_pos_x, self.cor_pos_y, self.img_h*2, self.img_h*2)
        # YEMEK ÇİZDİRME
        if main.hit_point:
            pygame.draw.rect(ekran, (0,0,200), self.yemek_rect, 1)

    def move(self): 
        if self.y > 910:
            self.yok_ol = True
        else:
            self.y += self.yemek_vel * deltaTime

    def draw_food(self, pos_x, pos_y): ekran.blit(self.food_sec, (pos_x, pos_y))

    def secim_yap(self):
        if self.yendi_mi:
            main.sound.power_up()
            if self.secim == 0:
                main.rock_sekme_sayisi += 1
                main.rock_timer -= 50
                main.dude_spec_yazdır()
            elif self.secim == 1:
                main.set_dude_vel(20)
                main.dude_spec_yazdır()
            elif self.secim == 2:
                main.dude.heal_dude_life(25)
            elif self.secim == 3:
                main.dude.dude_shift += 30
                if main.dude.dude_shift >= 100:
                    main.dude.dude_shift = 100
        else:
            if self.secim == 0:
                self.food_sec = self.apple_pie_food_animation
            elif self.secim == 1:
                self.food_sec = self.pizza_food_animation
            elif self.secim == 2:
                self.food_sec = self.burger_food_animation
            elif self.secim == 3:
                self.food_sec = self.fruitcake_food_animation

    def get_img(self, img):
        image = pygame.Surface((32, 32)).convert_alpha()
        image.blit(img, (0, 0), (0, 0, 32, 32))
        image.set_colorkey("black")
        return image

class Sound():
    def __init__(self):
        self.background_music = mixer.Sound("Assets/sound/Run As Fast As You Can.wav")
        self.background_music.play(-1)

        self.hit_sound = mixer.Sound("Assets/sound/hitHurt.wav")
        self.power_up_sound = mixer.Sound("Assets/sound/powerUp.wav")
        self.power_down_sound = mixer.Sound("Assets/sound/powerDown.wav")
        self.run_sound = mixer.Sound("Assets/sound/run.wav")
        self.sekme_sound = mixer.Sound("Assets/sound/sekme.wav")
        self.fırlat_sound = mixer.Sound("Assets/sound/fırlat.wav")
        self.hit_ghost_sound = mixer.Sound("Assets/sound/hitGhost.wav")
        self.ghost_dead_sound = mixer.Sound("Assets/sound/ghostDead.wav")
        self.game_over_sound = mixer.Sound("Assets/sound/GameOver.wav")
        
        self.kıs1 = 1
        self.kıs2 = 1

    def reset(self):
        self.background_music.stop()
        self.game_over_sound.stop()

    def hit(self):
        self.hit_sound.play()

    def power_up(self):
        self.power_up_sound.play()
    
    def power_down(self):
        self.power_down_sound.play()
    
    def walk(self):
        self.run_sound.play()
    
    def sekme(self):
        self.sekme_sound.play()
    
    def fırlat(self):
        self.fırlat_sound.play() # 4
    
    def ghost_hit(self):
        self.hit_ghost_sound.play()
    
    def ghost_dead(self):
        self.ghost_dead_sound.play() # 2
    
    def game_over(self):
        self.background_music.stop()
        self.game_over_sound.play()
    
    def exit(self):
        self.game_over_sound.set_volume(self.kıs1)
        self.kıs1 -= 0.75 * deltaTime

class Hell_hound():
    def __init__(self):
        self.hell_hound_ıdle_img = pygame.image.load("Assets\hell-hound\hell-hound-idle.png")
        self.hell_hound_jump_img = pygame.image.load("Assets\hell-hound\hell-hound-jump.png")
        self.hell_hound_run_img = pygame.image.load("Assets\hell-hound\hell-hound-run.png")
        self.hell_hound_walk_img = pygame.image.load("Assets\hell-hound\hell-hound-walk.png")

        self.img_h = self.hell_hound_ıdle_img.get_height()
        self.animation_speed = 100

        self.piksel = 64
        self.piksel_scale = self.piksel * 2
        self.action = 0
        self.timer = 0
        self.animation_speed = 100
        self.life_bar = 100
        self.pos_x = rnd.randint(100,1500) - self.img_h/2
        self.pos_y = rnd.randint(100,800) - self.img_h/2
        self.l_right = False

        # IDLE
        self.ıdle_frame = 6
        self.ıdle_frame_tut = 0
        self.ıdle_list = []
        for i in range(self.ıdle_frame):
            self.ıdle_list.append(self.get_hell_ıdle(i))
        for i in range(self.ıdle_frame):
            self.ıdle_list.append(self.get_hell_ıdle(5-i))
        # reverse
        self.hell_hound_ıdle_img = pygame.transform.flip(self.hell_hound_ıdle_img, self.l_right, False)
        self.ıdle_list_right = []
        for i in range(self.ıdle_frame):
            self.ıdle_list_right.append(self.get_hell_ıdle(i))
        for i in range(self.ıdle_frame):
            self.ıdle_list_right.append(self.get_hell_ıdle(5 - i))

        # WALK
        self.walk_frame = 12
        self.walk_frame_tut = 0
        self.walk_list = []
        for i in range(self.walk_frame):
            self.walk_list.append(self.get_hell_walk(i))
        # reverse
        self.hell_hound_walk_img = pygame.transform.flip(self.hell_hound_walk_img, self.l_right, False)
        self.walk_list_right = []
        for i in range(self.walk_frame_tut):
            self.walk_list_right.append(self.get_hell_walk(i))

        # RUN
        self.run_frame = 5
        self.run_frame_tut = 0
        self.run_list = []
        for i in range(self.run_frame):
            self.run_list.append(self.get_hell_run(i))
        # reverse
        self.hell_hound_run_img = pygame.transform.flip(self.hell_hound_run_img, self.l_right, False)
        self.run_list_right = []
        for i in range(self.run_frame):
            self.run_list_right.append(self.get_hell_run(i))

        # JUMP
        self.jump_frame = 6
        self.jump_frame_tut = 0
        self.jump_list = []
        for i in range(self.jump_frame):
            self.jump_list.append(self.get_hell_jump(i))
        # reverse 
        self.hell_hound_jump_img = pygame.transform.flip(self.hell_hound_jump_img, self.l_right, False)
        self.jump_list_right = []
        for i in range(self.jump_frame):
            self.jump_list_right.append(self.get_hell_jump(i))

    def update(self):
        if self.action == 0:
            self.draw_hell_ıdle(self.pos_x,self.pos_y)
        if self.action == 1:
            self.draw_hell_walk(self.pos_x,self.pos_y)
        if self.action == 2:
            self.draw_hell_run(self.pos_x,self.pos_y)

    def get_hell_ıdle(self, frame):
        image = pygame.Surface((self.piksel, self.piksel)).convert_alpha()
        image.blit(self.hell_hound_ıdle_img, (0,0), (self.piksel * frame, 0, self.piksel, self.piksel))
        image = pygame.transform.scale(image, (self.piksel_scale, self.piksel_scale))
        image.set_colorkey("black")
        return image

    def draw_hell_ıdle(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.animation_speed:
            self.ıdle_frame_tut +=1
            self.timer = pygame.time.get_ticks()
            if self.ıdle_frame_tut >= len(self.ıdle_list):
                self.ıdle_frame_tut = 0
                self.action = 0
        if self.l_right:
            ekran.blit(self.ıdle_list_right[self.ıdle_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.ıdle_list[self.ıdle_frame_tut], (pos_x, pos_y))

    def get_hell_walk(self, frame):
        image = pygame.Surface((self.piksel, self.piksel)).convert_alpha()
        image.blit(self.hell_hound_walk_img, (0,0), (self.piksel * frame, 0, self.piksel, self.piksel))
        image = pygame.transform.scale(image, (self.piksel_scale, self.piksel_scale))
        image.set_colorkey("black")
        return image
            
    def draw_hell_walk(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.animation_speed:
            self.walk_frame_tut +=1
            self.timer = pygame.time.get_ticks()
            if self.walk_frame_tut >= len(self.walk_list):
                self.walk_frame_tut = 0
                self.action = 0
        if self.l_right:
            ekran.blit(self.walk_list_right[self.walk_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.walk_list[self.walk_frame_tut], (pos_x, pos_y))
    
    def get_hell_run(self,frame):
        image = pygame.Surface((self.piksel, self.piksel)).convert_alpha()
        image.blit(self.hell_hound_run_img, (0,0), ((self.piksel + 5)  * frame, 0, self.piksel, self.piksel))
        image = pygame.transform.scale(image, (self.piksel_scale, self.piksel_scale))
        image.set_colorkey("black")
        return image

    def draw_hell_run(self,pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.animation_speed:
            self.run_frame_tut +=1
            self.timer = pygame.time.get_ticks()
            if self.run_frame_tut >= len(self.run_list):
                self.action = 0
                self.run_frame_tut = 0
        if self.l_right:
            ekran.blit(self.run_list_right[self.run_frame_tut], (pos_x, pos_y))
        else:
            ekran.blit(self.run_list[self.run_frame_tut], (pos_x, pos_y))

    def get_hell_jump(self, frame):
        image = pygame.Surface((self.piksel, self.piksel)).convert_alpha()
        image.blit(self.hell_hound_jump_img, (0,0), (self.piksel * frame, 0, self.piksel, self.piksel))
        image = pygame.transform.scale(image, (self.piksel_scale, self.piksel_scale))
        image.set_colorkey("black")
        return image

    def draw_hell_jump(self, pos_x, pos_y):
        if pygame.time.get_ticks() - self.timer >= self.animation_speed:
            self.jump_frame_tut += 1
            self.timer = pygame.time.get_ticks()
            if self.jump_frame_tut >= len(self.jump_list):
                self.action = 1
                self.jump_frame_tut = 0

class Main():
    def __init__(self):
        # EKRAN
        self.rect1 = pygame.Rect(448,448,4,4)
        self.pencere = pygame.Rect(0,0,900,900)

        # FADE EKRAN
        self.fade_surface = pygame.Surface((900,900), pygame.SRCALPHA)
        self.fade_bool = True
        self.set_fade_alpha = 256
        self.set_fade_alpha_vel = 128
        self.fade_sett = 2

        self.cursor_img = pygame.image.load("Assets\Cursor.png")
        self.cursor_img = pygame.transform.scale(self.cursor_img, (25,25))
        self.cursor_img = pygame.transform.flip(self.cursor_img, True, False)

        # FARE
        self.mouse_buttons = pygame.mouse.get_pressed()
        self.mouse_pos = [0,0]

        self.TF = [True, False]

        # FONT
        self.font = pygame.freetype.Font("Daydream.ttf", 48)
        self.font2 = pygame.freetype.Font("Daydream.ttf", 24)
        self.font3 = pygame.freetype.Font("Daydream.ttf", 8)
        self.text_y = 0
        self.text_vel = 60
        self.temp = 0

        # HİT POİNT AÇ KAPA (H)
        self.hit_point = False

        self.supriz = False

        self.sound = Sound()
        pygame.mixer.set_num_channels(64)
        # KARAKTER
        self.dude_vel = 200
        self.dude = Dude()
        self.dude.dude_vel = self.dude_vel

        self.yandın = False
        self.skor = 0

        self.zorluk = 1
        self.game_over_sound = False

        # SPAWNERLAR
        self.ghost_spawn = []
        self.hell_spawn = []
        self.rock_list = []
        self.fire_ball_list = []
        self.yemek_list = []

        # TİMERLAR VE ZORLUK DENGESİ
        self.gecen_timer = 1000
        self.gecen_time = 0
        self.gecen_sure = 0
        self.gecen_sure_tut = 0
        self.zorluk_arttır_timer = 15000 # 15 saniye
        self.zorluk_arttır_time = 0

        self.pecere_flick_timer = 100
        self.pencere_flic_time = 0

        self.ghost_timer = 1000
        self.ghost_time = 0
        self.ghost_vel = 54
        self.fire_range_max = 350
        self.fire_atıs_sayısı = 0
        self.fire_ball_vel = 300
        self.fire_ihtimal = 8

        self.rock_timer = 750
        self.rock_time = 0
        self.rock_vel = 600
        self.rock_damage = 25
        self.rock_sekme_sayisi = 0

        self.yemek_vel = 200
        self.yemek_timer = rnd.randint(2000,9000)
        self.yemek_time = 0
        
    def key_controller(self):
        self.mouse_buttons = pygame.mouse.get_pressed() # FARE TUŞLARI BASMA KONTROL
        if self.mouse_buttons[0] and not self.yandın: # TAŞ FIRLATMA # SOL TUŞ
            self.tas_fırlat()
        elif self.mouse_buttons[1] and not self.yandın: # ORTA TUŞ
            pygame.quit()
            sys.exit()
        elif self.mouse_buttons[2] and not self.yandın: # SAĞ TUŞ
            main.dude.get_dude_damage(100)

        for e in pygame.event.get(): # İNPUT KONTROLLERİ
            if e.type == pygame.QUIT:
                print("MİNİNM FPS : {}".format(minfps))
                pygame.quit()
                sys.exit()
            # KARAKTER HAREKET ETTİRME VE ÖZELLİKLER
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_h: # HİT POİNT AÇ-KAPA
                    self.hit_point = not self.hit_point
                if e.key == pygame.K_SPACE and self.yandın:
                    self.sound.reset()
                    main_sıfırla()
                if e.key == pygame.K_ESCAPE and self.yandın and not self.fade_bool:
                    self.fade_bool = True
                    self.set_fade_alpha = 0
                    self.fade_sett = 1
                if e.key == pygame.K_LSHIFT and main.dude.dude_shift > 10 and not self.yandın:
                    main.dude.dude_is_shift = True
                    main.dude.dude_dust_animation_frame_tut = 0
                if e.key == pygame.K_UP or e.key == pygame.K_w and not self.yandın:
                    self.dude.k_up = True
                    self.dude.dude_action = 1 
                if e.key == pygame.K_DOWN or e.key == pygame.K_s and not self.yandın:
                    self.dude.k_down = True
                    self.dude.dude_action = 1 
                if e.key == pygame.K_LEFT or e.key == pygame.K_a and not self.yandın:
                    self.dude.k_left = True
                    self.dude.l_left = True
                    self.dude.dude_action = 1 
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d and not self.yandın:
                    self.dude.k_right = True
                    self.dude.l_left = False
                    self.dude.dude_action = 1 
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LSHIFT and not self.yandın:
                    main.dude.dude_is_shift = False
                if e.key == pygame.K_UP or e.key == pygame.K_w and not self.yandın:
                    self.dude.k_up = False
                if e.key == pygame.K_DOWN or e.key == pygame.K_s and not self.yandın:
                    self.dude.k_down = False
                if e.key == pygame.K_LEFT or e.key == pygame.K_a and not self.yandın:
                    self.dude.k_left = False
                if e.key == pygame.K_RIGHT or e.key == pygame.K_d and not self.yandın:
                    self.dude.k_right = False

    def update(self):
        # ZORLUK ARTTIR
        if pygame.time.get_ticks() - self.zorluk_arttır_time >= self.zorluk_arttır_timer and not self.yandın:
            self.zorluk_arttır_time = pygame.time.get_ticks()
            self.zorluk += 1
            self.ghost_vel += 5
            self.yemek_vel += 20
            self.fire_atıs_sayısı += 1
            self.fire_range_max += 20
            self.ghost_timer -= 35
            self.rock_timer -= 40

            if self.rock_damage <= 5:
                self.rock_damage = 5
            else:
                self.rock_damage -= 3

            if self.fire_ihtimal <= 1:
                self.fire_ihtimal = 1
            else:
                self.fire_ihtimal -= 1
            
            if self.fire_atıs_sayısı >= 3:
                self.fire_atıs_sayısı = 3
            else:
                self.fire_atıs_sayısı += 1

        # KARAKTER GÜNCELLEME
        self.dude.update()
        
        # HAYALET GÜNCELLEME
        if not main.supriz:
            self.hayalet_olustur()
        if len(self.ghost_spawn) > 0:
            for x in self.ghost_spawn: # GHOST GÜNCELLEME
                x.update(self.dude.get_dude_position_x(), self.dude.get_dude_position_y())
                if x.ghost_rect.colliderect(self.dude.dude_rect): # GHOST İLDE DUDE ÇARPIŞMA
                    self.dude.get_dude_damage(x.crash_damage)
            for x in self.ghost_spawn:
                if x.dead: # GHOST SİLME
                    tut = self.ghost_spawn.index(x)
                    del self.ghost_spawn[tut] 
                    self.skor += 5
        # TAŞ GÜNCELLEME
        if len(self.rock_list) > 0:
            for x in self.rock_list: # ROCK GÜNCELLEME
                x.update()
                for z in self.ghost_spawn: # ROCK İLE GHOST ÇARPIŞMA ALGILAMA
                    if x.rock_rect.colliderect(z.ghost_rect):
                        vuruldumu = False
                        for c in x.rock_vurulanlar: # ROCK VE GHOST DAHA ÖNCE ÇARPIŞTI MI KONTROL ETME
                            if z == c:
                                vuruldumu = True
                        if not vuruldumu:
                            z.ghost_get_damage(x.rock_damage)
                            x.rock_vurulanlar.append(z)
                if (x.rock_x > 910 or x.rock_x < -10) or (x.rock_y > 910 or x.rock_y < -10): # TAŞ SİLME
                    tut = self.rock_list.index(x)
                    del self.rock_list[tut]
        # YEMEK GÜNCELLEME
        self.yemek_olustur()
        if len(self.yemek_list) > 0:
            for x in self.yemek_list:
                x.update()
                if x.yemek_rect.colliderect(self.dude.dude_rect):
                    x.yendi_mi = True
                    x.secim_yap()
            for x in self.yemek_list:
                if x.yendi_mi:
                    tut = self.yemek_list.index(x)
                    del self.yemek_list[tut] 
                    self.skor += 2
            for x in self.yemek_list:
                if x.yok_ol:
                    tut = self.yemek_list.index(x)
                    del self.yemek_list[tut] 
        # FİRE-BALL GÜNCELLEME
        if len(self.fire_ball_list) > 0:
            for x in self.fire_ball_list:
                x.update()
                if x.fire_rect.colliderect(main.dude.dude_rect):
                    self.dude.get_dude_damage(x.fire_damage)
                    x.yok_ol = True
            for x in self.fire_ball_list:
                if x.yok_ol == True:
                    tut = self.fire_ball_list.index(x)
                    del self.fire_ball_list[tut]
        # PENCERE VE TEXT AYARLARI
        if pygame.time.get_ticks() - self.gecen_time >= main.gecen_timer: # SÜRE
            self.gecen_time = pygame.time.get_ticks()
            self.gecen_sure += 1
        if not self.yandın:
            self.panele_yazdır(self.font2,"SKOR:{0} - ZORLUK:{2} -- {1} ".format(self.skor, self.gecen_sure, self.zorluk), (255, 250, 255), (250, 45), True)

        if self.dude.x == 900 or self.dude.x == 0 or self.dude.y == 900 or self.dude.y == 0 or self.dude.dead:
            if pygame.time.get_ticks() - main.pencere_flic_time >= self.pecere_flick_timer:
                pygame.draw.rect(ekran, (255,0,0), self.pencere, 5)
                main.pencere_flic_time = pygame.time.get_ticks()
            if self.yandın:# YANMA EKRANI
                self.yemek_timer = 100
                self.yemek_olustur()

                if len(self.ghost_spawn) < 30:
                    main.supriz = True
                    self.ghost_timer = 100
                    self.hayalet_olustur(True)

                if self.text_y > 0:
                    self.temp -= 1
                else:
                    self.temp += 1

                self.text_y += (self.text_vel + self.temp) * deltaTime

                if abs(self.text_y) >= 100:
                    self.text_vel *= -1
                    self.temp *= -1
                # YANMA TABLOSU
                #                    FONT     MESAJ       RENK           POS                GOLGE
                self.panele_yazdır(self.font,"YANDIN", (255,0,0), (450, 310 + self.text_y), True)
                self.panele_yazdır(self.font,"SKOR : {}".format(self.skor), (255,255,255), (450, 410 + self.text_y), True)
                self.panele_yazdır(self.font,"GECEN SURE : {}".format(self.gecen_sure_tut), (255,255,255), (450, 510 + self.text_y), True)
                self.panele_yazdır(self.font2,"Space to Restart", (0,191,255), (250, 610 + self.text_y),True)
                self.panele_yazdır(self.font2,"Esc To Quit", (0,191,255), (650, 610 + self.text_y), True)

        # FADE EKRAN
        if self.fade_bool:
            if self.fade_sett == 1: # FADE KAPAT
                self.set_fade_alpha += self.set_fade_alpha_vel * deltaTime
                self.fade_surface.set_alpha(self.set_fade_alpha)
                self.fade_surface.fill((0,0,0))
                ekran.blit(self.fade_surface,(0,0))
                main.sound.exit()
                if self.set_fade_alpha >= 256:
                    pygame.quit()
                    sys.exit()
            elif self.fade_sett == 2: # FADE AÇ
                self.set_fade_alpha -= self.set_fade_alpha_vel * deltaTime
                self.fade_surface.set_alpha(self.set_fade_alpha)
                self.fade_surface.fill((0,0,0))
                ekran.blit(self.fade_surface,(0,0))
                if self.set_fade_alpha <= 0:
                    self.set_fade_alpha = 0
                    self.fade_sett = 0
                    self.fade_bool = False
                    
        # FARE TAKİP ETME
        ekran.blit(self.cursor_img, (self.mouse_pos[0], self.mouse_pos[1]))

        # KARAKTER ORTA NOKTASI
        #pygame.draw.rect(ekran, (255,255,255), (self.dude.x-2, self.dude.y-2, 4,4))
        # EKRANIN ORTA NOKTASI
        #pygame.draw.rect(ekran, (255,0,0), self.rect1)
    
    def set_dude_vel(self, artıs): self.dude.dude_vel += artıs

    def tas_fırlat(self):
        if pygame.time.get_ticks() - self.rock_time >= self.rock_timer:
            self.rock_time = pygame.time.get_ticks()
            if self.dude.is_running: 
                self.dude.dude_action = 2
                self.dude.dude_run_throw_animation_frame_tut = 0
            else:
                self.dude.dude_action = 3
                self.dude.dude_throw_animation_frame_tut = 0
            self.rock_list.append(Dude_Rock(self.mouse_pos[0], self.mouse_pos[1]))
            self.sound.fırlat()

    def hayalet_olustur(self, supriz_tut=False):
        if pygame.time.get_ticks() - self.ghost_time >= self.ghost_timer: # GHOST OLUŞTURMA SIKLIĞI
            self.ghost_time = pygame.time.get_ticks()
            if main.supriz and supriz_tut:
                temp = Ghost()
                temp.random_pos_ver()
                temp.l_right = choice(self.TF)
                self.ghost_spawn.append(temp)
            else:
                self.ghost_spawn.append(Ghost())

    def yemek_olustur(self):
        if pygame.time.get_ticks() - self.yemek_time >= self.yemek_timer:
            self.yemek_time = pygame.time.get_ticks()
            self.yemek_list.append(Yemek())
            self.yemek_timer = rnd.randint(2000,9000)

    def dude_spec_yazdır(self):
        print("Dude Hız :{} -- Taş Sekme Sayısı :{}".format(main.dude.dude_vel, main.rock_sekme_sayisi))

    def panele_yazdır(self, font='font', yazi="bos", renk=(255,255,255), pos=[0,0], golge=False):
        # GÖLGE
        if golge:
            text_surface, rect = font.render("{}".format(yazi), (0,0,0))
            ekran.blit(text_surface, (pos[0] - rect.right/2 + 5, pos[1] - rect.y + 5))
        # YAZI
        text_surface, rect = font.render("{}".format(yazi), renk)
        ekran.blit(text_surface, (pos[0] - rect.right/2, pos[1] - rect.y))

    def Karart(self):
        pass        

    def Reset(self):
        self.sound.reset()
        main_sıfırla()

pygame.init()
ekran = pygame.display.set_mode((900,900))
clock = pygame.time.Clock()
pygame.mouse.set_visible(False)

# MAİNİ RESETLEYEREK OYUNA RESET ATMA
def main_sıfırla():
    global main
    main = Main()
    choice_bg()
    
def choice_bg():
    global background
    background = pygame.image.load("Assets/background/Ground{}.png".format(rnd.randint(0,5))).convert()

choice_bg()# RANDOM ARKA PLAN SEÇ
main_sıfırla()# MAİN BAŞLATMA

getTicksLastFrame = 0
deltaTime = 0
minfps = 500

last_time = 0
fps = 0
dT = 0

run = True
while run:
    # ARKAPLAN RENGİ
    ekran.blit(background, (0,0))
    #ekran.fill((42,42,42))
    if fps < minfps and fps != 0:
        minfps = fps

    # GÖSTERGELER
    if pygame.time.get_ticks() - last_time >=200:
        last_time = pygame.time.get_ticks()
        fps = int(clock.get_fps())
        dT = deltaTime
    
    pygame.draw.rect(ekran, (0,0,0), (0,860,100,50))# GÖSTERGE ARKAPLANI
    main.panele_yazdır(main.font3,"FPS:{}".format(fps),(255, 255, 255), (50, 875), False)
    main.panele_yazdır(main.font3,"GEC:{}".format(dT),(255, 255, 255), (50, 890), False)
    
    #print(clock.get_fps())
    t = pygame.time.get_ticks()
    # deltaTime in seconds.
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t
    
    main.key_controller()
    main.update()

    main.mouse_pos = pygame.mouse.get_pos()

    # EKRAN YENİLEME VE FPS
    pygame.display.update()
    clock.tick()