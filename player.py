import numpy as np

class player_module:
        
    # constructor, allocate any private date here
    def __init__(self):
        self.init_x, self.init_y = -1., -1.

    # Please update the banner according to your information
    def banner(self):
        print('-'*40)
        print('Author: Hung-Jui Wang')
        print('ID: b05502087')
        print('-'*40)
    
    # Decision making function for moving your ship, toward next frame:
    # simply return the speed and the angle
    # ----------------------------------------------
    # The value of "speed" must be between 0 and 1.
    # speed = 1 : full speed, moving 0.01 in terms of space coordination in next frame
    # speed = x : moving 0.01*x in terms of space coordination
    # speed = 0 : just don't move
    #
    # The value of angle must be between 0 and 2*pi.
    #
    # if speed is less than 1, it will store the gauge value by 4*(1-speed).
    # If the gauge value reach 1000, it will perform the "gauge attack" and destory
    # any enemy within a circle of 0.6 radius
    #

    def angleOf_vectors(self, v1, v2):
        unit_vector_1 = v1 / np.linalg.norm(v1)
        unit_vector_2 = v2 / np.linalg.norm(v2)
        dot_product = np.dot(unit_vector_1, unit_vector_2)
        if dot_product > 1.:
            dot_product = 1.
        if dot_product < -1.:
            dot_product = -1.
        try:
            angle = np.arccos(dot_product)
        except:
            print(dot_product)

        return angle

    def vector_len(self, v):
        vx ,vy = v
        return (vx**2+vy**2)**(0.5)

    def getVertical_distance(self, x,y,dx,dy,player1_x,player1_y):
        bullet2player = np.array([player1_x-x, player1_y-y])
        bullet_direction = np.array([dx,dy])
        ang = self.angleOf_vectors(bullet2player, bullet_direction)
        #print(ang)
        vertical_dis = self.vector_len(bullet2player * np.sin(ang))
        return vertical_dis
    
    def vector2angle(self, v):
        vx, vy = v
        return np.arctan2(vy, vx)
    
    def clockize(self, v1, v2):
        v1x, v1y = v1
        v2x, v2y = v2
        return v1x*v2y - v1y*v2x

    def bossCome(self, enemy_data):
        for e in enemy_data:
            if e[0] == 6:
                return True
        return False

    def decision(self,player_data, enemy_data):
        
        speed, angle = 0., 0.
        
        # your data
        player1_x      = player_data[0][0]
        player1_y      = player_data[0][1]
        player1_hp     = player_data[0][2]
        player1_score  = player_data[0][3]
        player1_gauge  = player_data[0][4]
        player1_weapon = player_data[0][5]
        
        # data for another player
        player2_x      = player_data[1][0]
        player2_y      = player_data[1][1]
        player2_hp     = player_data[1][2]
        player2_score  = player_data[1][3]
        player2_gauge  = player_data[1][4]
        player2_weapon = player_data[1][5]
        
        # save the initial x position
        if self.init_x==-1. and self.init_y==-1.:
            self.init_x, self.init_y = player1_x, player1_y
        
        # let's try to move back to the initial position by default
        speed = ((self.init_x-player1_x)**2 + (self.init_y-player1_y)**2)**0.5
        speed /= 0.01 # since the maximum speed is 0.01 unit per frame
        if speed>1.: speed = 1.
        angle = np.arctan2(self.init_y-player1_y,self.init_x-player1_x)
        
        attack_dx, attack_dy = 0, 0
        avoid_dx, avoid_dy = 0, 0
        minX = 21474836
        # loop over the enemies and bullets
        if self.bossCome(enemy_data):
            #print('boss come')
            self.init_x = 0.4
            self.init_y = 0.1
            for data in enemy_data:
                type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo, 6 - boss, 7 - rescuecap, 8 - weaponup
                x    = data[1]
                y    = data[2]
                dx   = data[3] # expected movement in x direction for the next frame
                dy   = data[4] # expected movement in y direction for the next frame

                # calculate the distance toward player1
                dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5
                if (type==7 or type == 8) and dist < 0.7 and y <0.6:
                    avoid_dx = (x-player1_x)
                    avoid_dy = (y-player1_y)
                    break

                if type == 0 and dist < 0.25:
                    ret = self.getVertical_distance(x,y,dx,dy,player1_x,player1_y)
                    #print(ret)
                    if ret < 0.1:
                        temp_dx = dy
                        temp_dy = -dx
                        if self.clockize(np.array([dx,dy]), np.array([player1_x - x,player1_y - y]))\
                            * self.clockize(np.array([dx,dy]), np.array([temp_dx, temp_dy]))< 0: #go right
                            avoid_dx += -temp_dx
                            avoid_dy += -temp_dy
                        else:
                            avoid_dx += temp_dx
                            avoid_dy += temp_dy
                        """
                        # use the angle of bullet to decide escape direction
                        if self.clockize(np.array([x-player1_x,y-player1_y]), np.array([dx,dy])) < 0: #go right
                            avoid_dx += -0.3
                            avoid_dy = 0
                        else: # go left
                            avoid_dx += 0.3
                            avoid_dy = 0
                        """
                if type == 6 and dist < 0.3:
                    avoid_dx += (player1_x-x)
                    avoid_dy += (player1_y-y)
                
        else:
            self.init_x = 0.5
            self.init_y = 0.15

            for data in enemy_data:
                type = data[0] # 0 - bullet, 1..4 - different types of invaders, 5 - ufo, 6 - boss, 7 - rescuecap, 8 - weaponup
                x    = data[1]
                y    = data[2]
                dx   = data[3] # expected movement in x direction for the next frame
                dy   = data[4] # expected movement in y direction for the next frame
                
                # calculate the distance toward player1
                dist = ((x-player1_x)**2+(y-player1_y)**2)**0.5

                # if too close, avoid
                #if type == 6 and dist < 0.3:
                #    avoid_dx += (player1_x-x)
                # if the rescuecap/weaponup is close enough, try to catch it
                if (type==7 or type == 8) and dist < 0.7 and y <0.6:
                    avoid_dx = (x-player1_x)
                    avoid_dy = (y-player1_y)
                    break

                elif dist < 0.25 and type !=3:
                    ### avoid
                    if type == 0:
                        ret = self.getVertical_distance(x,y,dx,dy,player1_x,player1_y)
                        #print(ret)
                        if ret < 0.1:
                            temp_dx = dy
                            temp_dy = -dx
                            if self.clockize(np.array([dx,dy]), np.array([player1_x - x,player1_y - y]))\
                            * self.clockize(np.array([dx,dy]), np.array([temp_dx, temp_dy]))< 0: #go right
                                avoid_dx += -temp_dx
                                avoid_dy += -temp_dy
                            else:
                                avoid_dx += temp_dx
                                avoid_dy += temp_dy
                    
                    elif (type==1 or type==2 or type==4 or type==5) and dist<0.15:
                        ### mix with avoid bullet?
                        # escape to the opposite direction of enemy
                        avoid_dx += (player1_x-x)
                        avoid_dy += (player1_y-y)

                elif (dist >= 0.25 and dist < 0.9) or (type==3 and y > player1_y):
                    # if there is an enemy and is close enough, attack it
                    #print('attack!!!')
                    if type!= 0 and type!=6 and type!=7 and type!=8:
                        attack_dx = (x-player1_x)
                        attack_dy = self.init_y-player1_y
                        """
                        if abs(x-player1_x) < minX:
                            minX = abs(x-player1_x)
                            attack_dx = (x-player1_x)
                            attack_dy = self.init_y-player1_y
                        """
                
                ### consider the wall with mix vector
                if player1_y < 0.2:
                    #print('player1_y', player1_y)
                    pass

        if avoid_dx != 0 or avoid_dy != 0:
            to_dx, to_dy = avoid_dx, avoid_dy
            speed = 1
        elif attack_dx != 0 or attack_dy != 0:
            to_dx, to_dy = attack_dx, attack_dy
            speed = 0.8
        else: 
            # no need to attack / avoid
            # just go
            to_dx = 0
            to_dy = 0

        #print('speed', speed)
        if to_dx != 0 or to_dy != 0:
            angle = self.vector2angle(np.array([to_dx, to_dy]))

        return speed, angle