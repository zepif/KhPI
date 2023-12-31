import tkinter as tk
import numpy as np
from collections import deque
import yaml

class CoordinateSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordinate System")
        
        global height, width
        with open("config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
            height = config["height"]
            width = config["width"]
        global Ox, Oy
        with open("config.yaml", "r") as config_file:
            config = yaml.safe_load(config_file)
            Ox = config["Ox"]
            Oy = config["Oy"]
        self.canvas = tk.Canvas(self.root, width=width, height=height, bg='white')
        self.canvas.pack()
        
        self.line_entry = tk.Entry(self.root, width=30)
        self.line_entry.insert(0, "x1, y1, x2, y2")
        self.line_entry.pack()
        
        self.circle_entry = tk.Entry(self.root, width=30)
        self.circle_entry.insert(0, "center_x, center_y, radius")
        self.circle_entry.pack()
        
        self.add_line_button = tk.Button(self.root, text="Add Line", command=self.add_line)
        self.add_line_button.pack()
        
        self.add_circle_button = tk.Button(self.root, text="Add Circle", command=self.add_circle)
        self.add_circle_button.pack()

        '''self.delete_line_button = tk.Button(self.root, text="Delete Line", command=self.delete_line)
        self.delete_line_button.pack()
        
        self.delete_circle_button = tk.Button(self.root, text="Delete Circle", command=self.delete_circle)
        self.delete_circle_button.pack()'''

        self.canvas.bind("<Button-1>", self.on_canvas_click)
        self.pixel_grid = [['white' for _ in range(width*2)] for _ in range(height*2)]

        self.draw_coordinate_system()
    
    
    def refresh_canvas(self):
        for y, row in enumerate(self.pixel_grid):
            for x, color in enumerate(row):
                self.canvas.create_rectangle(x, y, x, y, outline=color)
    '''
    def draw_coordinate_system(self):
        for i in range(-Ox // 2, Ox // 2 + 1):
            for x in range(width // 2 + i * width // Ox, width // 2 + i * width // Ox + 1):
                for y in range(height):
                    if (self.check_dot(y, x) == True):
                        self.pixel_grid[y][x] = 'lightgray'

        for i in range(-Oy // 2, Oy // 2 + 1):
            for y in range(height // 2 + i * height // Oy, height // 2 + i * height // Oy + 1):
                for x in range(width):
                    if (self.check_dot(y, x) == True):
                        self.pixel_grid[y][x] = 'lightgray'

        for x in range(width):
            self.pixel_grid[height // 2][x] = 'black'
        for y in range(height):
            self.pixel_grid[y][width // 2] = 'black'

        self.refresh_canvas()
    '''

    def draw_coordinate_system(self):
        for i in range(-Ox//2, Ox//2+1):
            self.canvas.create_line(width//2 + i * width//Ox, 0, width//2 + i * width//Ox, height, fill='lightgray')
            for x in range(width // 2 + i * width // Ox, width // 2 + i * width // Ox + 1):
                for y in range(height):
                    if (self.check_dot(y, x) == True):
                        self.pixel_grid[y][x] = 'lightgray'

        for i in range(-Oy//2, Oy//2+1):
            self.canvas.create_line(0, height//2 + i * height//Oy, width, height//2 + i * height//Oy, fill='lightgray')
            for y in range(height // 2 + i * height // Oy, height // 2 + i * height // Oy + 1):
                for x in range(width):
                    if (self.check_dot(y, x) == True):
                        self.pixel_grid[y][x] = 'lightgray'
        
        self.canvas.create_line(0, height//2, width, height//2, fill='black', width=2)
        self.canvas.create_line(width//2, 0, width//2, height, fill='black', width=2)
        for x in range(width):
            self.pixel_grid[height // 2][x] = 'black'
        for y in range(height):
            self.pixel_grid[y][width // 2] = 'black'

    def check_dot(self, x, y):
        if x >= 0 and x < width and y >= 0 and y < height:
            return True
        else:
            return False

    def draw_line_on_grid(self, x1, y1, x2, y2, color):
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        while x1 != x2 or y1 != y2:
            if self.check_dot(x1, y1) == True:
                self.pixel_grid[y1][x1] = color
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def add_line(self):
        coordinates = self.line_entry.get()
        try:
            x1, y1, x2, y2 = map(float, coordinates.split(','))
            # sigment drawing
            #x1, y1, x2, y2 = x1 * width//10, y1 * height//10, x2 * width//10, y2 * height//10
            #x1, y1, x2, y2 = x1 + width//2, height//2 - y1, x2 + width//2, height//2 - y2
            # line drawing
            x1, y1, x2, y2 = map(float, coordinates.split(','))
            x1, y1, x2, y2 = x1 * width//(Ox), y1 * height//(Oy), x2 * width//(Ox), y2 * height//(Oy)
            x1, y1, x2, y2 = x1 + width//2, height//2 - y1, x2 + width//2, height//2 - y2
            dx, dy = (x2 - x1), (y2 - y1)
            x1, x2, y1, y2 = x1 + dx * 5000, x2 - dx * 5000, y1 + dy * 5000,  y2 - dy * 5000
            self.draw_line_on_grid(x1, y1, x2, y2, 'blue')
            # Pray to god that this works lol
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
        except ValueError:
            print("Invalid input for line coordinates. Please use the format: x1, y1, x2, y2")

    def draw_circle_on_grid(self, center_x, center_y, radius, color):
        x, y = radius, 0
        err = 0

        while x >= y:
            positions = [
                (center_y + y, center_x + x),
                (center_y + x, center_x + y),
                (center_y + x, center_x - y),
                (center_y + y, center_x - x),
                (center_y - y, center_x - x),
                (center_y - x, center_x - y),
                (center_y - x, center_x + y),
                (center_y - y, center_x + x)
            ]
            for pos_y, pos_x in positions:
                if self.check_dot(pos_x, pos_y):
                    self.pixel_grid[pos_y][pos_x] = color

            if err <= 0:
                y += 1
                err += 2 * y + 1
            if err > 0:
                x -= 1
                err -= 2 * x + 1

    def add_circle(self):
        coordinates = self.circle_entry.get()
        try:
            center_x, center_y, radius = map(float, coordinates.split(','))
            center_x, center_y, radius = center_x * width//Ox, center_y * height//Oy, radius
            center_x, center_y = center_x + width//2, height//2 - center_y
            self.draw_circle_on_grid(int(center_x), int(center_y), int(radius * (width / Ox)), 'blue')
            self.canvas.create_oval(center_x - radius * (width / Ox), center_y - radius * (height / Oy),
                                    center_x + radius * (width / Ox), center_y + radius * (height / Oy),
                                    outline='blue', width=2)
        except ValueError:
            print("Invalid input for circle coordinates. Please use the format: center_x, center_y, radius")

    def calculate_area(self, start_x, start_y, fill_color, border_color):
        for x in range(width):
            for y in range(height):
                if self.pixel_grid[y][x] == fill_color:
                    self.pixel_grid[y][x] = 'white'
                    #img = tk.PhotoImage(width=width, height=height)
                    #img.put("#ffffff", (x, y))
        self.refresh_canvas()
        stack = deque([(start_x, start_y)])
        filled = set()
        area = 0

        while stack:
            x, y = stack.pop()

            if (x, y) in filled:
                continue

            if self.pixel_grid[y][x] != border_color:
                if self.pixel_grid[y][x] == 'white':
                    self.pixel_grid[y][x] = fill_color
                #self.pixel_grid[y][x] = fill_color
                area += 1

                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    new_x, new_y = x + dx, y + dy
                    if self.check_dot(new_x, new_y):
                        stack.append((new_x, new_y))
            filled.add((x, y))
            self.canvas.create_rectangle(x, y, x, y, fill=self.pixel_grid[y][x], outline=self.pixel_grid[y][x])

        return area * ((Ox*Oy)/(width*height))

    def on_canvas_click(self, event):
        x, y = event.x, event.y
        fill_color = 'green'
        border_color = 'blue'
        area = self.calculate_area(x, y, fill_color, border_color)
        print(f"Area of the region at ({x}, {y}): {area}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateSystemApp(root)
    root.mainloop()