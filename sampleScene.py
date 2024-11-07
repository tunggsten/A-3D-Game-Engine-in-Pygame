from yeentooth import *
import pygame
import time
import random

origin = Abstract()
ROOT.add_child_relative(origin)

environment = Abstract()
origin.add_child_relative(environment)

player = Abstract(Matrix([[0],
                          [0],
                          [-4]]))
origin.add_child_relative(player)

camera = Camera(ORIGIN, I3, 60)
player.add_child_relative(camera)

listener = Listener(1, 2)
player.add_child_relative(listener)

playerTopBody = Body(1, 2, 2, False)
playerTopCollider = SphereCollider(0.5, playerTopBody, Matrix([[0],
                                                            [0.25],
                                                            [0]]))
player.add_child_relative(playerTopBody)

playerBottomBody = Body(1, 2, 2, False)
playerBottomCollider = SphereCollider(0.5, playerBottomBody, Matrix([[0],
                                                            [-0.5],
                                                            [0]]))
player.add_child_relative(playerBottomBody)

blawg = Texture("blawg.png")

teapot = Wavefront("lowPolyUtahTeapot.obj",
                   (0, 0, 0),
                   True,
                   Matrix([[5],
                          [0],
                          [0]]), 
                  I3.multiply_contents(0.15),
                  texture=blawg)

environment.add_child_relative(teapot)

leftWall = Plane((4, 4), (0, 0, 0), True, Matrix([[-2],
                                                  [1],
                                                  [0]]), Matrix([[0, 4, 0],
                                                                 [-4, 0, 0],
                                                                 [0, 0, 4]]))
environment.add_child_relative(leftWall)

backWall = Body(1, 0.8, 5, False, Matrix([[0],
                                          [1],
                                          [2]]), Matrix([[1, 0, 0],
                                                         [0, 0, 1],
                                                         [0, -1, 0]]))
backWallCollider = PlaneCollider(4, 4, backWall)

backWallVisual = Plane((4, 4), (0, 0, 0), True, ORIGIN, I3.multiply_contents(4))
backWall.add_child_relative(backWallVisual)

environment.add_child_relative(backWall)

# Floor

floor = Body(1, 0.8, 5, False, Matrix([[2],
                                    [-1],
                                    [-2]]))

environment.add_child_relative(floor)

floorCollider = PlaneCollider(8, 8, floor)

floorVisual = Plane((8, 8), (0, 0, 0), True, ORIGIN, I3.multiply_contents(8))
floor.add_child_relative(floorVisual)

# Ball

balls = []

for i in range(5):
    ball = Body(1, 0.8, 10, True, Matrix([[0],
                                      [i],
                                      [0]]))
    environment.add_child_relative(ball)

    ball.velocity = Matrix([[random.random()],
                            [0],
                            [-random.random()]])
    
    ball.add_tag(f"Ball {i}")

    ballCollider = SphereCollider(0.25, ball)

    ballVisual = Cube((0, 0, 0), True, ORIGIN, I3.multiply_contents(0.5))
    ballVisual.change_tris_to_gradient((248, 54, 119), (58, 244, 189), (229, 249, 54))

    ball.add_child_relative(ballVisual)

    balls.append(ball)


floorVisual.set_pattern_triangles((0, 0, 0), (108, 108, 108))
backWallVisual.set_pattern_triangles((0, 0, 0), (108, 108, 108))
leftWall.set_pattern_triangles((252, 252, 252), (108, 108, 108))


backWallVisual.change_tris_to_gradient((248, 54, 119), (58, 244, 189), (229, 249, 54))

boom = SoundEffect("boom.wav", 0.4)
teapot.add_child_relative(boom)


lightCarousel = Abstract(Matrix([[5],
                                 [0],
                                 [0]]))

environment.add_child_relative(lightCarousel)

lights = []

greenLight = Light(1, (100, 255, 100), Matrix([[2],
                                         [0],
                                         [0]]))
lights.append(greenLight)

redLight = Light(1, (255, 100, 100), Matrix([[0],
                                         [0],
                                         [-2]]))
lights.append(redLight)

blueLight = Light(1, (100, 100, 255), Matrix([[0],
                                         [0],
                                         [2]]))
lights.append(blueLight)

for light in lights:
    lightCarousel.add_child_relative(light)

sun = SunLight(0.9, (220, 220, 200))
sun.rotate_euler_radians(0, 0, -math.pi / 4)

environment.add_child_relative(sun)



# ---------------- MAIN LOOP ----------------

movementSpeed = 4
lookSpeed = 2

frameDelta = 0

while running:
    startTime = time.time()

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            
    playerMovement = [[0],
                        [0],
                        [0]]

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        playerMovement[2] = [1]
    if keys[pygame.K_s]:
        playerMovement[2] = [-1]

    if keys[pygame.K_a]:
        playerMovement[0] = [-1]
    if keys[pygame.K_d]:
        playerMovement[0] = [1]

    if keys[pygame.K_SPACE]:
        playerMovement[1] = [1]
    if keys[pygame.K_LSHIFT]:
        playerMovement[1] = [-1]

    if keys[pygame.K_b]:
        boom.play()

    player.translate_relative(Matrix(playerMovement).set_magnitude(movementSpeed * frameDelta))
        
    if keys[pygame.K_RIGHT]:
        player.rotate_euler_radians(0, lookSpeed * frameDelta, 0)
    if keys[pygame.K_LEFT]:
        player.rotate_euler_radians(0, -lookSpeed * frameDelta, 0)

    if keys[pygame.K_UP]:
        camera.rotate_euler_radians(-lookSpeed * frameDelta, 0, 0)
    if keys[pygame.K_DOWN]:
        camera.rotate_euler_radians(lookSpeed * frameDelta, 0, 0)

    teapot.rotate_euler_radians(0, frameDelta, 0)

    lightCarousel.rotate_euler_radians(0, -frameDelta / 3, 0)

    for ball in balls:
        ballLocation = ball.objectiveLocation.get_contents()
        if (not -2 < ballLocation[1][0] < 6):
            ball.set_location_objective(Matrix([[random.random()],
                            [0],
                            [-random.random()]]))
            ball.velocity = ORIGIN

    process_bodies(frameDelta)
        
    window.fill((255, 255, 255))
    camera.render()

    listener.listen()

    print(I3.get_collumb(0).get_contents())
    print(I3.get_row(1).get_contents())
        
    frameDelta = time.time() - startTime

    if frameDelta > 0.1:
        print("Framedrop detected")

    try:
        print(f"Finished frame in {frameDelta} seconds. \nEquivalent to {1 / (frameDelta)} Hz \n")
    except:
        print("Very fast")

    print(screen_colours([(255, 255, 0), (0, 0, 255)]))
        

    pygame.display.flip()