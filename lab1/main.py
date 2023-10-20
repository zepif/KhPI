import tkinter as tk

class CoordinateSystemApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Coordinate System")
        
        global height, width
        height, width = 640, 640
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
        
        self.draw_coordinate_system()
        
    def draw_coordinate_system(self):
        for i in range(-5, 6):
            self.canvas.create_line(width//2 + i * width//10, 0, width//2 + i * width//10, height, fill='lightgray')
            self.canvas.create_line(0, height//2 + i * height//10, width, height//2 + i * height//10, fill='lightgray')
        
        self.canvas.create_line(0, height//2, width, height//2, fill='black', width=2)
        self.canvas.create_line(width//2, 0, width//2, height, fill='black', width=2)

    def add_line(self):
        coordinates = self.line_entry.get()
        try:
            x1, y1, x2, y2 = map(float, coordinates.split(','))
            # sigment drawing
            #x1, y1, x2, y2 = x1 * width//10, y1 * height//10, x2 * width//10, y2 * height//10
            #x1, y1, x2, y2 = x1 + width//2, height//2 - y1, x2 + width//2, height//2 - y2
            # line drawing
            x1, y1, x2, y2 = map(float, coordinates.split(','))
            x1, y1, x2, y2 = x1 * width//10, y1 * height//10, x2 * width//10, y2 * height//10
            x1, y1, x2, y2 = x1 + width//2, height//2 - y1, x2 + width//2, height//2 - y2
            dx, dy = (x2 - x1), (y2 - y1)
            x1, x2, y1, y2 = x1 + dx * 5000, x2 - dx * 5000, y1 + dy * 5000,  y2 - dy * 5000
            self.canvas.create_line(x1, y1, x2, y2, fill='blue', width=2)
        except ValueError:
            print("Invalid input for line coordinates. Please use the format: x1, y1, x2, y2")

    def add_circle(self):
        coordinates = self.circle_entry.get()
        try:
            center_x, center_y, radius = map(float, coordinates.split(','))
            center_x, center_y, radius = center_x * width//10, center_y * height//10, radius * (height+width)//20
            center_x, center_y = center_x + width//2, height//2 - center_y
            self.canvas.create_oval(center_x - radius, center_y - radius, center_x + radius, center_y + radius, outline='red', width=2)
        except ValueError:
            print("Invalid input for circle coordinates. Please use the format: center_x, center_y, radius")

if __name__ == "__main__":
    root = tk.Tk()
    app = CoordinateSystemApp(root)
    root.mainloop()
