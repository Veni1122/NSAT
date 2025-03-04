import tkinter as tk


class RangeSlider(tk.Canvas):
    def __init__(self, parent, min_val=0, max_val=100, initial_low=25, initial_high=75, width=300, height=50,
                 callback=None, *args, **kwargs, ):
        super().__init__(parent, width=width, height=height, *args, **kwargs)
        self.callback = callback
        self.min_val = min_val
        self.max_val = max_val
        self.low_val = initial_low
        self.high_val = initial_high
        self.width = width
        self.height = height

        self.slider_width = 20  # Width of slider handles
        self.slider_radius = self.slider_width // 2

        self.bind("<B1-Motion>", self.move_slider)
        self.bind("<Button-1>", self.click_slider)

        self.draw_slider()

    def draw_slider(self):
        self.delete("slider")

        # Calculate positions for low and high values
        low_x = self.value_to_position(self.low_val)
        high_x = self.value_to_position(self.high_val)

        # Draw the slider background
        self.create_line(10, self.height // 2, self.width - 10, self.height // 2, fill="gray", width=4, tags="slider")

        # Draw the active range
        self.create_line(low_x, self.height // 2, high_x, self.height // 2, fill="blue", width=6, tags="slider")

        # Draw the low value handle
        self.create_oval(
            low_x - self.slider_radius,
            self.height // 2 - self.slider_radius,
            low_x + self.slider_radius,
            self.height // 2 + self.slider_radius,
            fill="blue",
            tags=("slider", "low"),
        )

        # Draw the high value handle
        self.create_oval(
            high_x - self.slider_radius,
            self.height // 2 - self.slider_radius,
            high_x + self.slider_radius,
            self.height // 2 + self.slider_radius,
            fill="blue",
            tags=("slider", "high"),
        )

    def value_to_position(self, value):
        """Convert a value to a canvas position."""
        return 10 + ((value - self.min_val) / (self.max_val - self.min_val)) * (self.width - 20)

    def position_to_value(self, x):
        """Convert a canvas position to a value."""
        return self.min_val + ((x - 10) / (self.width - 20)) * (self.max_val - self.min_val)

    def move_slider(self, event):
        """Move the slider handle."""
        x = event.x
        if x < 10:
            x = 10
        if x > self.width - 10:
            x = self.width - 10

        clicked = self.find_closest(event.x, event.y)[0]
        tags = self.gettags(clicked)

        if "low" in tags:
            new_val = self.position_to_value(x)
            if new_val < self.high_val:
                self.low_val = new_val
        elif "high" in tags:
            new_val = self.position_to_value(x)
            if new_val > self.low_val:
                self.high_val = new_val
        if self.callback:
            self.callback(self.get_range())
        self.draw_slider()

    def click_slider(self, event):
        self.move_slider(event)

    def get_range(self):
        """Get the selected range."""
        return round(self.low_val), round(self.high_val)
