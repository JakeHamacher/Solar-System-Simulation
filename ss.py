import pygame, pygame_gui
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Solar System \"Simulation\"")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Trail length
TRAIL_LENGTH = 50

# Gravitational constant
G = 10

# Zooming
zoom_level = 1.0
zoom_speed = 0.1
MAX_ZOOM = 5.0
MIN_ZOOM = 0.2

# Planet class
class Planet(pygame.sprite.Sprite):
    def __init__(self, image_path, radius, speed, semi_major_axis, eccentricity, parent=None, angle=0):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (radius * 2, radius * 2))
        self.image = self.original_image.copy()  # Start with the original image
        self.rect = self.image.get_rect()
        self.radius = radius
        self.speed = speed
        self.semi_major_axis = semi_major_axis
        self.eccentricity = eccentricity
        self.angle = angle
        self.x = 0
        self.y = 0
        self.trail = []  # Store the trail of positions
        self.orbit_path = [] # Store the orbit path
        self.x_velocity = 0
        self.y_velocity = 0
        self.selected = False
        self.parent = parent  # Parent planet for moons

    def update(self, simulation_speed=1.0):
        if self.parent:
            # Calculate distance from the parent planet based on elliptical orbit
            dx = self.parent.x - self.x
            dy = self.parent.y - self.y
        else:
            # Calculate distance from the sun based on elliptical orbit
            dx = WIDTH / 2 - self.x
            dy = HEIGHT / 2 - self.y

        r = math.sqrt(dx**2 + dy**2)
        
        # Normalize the direction vector
        dx /= r
        dy /= r
        
        # Calculate gravitational force components
        force = G / r**2
        fx = force * dx
        fy = force * dy
        
        # Update velocity based on gravitational force
        self.x_velocity += fx * simulation_speed
        self.y_velocity += fy * simulation_speed
        
        # Update position based on velocity
        self.x += self.x_velocity * simulation_speed
        self.y += self.y_velocity * simulation_speed
        
        self.rect.center = (int(self.x), int(self.y))

        # Update angle for Keplerian motion
        self.angle += self.speed * simulation_speed

        # Update trail
        self.trail.append((self.x, self.y))
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)
            
        # Update orbit path
        self.orbit_path.append((self.x, self.y))

    def draw_trail(self, screen, zoom_level, offset_x, offset_y):
        scaled_trail = [(x * zoom_level + offset_x, y * zoom_level + offset_y) for x, y in self.trail]
        for i, pos in enumerate(scaled_trail):
            alpha = int((i / len(scaled_trail)) * 255)  # Fade effect
            color = (255, 255, 255, alpha)  # White color with alpha
            if i > 0:
                pygame.draw.line(screen, color, pos, scaled_trail[max(0, i-1)], 3)
                
    def draw_orbit_path(self, screen, zoom_level, offset_x, offset_y):
        scaled_orbit_path = [(x * zoom_level + offset_x, y * zoom_level + offset_y) for x, y in self.orbit_path]
        if len(scaled_orbit_path) > 1:
            pygame.draw.lines(screen, WHITE, False, scaled_orbit_path, 1)

# Sprite groups
all_sprites = pygame.sprite.Group()
planets = pygame.sprite.Group()

# Sun
sun_radius = 50
sun_image_path = "resources/pixel_planet_rho.png"  # Sun
sun = pygame.sprite.Sprite()
sun.image = pygame.image.load(sun_image_path).convert_alpha()
sun.original_image = sun.image.copy()
sun.image = pygame.transform.scale(sun.image, (sun_radius * 2, sun_radius * 2))
sun.rect = sun.image.get_rect()
sun.rect.center = (WIDTH // 2, HEIGHT // 2)
sun.x = WIDTH // 2
sun.y = HEIGHT // 2
all_sprites.add(sun)

# Initial planets with image paths, semi-major axis, and eccentricity
planet_data = [
    ("resources/pixel_planet_epsilon.png", 20, 0.02, 150, 0.2),  # Earth
    ("resources/pixel_planet_iota.png", 15, 0.03, 220, 0.3),   # Mars
    ("resources/pixel_planet_nu.png", 25, 0.01, 300, 0.1), # Jupiter
]

def create_planets():
    jupiter = None
    for image_path, radius, speed, semi_major_axis, eccentricity in planet_data:
        planet = Planet(image_path, radius, speed, semi_major_axis, eccentricity)
        if image_path == "resources/pixel_planet_nu.png":
            jupiter = planet
        planet.x = WIDTH / 2 + semi_major_axis  # Initial position
        planet.y = HEIGHT / 2
        distance = planet.semi_major_axis * (1 - planet.eccentricity**2) / (1 + planet.eccentricity * math.cos(0))
        velocity = math.sqrt(G / distance)  # Circular orbit approximation
        planet.y_velocity = -velocity  # Initial velocity is tangential
        
        all_sprites.add(planet)
        planets.add(planet)
    
    # Add moon orbiting Jupiter
    if jupiter:
        moon = Planet("resources/pixel_planet_mu.png", 5, 0.05, 40, 0.1, parent=jupiter)
        moon.x = jupiter.x + moon.semi_major_axis  # Initial position relative to Jupiter
        moon.y = jupiter.y
        distance = moon.semi_major_axis
        velocity = math.sqrt(G / distance)  # Circular orbit approximation
        moon.y_velocity = -velocity  # Initial velocity is tangential
        all_sprites.add(moon)
        planets.add(moon)

create_planets()

# Pygame GUI manager
manager = pygame_gui.UIManager((WIDTH, HEIGHT))

# Simulation speed control
speed_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((550, 10), (200, 30)),
    start_value=1.0, value_range=(0.0, 50.0),
    manager=manager
)
speed_label = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((450, 10), (150, 30)), text="Speed:", manager=manager)
simulation_speed = 1.0

# Velocity control
velocity_slider = pygame_gui.elements.UIHorizontalSlider(
    relative_rect=pygame.Rect((WIDTH // 2 - 100, HEIGHT - 50), (200, 30)),
    start_value=0.0, value_range=(0.0, -0.5),
    manager=manager,
    visible=False
)
velocity_label = pygame_gui.elements.UILabel(
    relative_rect=pygame.Rect((WIDTH // 2 - 170, HEIGHT - 50), (70, 30)),
    text="Velocity:",
    manager=manager,
    visible=False
)
selected_planet = None

# Reset button
reset_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 10), (100, 30)),
    text='Reset',
    manager=manager
)

# Exit button
exit_button = pygame_gui.elements.UIButton(
    relative_rect=pygame.Rect((10, 50), (100, 30)),
    text='Exit',
    manager=manager
)

# Function to handle planet selection
def select_planet(planet):
    global selected_planet
    if selected_planet:
        selected_planet.selected = False
    selected_planet = planet
    selected_planet.selected = True
    velocity_slider.show()
    velocity_label.show()
    velocity_slider.set_current_value(selected_planet.y_velocity)

# Function to reset the simulation
def reset_simulation():
    global all_sprites, planets, selected_planet
    all_sprites.empty()
    planets.empty()
    all_sprites.add(sun)
    create_planets()
    selected_planet = None
    velocity_slider.hide()
    velocity_label.hide()

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEWHEEL:
            # Zoom in or out based on the direction of the wheel
            if event.y > 0:  # Zoom in
                zoom_level += zoom_speed
            else:  # Zoom out
                zoom_level -= zoom_speed

            # Clamp zoom level to reasonable bounds
            zoom_level = max(MIN_ZOOM, min(zoom_level, MAX_ZOOM))
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_x, mouse_y = event.pos
                for planet in planets:
                    # Check if the mouse click is within the planet's rect
                    if planet.rect.collidepoint(mouse_x, mouse_y):
                        select_planet(planet)
                        break

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == reset_button:
                reset_simulation()
            if event.ui_element == exit_button:
                running = False

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == speed_slider:
                simulation_speed = speed_slider.get_current_value()
            if event.ui_element == velocity_slider:
                if selected_planet:
                    selected_planet.y_velocity = velocity_slider.get_current_value()

        manager.process_events(event)

    # Update
    for planet in planets:
        planet.update(simulation_speed)

    manager.update(time_delta)

    # Calculate the offset to keep the center in the middle of the screen
    offset_x = WIDTH / 2 - (WIDTH / 2) * zoom_level
    offset_y = HEIGHT / 2 - (HEIGHT / 2) * zoom_level

    # Draw
    screen.fill(BLACK)
    
    # Draw orbit paths
    for planet in planets:
        planet.draw_orbit_path(screen, zoom_level, offset_x, offset_y)
    
    # Draw trails
    for planet in planets:
        planet.draw_trail(screen, zoom_level, offset_x, offset_y)
        
    # Draw sun
    sun.image = pygame.transform.scale(sun.original_image, (int(sun_radius * 2 * zoom_level), int(sun_radius * 2 * zoom_level)))
    sun.rect = sun.image.get_rect(center=(int(sun.x * zoom_level + offset_x), int(sun.y * zoom_level + offset_y)))
    screen.blit(sun.image, sun.rect)
    
    # Draw planets
    for planet in planets:
        planet.image = pygame.transform.scale(planet.original_image, (int(planet.radius * 2 * zoom_level), int(planet.radius * 2 * zoom_level)))
        planet.rect = planet.image.get_rect(center=(int(planet.x * zoom_level + offset_x), int(planet.y * zoom_level + offset_y)))
        screen.blit(planet.image, planet.rect)
        
    manager.draw_ui(screen)

    pygame.display.flip()

pygame.quit()
