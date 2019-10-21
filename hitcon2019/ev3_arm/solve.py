import turtle
turtle.screensize(20000,1500)
turtle.speed('fastest')

for line in open("disas"):
    if 'port_motor' in line:
        motor = line.split('port_motor: ')[1][0]
        rotations = float(line.split('rotations: ')[1].split()[0])
        speed = int(line.split('speed: ')[1].split()[0])
        #print(motor, rotations, speed)
        if motor == 'A':
            dist = rotations/20
            if speed < 0:
                dist = -dist
            x,y = turtle.pos()
            y += dist
            turtle.goto((x,y))
        elif motor == 'B':
            if speed > 0:
                turtle.penup()
            else:
                turtle.pendown()
        elif motor == 'C':
            dist = rotations * 10
            if speed < 0:
                dist = -dist
            x,y = turtle.pos()
            x += dist
            turtle.goto((x,y))


turtle.done()
