import math
import pygame
import random
import copy

pygame.init()
screen = pygame.display.set_mode((1280, 660))
clock = pygame.time.Clock()
font = pygame.font.SysFont("Times New Roman", 20)
gravity = 0.005
change = 20
mouse_holding = False


class Slider:
    def __init__(self, position, length, range, color, name, start = 0, step = 0):
        self.position = position
        self.length = length
        self.end_pos = (self.position[0] + self.length, self.position[1])
        self.range = range
        self.step = step
        self.color = color
        font = pygame.font.SysFont("Times New Roman", 12)
        self.name = font.render(name, False, self.color)
        self.slider_pos = start
        self.namepos = (self.position[0], self.position[1] + 5)
        self.valpos = (self.position[0] + self.length + 1, self.position[1] - 2)

    def dot_pos(self):
        dot_pos = (self.position[0] + self.slider_pos, self.position[1])
        return dot_pos

    def value(self):
        font = pygame.font.SysFont("Times New Roman", 12)
        val = font.render(str(round(((self.slider_pos / self.length) * (self.range[1] - self.range[0])) + self.range[0], 2)), False, self.color)
        return val

    def realval(self):
        val = (((self.slider_pos) / self.length) * (self.range[1] - self.range[0])) + self.range[0]
        return val

    def draw_update(self):
        global mouse_click
        screen.blit(self.name, self.namepos)
        screen.blit(self.value(), self.valpos)
        pygame.draw.line(screen, self.color, self.position, self.end_pos, 2)
        pygame.draw.circle(screen, self.color, self.dot_pos(), 6)
        if mouse_click and self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.length and self.position[1] - 5 < pygame.mouse.get_pos()[1] < self.position[1] + 5:
            self.slider_pos = pygame.mouse.get_pos()[0] - self.position[0]


class Switcher:
    def __init__(self, position, values, color, name, start_val = 0):
        self.num_of_vals = len(values)
        self.color = color
        font = pygame.font.SysFont("Times New Roman", 12)
        self.valfont = pygame.font.SysFont("Times New Roman", 12)
        self.values = values
        self.curr_val = start_val
        self.val_rend = self.valfont.render(values[self.curr_val], False, self.color)
        self.name = font.render(name, False, self.color)
        self.position = position
        self.tex_pos = (self.position[0] - 6, self.position[1] + 8)
        self.valpos = (self.position[0] + 6 * (self.num_of_vals - 1) + 7, self.position[1] - 6)
        self.rectpos = (self.position[0], self.position[1] - 6)

    def switch(self):
        global mouse_click_2
        mouspos = pygame.mouse.get_pos()
        if mouse_click_2 and self.position[0] - 6 < mouspos[0] < self.position[0] + (6 * self.num_of_vals) and self.position[1] - 6 < mouspos[1] < self.position[1] + 6:
            if self.curr_val < self.num_of_vals - 1:
                self.curr_val += 1
                self.val_rend = self.valfont.render(self.values[self.curr_val], False, self.color)
            elif self.curr_val == self.num_of_vals - 1:
                self.curr_val = 0
                self.val_rend = self.valfont.render(self.values[self.curr_val], False, self.color)

    def display(self):
        pygame.draw.circle(screen, self.color, self.position, 6)
        pygame.draw.circle(screen, self.color, (self.position[0] + 6 * (self.num_of_vals - 1), self.position[1]), 6)
        pygame.draw.rect(screen, self.color, [self.rectpos[0], self.rectpos[1], 6 * (self.num_of_vals - 1), 12])
        pygame.draw.circle(screen, (0, 0, 0), (self.position[0] + 6 * self.curr_val, self.position[1]), 5)
        screen.blit(self.name, self.tex_pos)
        screen.blit(self.val_rend, self.valpos)


class Button:
    def __init__(self, position, color, name, toggle = False, pressed = False):
        self.color = color
        self.font = pygame.font.SysFont("Times New Roman", 12)
        self.name = self.font.render(name, False, (0, 0, 0))
        self.position = position
        self.tex_pos = (self.position[0], self.position[1])
        self.rectpos = (self.position[0], self.position[1])
        self.toggle = toggle
        self.pressed = pressed

    def draw(self):
        color = self.color
        if self.pressed == True:
            color = (self.color[0] - 35, self.color[1] - 35, self.color[2] - 35)
        elif self.pressed == False:
            color = self.color
        pygame.draw.circle(screen, color, (self.position[0], self.position[1] + 7), 7)
        pygame.draw.circle(screen, color, (self.position[0] + self.name.get_width(), self.position[1] + 7), 7)
        pygame.draw.rect(screen, color, [self.rectpos[0] - 1, self.rectpos[1] - 1, self.name.get_width() + 2, self.name.get_height() + 2])
        screen.blit(self.name, self.tex_pos)

    def get_mouse_hover(self):
        if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.name.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.name.get_height():
            return True
        else:
            return False

    def click(self):
        if self.pressed == True and self.toggle == False:
            self.pressed = False
        if self.position[0] < pygame.mouse.get_pos()[0] < self.position[0] + self.name.get_width() and self.position[1] < pygame.mouse.get_pos()[1] < self.position[1] + self.name.get_height() and mouse_click_2:
            if self.toggle == True:
                self.pressed = not self.pressed
            elif self.toggle == False and self.pressed == False:
                self.pressed = True


class Lightsource:
    def __init__(self, intensity, position, angle, on_screen, affect_move = True):
        self.affect_move = affect_move
        self.position = position
        self.on_screen = on_screen
        self.intensity = intensity
        self.on_image = pygame.transform.rotate(pygame.image.load("litlamp.png"), angle)
        self.off_image = pygame.transform.rotate(pygame.image.load("offlamp.png"), angle)
        self.on_status = False
        self.move_intensity = intensity * 20

    def get_clicked(self):
        if self.position[0] + 100 < pygame.mouse.get_pos()[0] < self.position[0] + self.on_image.get_width() and self.position[1] + 20 < pygame.mouse.get_pos()[1] < self.position[1] + self.on_image.get_height() - 20 and mouse_click_2 and self.on_screen:
            self.on_status = not self.on_status
            return True
        else:
            return False

    def draw(self):
        if self.on_screen == False:
            pass
        elif self.on_status == True:
            screen.blit(self.on_image, self.position)
        elif self.on_status == False:
            screen.blit(self.off_image, self.position)

    def update(self):
        self.draw()
        self.get_clicked()


colortype = 0
density = 500
walls_remove_temp = False


class Particle(pygame.sprite.Sprite):
    conductivity = .08
    connection_strength = 2000
    flex = False

    def __init__(self, xvelocity, yvelocity, volume, con_streng, connections, con_tar_lengs, position, id, temperature, pin, material_factor = .000002, beingheld = False, istemp = False):
        super().__init__()
        global density
        self.position = position
        self.pin = pin
        self.target_position = position
        self.color = (255, 255, 255)
        self.image = pygame.Surface([5, 5])
        self.rect = self.image.get_rect()
        self.rect.center = [position[0], position[1]]
        self.xvelocity = xvelocity
        self.yvelocity = yvelocity
        self.volume = volume
        self.radius = math.sqrt(math.pi * self.volume) / 2
        self.density = density
        self.defpos = position
        self.connections = connections
        self.mass = volume * density
        self.id = id
        self.temperature = temperature
        self.con_tar_lengs = con_tar_lengs
        self.temp_factor = (self.temperature + 273) * 2
        self.being_held = beingheld
        self.mat_factor = material_factor
        self.istemp = istemp
        self.selected = False


    def collide(self, collider):
        col = pygame.sprite.collide_rect(self, collider)
        return col

    def shallow_update(self):
        self.rect.center = self.position
        temp_color = self.color
        if colortype == 0:
            if self.temperature < 0:
                part_diff = 255 / abs(self.temperature)
                if part_diff > 255:
                    part_diff = 255
                if part_diff < 0:
                    part_diff = 0
                temp_color = (part_diff, part_diff, 255)
            if self.temperature > 0:
                part_diff = 255 / self.temperature
                if part_diff > 255:
                    part_diff = 255
                if part_diff < 0:
                    part_diff = 0
                temp_color = (255, part_diff, part_diff)
        elif colortype == 1:
            temp_scale = (20900 / ((self.temperature + 273) + 19))
            blue = ((-1 / 19) * (temp_scale ** 2)) + 550
            green = ((-1 / 19) * (temp_scale ** 2)) + (7.5 * temp_scale) - 5
            red = ((-1 / 19) * (temp_scale ** 2)) + (10.9 * temp_scale) - 230
            if red < 0 and self.temperature > 2700:
                red = ((-1 / 39) * (temp_scale ** 2)) - (10.9 * temp_scale) - 230
            if blue < 40:
                blue = 40
            if green < 40:
                green = 40
            if red < 40:
                red = 40
            if blue > 255:
                blue = 255
            if green > 255:
                green = 255
            if red > 255:
                red = 255
            temp_color = (red, green, blue)
        elif colortype == 2:
            red = (abs(self.xvelocity) + 1) * 55
            blue = (abs(self.yvelocity) + 1) * 55
            green = ((abs(self.xvelocity) * abs(self.xvelocity / 2))) * 25
            if blue <= 10:
                blue = 10
            if green <= 10:
                green = 10
            if red <= 10:
                red = 10
            if blue >= 255:
                blue = 255
            if green >= 255:
                green = 255
            if red >= 255:
                red = 255
            temp_color = (red, green, blue)
        else:
            temp_color = (0, 0, 0)
        self.show_temp(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        self.position = self.target_position
        mouse_position = pygame.mouse.get_pos()
        if self.position[0] - math.sqrt(math.pi * self.volume) < mouse_position[0] < self.position[0] + math.sqrt(math.pi * self.volume) and self.position[1] - math.sqrt(math.pi * self.volume) < mouse_position[1] < self.position[1] + math.sqrt(math.pi * self.volume) and mouse_click_2:
            self.selected = not self.selected
        if self.selected:
            temp_color = (0, 255, 0)
        pygame.draw.circle(screen, temp_color, self.position, self.radius)

    def get_point_circ_tar(self, current_con, point=(0, 0)):
        g = point[0] - self.position[0]
        h = point[1] - self.position[1]
        b = 90
        if g == 0:
            if h > 0:
                b = 90
            elif h <= 0:
                b = -90
        elif h == 0:
            if g < 0:
                b = -180
            elif g >= 0:
                b = 0
        elif g != 0:
            s = h / g
            b = math.atan(s)
        if current_con == 0:
            d = 10 * math.cos(b)
            f = 10 * math.sin(b)
        else:
            d = self.con_tar_lengs[self.connections.index(current_con.id)] * math.cos(b)
            f = self.con_tar_lengs[self.connections.index(current_con.id)] * math.sin(b)
        if g < 0:
            d = -d
            f = -f
        return [d - g, f - h]

    def update(self):
        if gravity != 0:
            self.yvelocity += gravity
        self.rect.center = self.position
        temp_color = self.color
        self.conduct_temperature()
        if colortype == 0:
            if self.temperature < 0:
                part_diff = 255 / abs(self.temperature)
                if part_diff > 255:
                    part_diff = 255
                if part_diff < 0:
                    part_diff = 0
                temp_color = (part_diff, part_diff, 255)
            if self.temperature > 0:
                part_diff = 255 / self.temperature
                if part_diff > 255:
                    part_diff = 255
                if part_diff < 0:
                    part_diff = 0
                temp_color = (255, part_diff, part_diff)
        elif colortype == 1:
            temp_scale = (20900 / ((self.temperature + 273) + 19))
            blue = ((-1 / 19) * (temp_scale ** 2)) + 550
            green = ((-1 / 19) * (temp_scale ** 2)) + (7.5 * temp_scale) - 5
            red = ((-1 / 19) * (temp_scale ** 2)) + (10.9 * temp_scale) - 230
            if red < 0 and self.temperature > 2700:
                red = ((-1 / 39) * (temp_scale ** 2)) - (10.9 * temp_scale) - 230
            if blue < 40:
                blue = 40
            if green < 40:
                green = 40
            if red < 40:
                red = 40
            if blue > 255:
                blue = 255
            if green > 255:
                green = 255
            if red > 255:
                red = 255
            temp_color = (red, green, blue)
        elif colortype == 2:
            red = (abs(self.xvelocity) + 1) * 55
            blue = (abs(self.yvelocity) + 1) * 55
            green = ((abs(self.xvelocity) * abs(self.xvelocity / 2))) * 25
            if blue <= 10:
                blue = 10
            if green <= 10:
                green = 10
            if red <= 10:
                red = 10
            if blue >= 255:
                blue = 255
            if green >= 255:
                green = 255
            if red >= 255:
                red = 255
            temp_color = (red, green, blue)
        else:
            temp_color = (0, 0, 0)
        if vibrate == True:
            self.vibrate()
        else:
            self.position = self.target_position
        if self.pin == False:
            self.move_based_on_vel()
        elif self.pin == True:
            self.xvelocity = 0
            self.yvelocity = 0
            self.pin = True
            self.position = self.defpos
        self.show_temp(pygame.mouse.get_pos(), pygame.mouse.get_pressed(3))
        if self.temperature < -273:
            self.temperature = -273
        self.temp_factor = (self.temperature - 29) * self.mat_factor
        self.color = temp_color
        try:
            pygame.draw.circle(screen, temp_color, self.position, self.radius)
        except:
            pygame.draw.circle(screen, (30, 30, 30), self.position, self.radius)

    def get_all_positions(self):
        positions = []
        cyc = 0
        while cyc < len(particle_list):
            if self.position[0] - 5 < particle_list[cyc].position[0] < self.position[0] + 5 and self.position[1] - 5 < particle_list[cyc].position[1] < self.position[1] + 5:
                positions.append(particle_list[cyc].id)
            else:
                positions.append(particle_list[cyc].position)
            cyc += 1
        return positions

    def get_distance(self, point):
        pos = self.position
        try:
            dist = math.sqrt((((pos[0] - point[0])) ** 2) + (((pos[1] - point[1])) ** 2))
        except:
            dist = .001
        return dist

    def conduct_temperature(self):
        selftemp = self.temperature
        cons = self.connections
        going_through = 0
        total_loss = 0
        blocking_light = False
        total_x_move = 0
        total_y_move = 0
        x_dist = 0
        y_dist = 0
        while going_through < len(cons) and not self.istemp:
            try:
                current_con = old_list[cons[going_through]]
            except:
                current_con = particle_list[cons[going_through]]
            current_contemp = current_con.temperature
            x_vel_dif = 0
            y_vel_dif = 0
            if self.xvelocity > current_con.xvelocity:
                x_vel_dif = self.xvelocity - current_con.xvelocity
            elif self.xvelocity < current_con.xvelocity:
                x_vel_dif = current_con.xvelocity - self.xvelocity
            if self.yvelocity > current_con.yvelocity:
                y_vel_dif = self.yvelocity - current_con.yvelocity
            elif self.yvelocity < current_con.yvelocity:
                y_vel_dif = current_con.yvelocity - self.yvelocity
            if current_con.connections.count(self.id) == 1 and cons.count(current_con.id) == 1:
                if self.flex == True:
                    if self.position[1] > current_con.position[1]:
                        y_dist = self.position[1] - current_con.position[1]
                    elif self.position[1] < current_con.position[1]:
                        y_dist = current_con.position[1] - self.position[1]
                    if y_dist == self.con_tar_lengs[self.connections.index(current_con.id)]:
                        pass
                    elif y_dist < self.con_tar_lengs[self.connections.index(current_con.id)]:
                        if self.position[1] < current_con.position[1]:
                            dist_to_tar = self.con_tar_lengs[self.connections.index(current_con.id)] - y_dist
                            total_y_move -= ((dist_to_tar ** 1.1) / (self.mass))
                            total_y_move -= y_vel_dif / self.connection_strength
                            current_con.xvelocity += y_vel_dif / self.connection_strength
                        elif self.position[1] > current_con.position[1]:
                            dist_to_tar = self.con_tar_lengs[self.connections.index(current_con.id)] - y_dist
                            total_y_move += ((dist_to_tar ** 1.1) / (self.mass))
                            total_y_move -= y_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity += y_vel_dif / math.sqrt(self.connection_strength)
                    elif y_dist > self.con_tar_lengs[self.connections.index(current_con.id)]:
                        if self.position[1] < current_con.position[1]:
                            dist_to_tar = y_dist - self.con_tar_lengs[self.connections.index(current_con.id)]
                            total_y_move += ((dist_to_tar ** 1.1) / (self.mass))
                            total_y_move += y_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity -= y_vel_dif / math.sqrt(self.connection_strength)
                        elif self.position[1] > current_con.position[1]:
                            dist_to_tar = y_dist - self.con_tar_lengs[self.connections.index(current_con.id)]
                            total_y_move -= ((dist_to_tar ** 1.1) / (self.mass))
                            total_y_move += y_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity -= y_vel_dif / math.sqrt(self.connection_strength)
                    if self.position[0] > current_con.position[0]:
                        x_dist = self.target_position[0] - current_con.position[0]
                    elif self.position[0] < current_con.position[0]:
                        x_dist = current_con.position[0] - self.target_position[0]
                    if abs(x_dist) == self.con_tar_lengs[self.connections.index(current_con.id)]:
                        pass
                    elif x_dist < self.con_tar_lengs[self.connections.index(current_con.id)]:
                        if self.position[0] < current_con.position[0]:
                            dist_to_tar = (self.con_tar_lengs[self.connections.index(current_con.id)] - x_dist)
                            total_x_move -= ((dist_to_tar ** 1.1)) / (self.mass)
                            total_x_move -= x_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity += x_vel_dif / math.sqrt(self.connection_strength)
                        elif self.position[0] > current_con.position[0]:
                            dist_to_tar = self.con_tar_lengs[self.connections.index(current_con.id)] - x_dist
                            total_x_move += ((dist_to_tar ** 1.1) / (self.mass))
                            total_x_move -= x_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity += x_vel_dif / math.sqrt(self.connection_strength)
                    elif x_dist > self.con_tar_lengs[self.connections.index(current_con.id)]:
                        if self.position[0] < current_con.position[0]:
                            dist_to_tar = x_dist - self.con_tar_lengs[self.connections.index(current_con.id)]
                            total_x_move += ((dist_to_tar ** 1.1) / (self.mass))
                            total_x_move += x_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity -= x_vel_dif / math.sqrt(self.connection_strength)
                        elif self.position[0] > current_con.position[0]:
                            dist_to_tar = x_dist - self.con_tar_lengs[self.connections.index(current_con.id)]
                            total_x_move -= ((dist_to_tar ** 1.1) / (self.mass))
                            total_x_move += x_vel_dif / math.sqrt(self.connection_strength)
                            current_con.xvelocity -= x_vel_dif / math.sqrt(self.connection_strength)
                if self.flex == False:

                    dist = self.get_distance(current_con.target_position)
                    distances = self.get_point_circ_tar(current_con, current_con.target_position)
                    if (400 * self.temp_factor) > 0:
                        total_x_move -= ((distances[0] * dist) * (self.connection_strength + current_con.connection_strength) / 2) / (600 * (self.connection_strength + current_con.temp_factor) / 2)
                        current_con.xvelocity += ((distances[0] * dist) * (self.connection_strength + current_con.connection_strength) / 2) / (600 * (self.connection_strength + current_con.temp_factor) / 2)
                        total_y_move -= ((distances[1] * dist) * (self.connection_strength + current_con.connection_strength) / 2) / (600 * (self.connection_strength + current_con.temp_factor) / 2)
                        current_con.yvelocity += ((distances[1] * dist) * (self.connection_strength + current_con.connection_strength) / 2) / (600 * (self.connection_strength + current_con.temp_factor) / 2)
                    else:
                        self.position = (distances[0] + self.position[0], distances[1] + self.position[1])
                        current_con.position = (self.position[0] - distances[0], self.position[1] - distances[0])
                        totx = self.xvelocity + current_con.xvelocity
                        toty = self.yvelocity + current_con.yvelocity
                        self.xvelocity = totx / 2
                        current_con.xvelocity = -totx / 2
                        self.yvelocity = toty / 2
                        current_con.yvelocity = -toty / 2

                if current_con.target_position[0] > self.target_position[0] and current_con.target_position[1] - 5 < self.target_position[1] < current_con.target_position[1] + 5:
                    blocking_light = True
                if current_contemp == self.temperature:
                    pass
                elif current_contemp < self.temperature:
                    difference = selftemp - current_contemp
                    rate = self.conductivity * difference
                    current_con.temperature += rate
                    total_loss -= rate
                elif current_contemp > self.temperature:
                    difference = current_contemp - selftemp
                    rate = self.conductivity * difference
                    current_con.temperature -= rate
                    total_loss += rate
                if self.temperature > self.connection_strength or self.get_distance(current_con.position) > self.connection_strength:
                    self.connections.pop(going_through)
                    if current_con.connections.count(self.id) > 0:
                        current_con.connections.remove(self.id)
                    self.yvelocity += random.random() - .5
                    self.xvelocity += random.random() - .5
                    going_through -= 1
            else:
                cons.remove(current_con.id)
            going_through += 1
        if len(self.connections) == 0:
            total_loss = 0
        if self.get_dist_to_light_source(light) > 0 and not blocking_light and light.on_status == True:
            total_loss += (1 / math.sqrt(self.get_dist_to_light_source(light))) * light.intensity
            if light.affect_move:
                total_x_move -= ((1 / math.sqrt(self.get_dist_to_light_source(light))) * (abs(light.move_intensity) / self.mass))
        if self.position[1] > 0 and not blocking_light and light_2.on_status == True and light_2.on_screen:
            total_loss += (1 / math.sqrt(self.position[1] - (light.position[1] + 100))) * light_2.intensity
            total_y_move -= ((1 / math.sqrt(self.position[1] - (light.position[1] + 100))) * (abs(light_2.move_intensity) / self.mass))
        self.xvelocity += total_x_move
        self.yvelocity += total_y_move
        self.temperature = selftemp + total_loss    # TODO: make it so that when drawing dots, if two dots overlap it will add those connections to each dot. this way, it will conduct, but if the temperature is too high the connection will sever again
        col_cycle = 0
        while col_cycle < len(particle_list):
            curr_compare = particle_list[col_cycle]
            if curr_compare.id != self.id:
                if self.get_distance(curr_compare.position) < self.radius + curr_compare.radius and self.temperature > 40:
                    self.connections.append(curr_compare.id)
                    self.con_tar_lengs.append(self.get_distance(curr_compare.position) * 2.5)
                    curr_compare.connections.append(self.id)
                    curr_compare.con_tar_lengs.append(curr_compare.get_distance(self.position) * 2.5)
                if self.radius < self.get_distance(curr_compare.position) < self.radius + curr_compare.radius and self.temperature <= 40:
                    distances = self.get_point_circ_tar(0, curr_compare.target_position)
                    self.position = (distances[0] + self.position[0], distances[1] + self.position[1])
                    curr_compare.position = (self.position[0] - distances[0], self.position[1] - distances[0])
                    totvel = self.xvelocity + curr_compare.xvelocity + self.yvelocity + curr_compare.yvelocity
                    self.xvelocity = -math.sqrt(abs(totvel)) * distances[0] / 5
                    curr_compare.xvelocity = math.sqrt(abs(totvel)) * distances[0] / 5
                    self.yvelocity = -math.sqrt(abs(totvel)) * distances[1] / 5
                    curr_compare.yvelocity = math.sqrt(abs(totvel)) * distances[1] / 5
            col_cycle += 1

    def show_temp(self, mouse_position, mousedown):
        global mouse_holding
        if self.position[0] - math.sqrt(math.pi * self.volume) < mouse_position[0] < self.position[0] + math.sqrt(math.pi * self.volume) and self.position[1] - math.sqrt(math.pi * self.volume) < mouse_position[1] < self.position[1] + math.sqrt(math.pi * self.volume):
            temp_text = font.render(str((self.temperature)), True, (250, 250, 250))
            screen.blit(temp_text, (50, 620))
            if not self.istemp:
                if mousedown[0] == True:
                    if mouse_holding == False:
                        self.being_held = True
                        mouse_holding = True
                    elif mouse_holding and not self.being_held:
                        self.being_held = False
                elif mousedown[0] == False:
                    mouse_holding = False
                    self.being_held = False
                if mousedown[2] == True and self.temperature > -273:
                    self.temperature += change
            else:
                if mousedown[0] == True:
                    if mouse_holding == True:
                        self.being_held = False
                        mouse_holding = False
        if self.temperature < -273:
            self.temperature = -273
        if self.being_held == True:
            mouse_holding = True
            self.xvelocity = 0
            self.yvelocity = 0
            self.target_position = mouse_position

    def vibrate(self):
        particle_rand_y = self.target_position[1] + random.randint(round((-1 * ((abs(self.temperature + 273)) ** .8) / 400)), round(((self.temperature + 273) ** 1.1 / 400)))
        particle_rand_x = self.target_position[0] + random.randint(round((-1 * ((abs(self.temperature + 273)) ** .8) / 400)), round(((self.temperature + 273) ** 1.1 / 400)))
        self.position = (particle_rand_x, particle_rand_y)

    def move_based_on_vel(self):
        new_tarx = self.target_position[0]
        new_tary = self.target_position[1]
        if 10 < new_tary < 640:
            new_tary += self.yvelocity
        elif new_tary > 640 or new_tary < 10:
            self.yvelocity = self.yvelocity * -wall_bounciness
            self.xvelocity = self.xvelocity * .9
            if walls_remove_temp == True:
                realtemp = self.temperature + 273
                self.temperature = (realtemp * .8) - 273
            if new_tary > 640:
                new_tary = 639
            if new_tary < 10:
                new_tary = 11

        if 10 < new_tarx < 1270:
            new_tarx += self.xvelocity
        elif new_tarx > 1270 or new_tarx < 10:
            self.xvelocity = self.xvelocity * -wall_bounciness
            self.yvelocity = self.yvelocity * .9
            if walls_remove_temp == True:
                realtemp = self.temperature + 273
                self.temperature = (realtemp * .8) - 273
            if new_tarx > 1270:
                new_tarx = 1269
            if new_tarx < 10:
                new_tarx = 11
        if -0.001 < self.xvelocity < 0.001:
            self.xvelocity = 0
        if -0.001 < self.yvelocity < 0.001:
            self.yvelocity = 0
        self.target_position = (new_tarx, new_tary)

    def get_dist_to_light_source(self, light_source):
        dist = light_source.position[0] + 100 - self.target_position[0]
        if dist < 0:
            dist = 0
        return dist

    def copy(self):
        new_copy = Particle(self.xvelocity, self.yvelocity, self.volume, self.density, self.connections, self.con_tar_lengs, self.target_position, self.id, self.temperature, self.pin, self.mat_factor, self.being_held)
        return new_copy

class Structure_menu:
    def __init__(self):
        self.connection_strength_slide = Slider((180, 150), 100, (10, 2000), (255, 255, 255), "Bond Strength")
        self.connect_button = Button((180, 180), (255, 255, 255), "Connect Selected")
        self.start_temp_slide = Slider((180, 210), 100, (-270, 2000), (255, 255, 255), "Starting Temperature")
        self.add_button = Button((180, 240), (255, 255, 255), "Add New Particle")
        self.place_button = Button((180, 270), (255, 255, 255), "Place Structure")
        self.save_button = Button((180, 270), (255, 255, 255), "Save Structure")
        self.select_button = Button((180, 300), (255, 255, 255), "Select Multiple", True)
        self.creating_particle = False
        self.temp_particle_list = []
        self.temp_single = Particle

    def create_particle(self, starttemp, con_streng):
        self.temp_single = Particle(0, 0, 10, con_streng, [], [], pygame.mouse.get_pos(), len(particle_list) + len(self.temp_particle_list), starttemp, False, .000002, True)
        self.temp_particle_list.append(self.temp_single)

    def update(self):
        self.connection_strength_slide.draw_update()
        self.connect_button.draw()
        self.connect_button.click()
        self.start_temp_slide.draw_update()

        self.save_button.draw()
        self.save_button.click()
        self.add_button.draw()
        self.add_button.click()
        self.place_button.draw()
        self.place_button.click()
        self.select_button.draw()
        self.select_button.click()
        if self.place_button.pressed:
            reales_temps = 0
            while reales_temps < len(self.temp_particle_list):
                self.temp_particle_list[reales_temps].istemp = False
                particle_list.append(self.temp_particle_list[reales_temps])
                self.temp_particle_list.remove(self.temp_particle_list[reales_temps])
                reales_temps += 0
        if self.creating_particle and mouse_click and not self.place_button.get_mouse_hover():
            self.creating_particle = False
            self.temp_single.beingheld = False
        if self.add_button.pressed and not self.creating_particle:
            self.creating_particle = True
            self.create_particle(self.start_temp_slide.realval(), self.connection_strength_slide.realval())
        drawtemps = 0
        if not self.select_button.pressed:
            while drawtemps < len(self.temp_particle_list):
                self.temp_particle_list[drawtemps].shallow_update()
                self.temp_particle_list[drawtemps].selected = False
                if draw_lines:
                    particle = self.temp_particle_list[drawtemps]
                    con_num = len(particle.connections)
                    con_num_cyc = 0
                    while con_num_cyc < con_num and draw_lines and len(self.temp_particle_list) > 0:
                        connection = self.temp_particle_list[particle.connections[con_num_cyc] - len(particle_list)]
                        pygame.draw.line(screen, (255, 255, 255), particle.position, connection.position, 1)
                        con_num_cyc += 1
                drawtemps += 1
        elif self.select_button.pressed:
            while drawtemps < len(self.temp_particle_list):
                currtemp = self.temp_particle_list[drawtemps]
                prevpos = currtemp.target_position
                currtemp.shallow_update()
                currtemp.target_position = prevpos
                if draw_lines:
                    particle = self.temp_particle_list[drawtemps]
                    con_num = len(particle.connections)
                    con_num_cyc = 0
                    while con_num_cyc < con_num and draw_lines and len(self.temp_particle_list) > 0:
                        connection = self.temp_particle_list[particle.connections[con_num_cyc] - len(particle_list)]
                        pygame.draw.line(screen, (255, 255, 255), particle.position, connection.position, 1)
                        con_num_cyc += 1
                if self.connect_button.pressed and currtemp.selected:
                    addcon = 0
                    while addcon < len(self.temp_particle_list):
                        curr = self.temp_particle_list[addcon]
                        if curr.selected and curr.connections.count(currtemp.id) == 0:
                            currtemp.connections.append(curr.id)
                            currtemp.con_tar_lengs.append(currtemp.get_distance(curr.position))
                            if curr.connections.count(currtemp.id) == 0:
                                curr.connections.append(currtemp.id)
                                curr.con_tar_lengs.append(curr.get_distance(currtemp.position))
                        addcon += 1
                drawtemps += 1
            if self.connect_button.pressed:
                self.connect_button.pressed = False
                self.select_button.pressed = False



def make_line(length, y, x, last_id, spacing, pins):
    cyc = 0
    s = spacing
    particle_list.append(Particle(0, 0, 10, 100, [last_id + 1], [s, s], (x - s, y), last_id, 0, pins))
    last_id += 1
    while cyc < length:
        particle_list.append(Particle(0, 0, 10, 100, [last_id - 1, last_id + 1], [s, s], (x + (cyc * s), y), last_id, 0, False))
        cyc += 1
        last_id += 1
    particle_list.append(Particle(0, 0, 10, 100, [last_id - 1], [s], (x + (cyc * s), y), last_id, 0, pins))


def make_matrix(width, height, y, x, id_to_start_on, spacing, pins, tem):
    width_cyc = 1
    height_cyc = 0
    x_increase = 0
    y_increase = 1
    id = id_to_start_on
    s = spacing
    particle_list.append(Particle(0, 0, 10, 100, [id + 1, id + height + 1], [s, s], (x, y + (spacing * y_increase)), id, tem, pins))
    y_increase = 2
    id = id_to_start_on + 1
    while height_cyc < height - 1:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id + height + 1], [s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
        y_increase += 1
        id += 1
        height_cyc += 1
    particle_list.append(Particle(0, 0, 10, 100, [id + height + 1, id - 1], [s, s], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
    id += 1
    while width_cyc < width - 1:
        x_increase += 1
        height_cyc = 0
        y_increase = 1
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - height - 1, id + height + 1], [s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
        id += 1
        y_increase = 2
        while height_cyc < height - 1:
            particle_list.append(Particle(0, 0, 10, 100, [id - height - 1, id - 1, id + 1, id + height + 1], [s, s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase)),
                                 id, tem, False))
            y_increase += 1
            id += 1
            height_cyc += 1
        particle_list.append(Particle(0, 0, 10, 100, [id - 1, id - height - 1, id + height + 1], [s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
        id += 1
        width_cyc += 1
    y_increase = 1
    x_increase += 1
    particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - height - 1], [s, s], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, pins))
    id += 1
    y_increase = 2
    height_cyc = 0
    while height_cyc < height - 1:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id - height - 1], [s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase)),
                             id, tem, False))
        y_increase += 1
        id += 1
        height_cyc += 1
    particle_list.append(Particle(0, 0, 10, 100, [id - height - 1, id - 1], [s, s], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))


def make_matrix_hex(width, height, y, x, id_to_start_on, spacing, pins, tem):
    Particle.connection_tar_leng = spacing
    width_cyc = 1
    height_cyc = 0
    x_increase = 0
    y_increase = 1
    id = id_to_start_on
    s = spacing
    he_spac = spacing / 2
    particle_list.append(Particle(0, 0, 10, 100, [id + 1, id + height + 1, id + height], [s, s, s], (x, y + (spacing * y_increase) + he_spac), id, tem, pins))
    y_increase = 2
    id = id_to_start_on + 1
    while height_cyc < height - 1:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id + height + 1, id + height - 2, id + height], [s, s, s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem, False))
        y_increase += 1
        id += 1
        height_cyc += 1
    particle_list.append(Particle(0, 0, 10, 100, [id + height + 1, id - 1, id + height], [s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem, False))
    id += 1
    while width_cyc < width - 1:
        if he_spac == spacing / 2:
            he_spac = -spacing / 2
        elif he_spac == -spacing / 2:
            he_spac = spacing / 2
        x_increase += 1
        height_cyc = 0
        y_increase = 1
        if he_spac == spacing / 2:
            particle_list.append(
                Particle(0, 0, 10, 100, [id + 1, id - height - 1, id + height + 1, id - height, id + height + 2],
                         [s, s, s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem,
                         False))
        elif he_spac == -spacing / 2:
            particle_list.append(
                Particle(0, 0, 10, 100, [id + 1, id - height + 1, id + height - 1, id - height, id + height + 1],
                         [s, s, s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem,
                         False))
        id += 1
        y_increase = 2
        while height_cyc < height - 1:
            if he_spac == spacing / 2:
                particle_list.append(Particle(0, 0, 10, 100,[id - height - 1, id - 1, id + 1, id + height + 1, id + height + 2,
                                     id - height, id + height], [s, s, s, s, s, s, s], (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac),
                                     id, tem, False))
            elif he_spac == -spacing / 2:
                particle_list.append(Particle(0, 0, 10, 100, [id - height - 1, id - 1, id + 1, id + height - 1, id + height +1 ,
                                             id - height, id + height], [s, s, s, s, s, s, s],
                                             (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac),
                                             id, tem, False))
            y_increase += 1
            id += 1
            height_cyc += 1
        if he_spac == spacing / 2:
            particle_list.append(Particle(0, 0, 10, 100, [id - 1, id - height - 1, id + height + 1, id + height], [s, s, s, s],
                         (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem, False))
        elif he_spac == -spacing / 2:
            particle_list.append(
                Particle(0, 0, 10, 100, [id - 1, id - height - 1, id + height - 1, id + height, id - height], [s, s, s, s, s],
                         (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem, False))
        id += 1
        width_cyc += 1
    y_increase = 1
    x_increase += 1
    if he_spac == spacing / 2:
        he_spac = -spacing / 2
    elif he_spac == -spacing / 2:
        he_spac = spacing / 2
    if he_spac == spacing / 2:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - height - 1, id - height], [s, s, s],
                                      (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem,
                                      pins))
    elif he_spac == -spacing / 2:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - height, id + height + 1], [s, s, s],
                                      (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem,
                                      pins))
    id += 1
    y_increase = 2
    height_cyc = 0
    while height_cyc < height - 1:
        if he_spac == spacing / 2:
            particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id - height - 1, id - height], [s, s, s, s],
                                          (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac),
                                          id, tem, False))
        elif he_spac == -spacing / 2:
            particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id - height - 2, id - height - 1], [s, s, s, s],
                                          (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac),
                                          id, tem, False))
        y_increase += 1
        id += 1
        height_cyc += 1
    if he_spac == spacing / 2:
        particle_list.append(Particle(0, 0, 10, 100, [id - height - 1, id - 1, id - height], [s, s, s],
                                      (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem,
                                      False))
    elif he_spac == -spacing / 2:
        particle_list.append(Particle(0, 0, 10, 100, [id - height, id - 1], [s, s],
                                      (x + (x_increase * spacing), y + (spacing * y_increase) + he_spac), id, tem,
                                      False))


def make_matrix_diag(width, height, y, x, id_to_start_on, spacing, pins, squeeze, tem):
    Particle.connection_tar_leng = spacing
    width_cyc = 1
    height_cyc = 0
    x_increase = 0
    y_increase = 1
    id = id_to_start_on
    if squeeze == False:
        diag_space = spacing * math.sqrt(2)
    else:
        diag_space = spacing
    s = spacing
    s2 = diag_space
    particle_list.append(Particle(0, 0, 10, 100, [id + 1, id + height + 1, id + height + 2], [s, s, s2], (x, y + (spacing * y_increase)), id, tem, pins))
    y_increase = 2
    id = id_to_start_on + 1
    while height_cyc < height - 1:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id + height + 1, id + height + 2, id + height], [s, s, s, s2, s2], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
        y_increase += 1
        id += 1
        height_cyc += 1
    particle_list.append(Particle(0, 0, 10, 100, [id + height + 1, id - 1, id + height], [s, s, s2], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
    id += 1
    while width_cyc < width - 1:
        x_increase += 1
        height_cyc = 0
        y_increase = 1
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - height - 1, id + height + 1, id - height, id + height + 2], [s, s, s, s2, s2], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
        id += 1
        y_increase = 2
        while height_cyc < height - 1:
            particle_list.append(Particle(0, 0, 10, 100, [id - height - 1, id - height - 2, id - 1, id + 1, id + height + 1, id + height + 2, id - height, id + height], [s, s2, s, s, s, s2, s2, s2], (x + (x_increase * spacing), y + (spacing * y_increase)),
                                 id, tem, False))
            y_increase += 1
            id += 1
            height_cyc += 1
        particle_list.append(Particle(0, 0, 10, 100, [id - 1, id - height - 1, id - height - 2, id + height + 1, id + height], [s, s, s2, s, s2], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))
        id += 1
        width_cyc += 1
    y_increase = 1
    x_increase += 1
    particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - height - 1, id - height], [s, s, s2], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, pins))
    id += 1
    y_increase = 2
    height_cyc = 0
    while height_cyc < height - 1:
        particle_list.append(Particle(0, 0, 10, 100, [id + 1, id - 1, id - height - 1, id - height - 2, id - height], [s, s, s, s2, s2], (x + (x_increase * spacing), y + (spacing * y_increase)),
                             id, tem, False))
        y_increase += 1
        id += 1
        height_cyc += 1
    particle_list.append(Particle(0, 0, 10, 100, [id - height - 1, id - height - 2, id - 1, id - height], [s, s2, s, s2], (x + (x_increase * spacing), y + (spacing * y_increase)), id, tem, False))


particle_list = []
grav_slider = Slider((50, 50), 100, (-1, 1), (255, 255, 255), "Gravity", 50, 0)
color_switch = Switcher((56, 75), ["Temperature 1", "Temperature 2", "Velocity"], (255, 255, 255), "Color view")
light_intens_slider = Slider((50, 100), 100, (0, 400), (255, 255, 255), "Light Intensity", 80)
light_move_affect_switch = Switcher((56, 75), ["Yes", "No"], (255, 255, 255), "Light Moves Particles")
wall_bounciness = 1


def reset_one():
    global light, light_2, grav_slider, color_switch, light_intens_slider, light_move_affect_switch, walls_cool_switch, wall_bounciness_slider, conductivity_slider, newpartbutton, clear_button
    make_matrix_diag(10, 20, 260, 100, len(particle_list), 15, False, False, -80)

    light_2 = Lightsource(-80, (50, 500), -90, False)
    light = Lightsource(380, (1000, -80), 0, True)
    grav_slider = Slider((50, 50), 100, (-1, 1), (255, 255, 255), "Gravity", 50, -1)
    wall_bounciness_slider = Slider((50, 80), 100, (0, 100), (255, 255, 255), "Wall Bounciness", 50, -1)
    light_intens_slider = Slider((50, 110), 100, (0, 2000), (255, 255, 255), "Light Intensity", 10)
    conductivity_slider = Slider((50, 140), 100, (0, 1), (255, 255, 255), "Material Conductivity", 10)
    color_switch = Switcher((56, 170), ["Temperature 1", "Temperature 2", "Velocity"], (255, 255, 255), "Color view")
    light_move_affect_switch = Switcher((56, 200), ["No", "Yes"], (255, 255, 255), "Light Moves Particles")
    walls_cool_switch = Switcher((56, 230), ["No", "Yes"], (255, 255, 255), "Walls Cool Particles")
    clear_button = Button((56, 290), (255, 255, 255), "Clear Screen", False)
    newpartbutton = Button((56, 260), (255, 255, 255), "New Structure", False)


reset_one()
particle_group = pygame.sprite.Group()
add_cyc = 0
old_list = copy.copy(particle_list)
while add_cyc < len(particle_list):
    particle_group.add(particle_list[add_cyc])
    add_cyc += 1

draw_lines = False
play = True
mouse_click = False
mouse_click_2 = False
vibrate = False
hol_var = False
color_mode = 0
particle_menu = Structure_menu()
new_part_menu = False
while play:
    keys = pygame.key.get_pressed()
    clock.tick(30)
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_click = True
            hold_var = False
        else:
            mouse_click = False
            hold_var = False
            mouse_click_2 = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                add_cyc = 0
                particle_list = []
                particle_group.empty()
                reset_one()
                while add_cyc < len(particle_list):
                    particle_group.add(particle_list[add_cyc])
                    add_cyc += 1
            if event.key == pygame.K_v:
                vibrate = not vibrate
            if event.key == pygame.K_t:
                draw_lines = not draw_lines
            if event.key == pygame.K_m:
                Particle.conductivity += .02
            if event.key == pygame.K_n:
                Particle.conductivity -= .02
            if event.key == pygame.K_COMMA:
                if change < 2070:
                    change += 5
            if event.key == pygame.K_PERIOD:
                if change > -2070:
                    change -= 5
    if mouse_click and not hold_var:
        mouse_click_2 = True
    else:
        mouse_click_2 = False
    if mouse_click:
        hold_var = True
    drawing_connections = 0
    oldparticle_list = particle_list
    while drawing_connections < len(oldparticle_list) and draw_lines == True:
        particle = oldparticle_list[drawing_connections]
        con_num = len(particle.connections)
        con_num_cyc = 0
        while con_num_cyc < con_num and draw_lines:
            connection = particle_list[particle.connections[con_num_cyc]]
            pygame.draw.line(screen, (255, 255, 255), particle.position, connection.position, 1)
            con_num_cyc += 1
        drawing_connections += 1
    drawing_dots = 0
    particle_group.draw(screen)
    particle_group.empty()
    old_list = []
    add_cyc = 0
    while add_cyc < len(particle_list):
        new = particle_list[add_cyc].copy()
        old_list.append(new)
        particle_group.add(new)
        add_cyc += 1

    particle_group.update()

    particle_group.empty()
    particle_list = []
    add_cyc = 0
    while add_cyc < len(old_list):
        new = old_list[add_cyc]
        particle_list.append(new)
        particle_group.add(new)
        add_cyc += 1

    adding_temps = 0
    temp = 0
    while adding_temps < len(particle_list):
        current_part = particle_list[adding_temps]
        temp += current_part.temperature
        adding_temps += 1
    Lightsource.update(light)
    Lightsource.update(light_2)
    newpartbutton.draw()
    newpartbutton.click()
    clear_button.draw()
    clear_button.click()
    if clear_button.pressed:
        particle_list.clear()
        particle_group.empty()
    if newpartbutton.pressed:
        newpartbutton.pressed = False
        new_part_menu = not new_part_menu
    light_intens_slider.draw_update()
    grav_slider.draw_update()
    wall_bounciness_slider.draw_update()
    conductivity_slider.draw_update()

    light_move_affect_switch.switch()
    light_move_affect_switch.display()
    color_switch.switch()
    color_switch.display()
    walls_cool_switch.switch()
    walls_cool_switch.display()
    cool = walls_cool_switch.curr_val
    if cool == 0:
        walls_remove_temp = False
    elif cool == 1:
        walls_remove_temp = True
    colortype = color_switch.curr_val
    if light_move_affect_switch.curr_val == 0:
        light.affect_move = False
    elif light_move_affect_switch.curr_val == 1:
        light.affect_move = True
    gravity = grav_slider.realval() / 40
    light.intensity = light_intens_slider.realval()
    wall_bounciness = wall_bounciness_slider.realval() / 100
    Particle.conductivity = conductivity_slider.realval() / 2.5
    if new_part_menu:
        particle_menu.update()
    pygame.display.flip()
