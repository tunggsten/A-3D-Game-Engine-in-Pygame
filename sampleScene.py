from engine.tooth import *
import pygame
import time
import random

# First, let's give ourselves an origin to work with.

origin = Abstract()
ROOT.add_child_relative(origin)



# Now, let's make a vessel for our player to control.

player = Abstract(Matrix([[0],
                          [0],
                          [-4]]))

origin.add_child_relative(player)

camera = Camera(ORIGIN, I3, 60)
player.add_child_relative(camera)



ears = Listener(1, 2) # Important distinction:

                          # Volume (the first one) is how loud sound is played back to the 
                          # player's speakers.
                          
                          # Sensitivity is how well it picks up sound in 3D space.
                          
                          # Ultimately, they're pretty similar, but just bear that in mind.
                          
player.add_child_relative(ears)

# This vessel is going to be able to move through stuff, but we still want to give it some
# solid body to whack things with. Let's add collision!



playerTopBody = Body(1, 1, 0.5, False)
playerTopCollider = SphereCollider(0.5, playerTopBody, Matrix([[0],
                                                            [0.25],
                                                            [0]]))
player.add_child_relative(playerTopBody)

playerBottomBody = Body(1, 1, 0.5, False)
playerBottomCollider = SphereCollider(0.5, playerBottomBody, Matrix([[0],
                                                            [-0.5],
                                                            [0]]))
player.add_child_relative(playerBottomBody)




# Let's start making our environment!

environment = Abstract()
origin.add_child_relative(environment)

# In this case, this is just to keep things neat. This abstract is like a folder, as in it's
# just there to group all of its children by topic.

# We need to set up a texture resource for a model we're about to use:

blawg = Texture("blawg.png")

# Now, we can instantiate the model:

teapot = Wavefront("lowPolyUtahTeapot.obj",
                   (0, 0, 0),
                   True,
                   Matrix([[5],
                          [0],
                          [0]]), 
                  I3.multiply_scalar(0.15), # This will shrink it down to 15% of it's size.
                  texture=blawg)

environment.add_child_relative(teapot)

leftWall = Body(1, 0.8, 5, False, Matrix([[-2],
                                          [1],
                                          [0]]), Matrix([[0, 1, 0],
                                                         [-1, 0, 0],
                                                         [0, 0, 1]]))
leftWallCollider = PlaneCollider(4, 4, leftWall)

leftWallVisual = Plane((3, 3), (0, 0, 0), True, ORIGIN, I3.multiply_scalar(4))
leftWall.add_child_relative(leftWallVisual)

environment.add_child_relative(leftWall)

backWall = Body(1, 0.8, 5, False, Matrix([[0],
                                          [1],
                                          [2]]), Matrix([[1, 0, 0],
                                                         [0, 0, 1],
                                                         [0, -1, 0]]))
backWallCollider = PlaneCollider(4, 4, backWall)

backWallVisual = Plane((3, 3), (0, 0, 0), True, ORIGIN, I3.multiply_scalar(4))
backWall.add_child_relative(backWallVisual)

environment.add_child_relative(backWall)

# Floor

floor = Body(1, 0.8, 0.5, False, Matrix([[2],
                                    [-1],
                                    [-2]]))

environment.add_child_relative(floor)

floorCollider = PlaneCollider(8, 8, floor)

floorVisual = Plane((6, 6), (0, 0, 0), True, ORIGIN, I3.multiply_scalar(8))
floor.add_child_relative(floorVisual)

# Ball

balls = []

for i in range(5):
    ball = Body(1, 0.8, 5, True, Matrix([[0],
                                      [i],
                                      [0]]))
    environment.add_child_relative(ball)

    ball.velocity = Matrix([[random.random()],
                            [0],
                            [-random.random()]])
    
    ball.add_tag(f"Ball {i}")

    ballCollider = SphereCollider(0.25, ball)

    ballVisual = Cube((0, 0, 0), True, ORIGIN, I3.multiply_scalar(0.5))
    ballVisual.change_tris_to_gradient((248, 54, 119), (58, 244, 189), (229, 249, 54))

    ball.add_child_relative(ballVisual)

    balls.append(ball)


floorVisual.set_pattern_triangles((0, 0, 0), (108, 108, 108))
backWallVisual.set_pattern_triangles((0, 0, 0), (108, 108, 108))
leftWallVisual.set_pattern_triangles((252, 252, 252), (108, 108, 108))


backWallVisual.change_tris_to_gradient((248, 54, 119), (58, 244, 189), (229, 249, 54))

boom = SoundEffect("boom.wav", 0.4)
teapot.add_child_relative(boom)


lightCarousel = Abstract(Matrix([[5],
                                 [0],
                                 [0]]))

environment.add_child_relative(lightCarousel)

lights = []

greenLight = Light(0.9, (100, 255, 100), Matrix([[2],
                                         [0],
                                         [0]]))
lights.append(greenLight)

redLight = Light(0.9, (255, 100, 100), Matrix([[0],
                                         [0],
                                         [-2]]))
lights.append(redLight)

blueLight = Light(0.9, (100, 100, 255), Matrix([[0],
                                         [0],
                                         [2]]))
lights.append(blueLight)

for light in lights:
    lightCarousel.add_child_relative(light)

sun = SunLight(0.8, (255, 255, 220))
sun.rotate_euler_radians(0, 0, -math.pi / 6)
sun.rotate_euler_radians(0, math.pi / 3, 0)

environment.add_child_relative(sun)


passthroughTest = TripVolume()
passthroughTestCollider = SphereCollider(3, passthroughTest)

environment.add_child_relative(passthroughTest)



# ---------------- PER FRAME PROCESS FUNCTIONS ----------------

# Here, we'll define what we want each of our abstracts to do each frame, and then
# call them in whatever order we want.



def process_player(frameDelta:float, keys):

    # Define our speeds
    movementSpeed = 4
    lookSpeed = 2
    
    playerMovement = [[0],
                      [0],
                      [0]]

    # Turn the status of the movement keys into a vector
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

    # Move the player by the normalised version of that vector
    player.translate_relative(Matrix(playerMovement).set_magnitude(movementSpeed * frameDelta))
        
    # Do the same but for the camera pretty much
    if keys[pygame.K_RIGHT]:
        player.rotate_euler_radians(0, lookSpeed * frameDelta, 0)
    if keys[pygame.K_LEFT]:
        player.rotate_euler_radians(0, -lookSpeed * frameDelta, 0)

    if keys[pygame.K_UP]:
        turnAmount = -lookSpeed * frameDelta
        camera.rotate_euler_radians(turnAmount, 0, 0)
        
        # This checks if the camera exceeded 90 degrees from facing forward, and moves it back if it has.
        if camera.get_distortion_relative().get_contents()[2][2] < 0:
            camera.rotate_euler_radians(-turnAmount, 0, 0)
            
    if keys[pygame.K_DOWN]:
        turnAmount = lookSpeed * frameDelta
        camera.rotate_euler_radians(turnAmount, 0, 0)
        
        if camera.get_distortion_relative().get_contents()[2][2] < 0:
            camera.rotate_euler_radians(-turnAmount, 0, 0)
            


def process_teapot(frameDelta:float, keys):
    rotationSpeed = 1
    
    if keys[pygame.K_b]:
        boom.play()

    teapot.rotate_euler_radians(0, rotationSpeed * frameDelta, 0)
    


def process_lights(frameDelta:float):
    rotationSpeed = -0.8
    
    lightCarousel.rotate_euler_radians(0, rotationSpeed * frameDelta, 0)
    
    

def process_balls():
    for ball in balls:
        ballLocation = ball.objectiveLocation.get_contents()
        
        if (not -2 < ballLocation[1][0] < 6):
            ball.set_location_objective(Matrix([[random.random()],
                                                [0],
                                                [-random.random()]]))
            
            ball.velocity = ORIGIN   
            
            

def process_sensors():
    WINDOW.fill((255, 255, 255))
    camera.render()

    for listener in ROOT.get_substracts_of_type(Listener):
        listener.listen()   

            
pygame.font.init()
font = pygame.font.SysFont(None, 30)

def analyse_framerate(frameDelta:float):
    if frameDelta > 0:
        textSurface = font.render(f"{round(1 / frameDelta, 3)} fps", False, (0, 0, 0))
    else:
        textSurface = font.render("your framerate's 0 somehow", False, (0, 0, 0))
        
    WINDOW.blit(textSurface, (0, 0))
        
    if frameDelta > 1 / 12:
        WINDOW.blit(font.render("ur pc boutta explode", False, (0, 0, 0)), (0, 40))
        



# ---------------- MAIN LOOP ----------------

frameDelta = 0

running = True

while running:
    startTime = time.time()

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    process_player(frameDelta, keys)
    process_teapot(frameDelta, keys)
    process_lights(frameDelta)
    process_balls()

    print(f"\n\n\n\n\n\n\nIntersecting with: {passthroughTest.intersections}")

    physicsDelta = frameDelta / 2
    for i in range(2):
        process_bodies(physicsDelta)
        
    process_sensors()
        
    frameDelta = time.time() - startTime
    
    analyse_framerate(frameDelta)

    pygame.display.flip()