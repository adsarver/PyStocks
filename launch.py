import kivy
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.graphics.texture import Texture
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import threading
import time

class MatplotlibWidget(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.fig)
        self.texture = None
        self.data = []

        # Start a thread to update the data
        self._update_thread = threading.Thread(target=self.update_data, daemon=True)
        self._update_thread.start()

        Clock.schedule_interval(self.update_plot, 1.0 / 30.0)

    def update_data(self):
        # Simulate live data update
        while True:
            self.data.append(np.random.random())
            if len(self.data) > 100:
                self.data.pop(0)
            time.sleep(0.1)

    def update_plot(self, dt):
        self.ax.clear()
        self.ax.plot(self.data, 'r-')
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

        buf = np.fromstring(self.fig.canvas.tostring_rgb(), dtype=np.uint8)
        buf = buf.reshape(self.fig.canvas.get_width_height()[::-1] + (3,))

        self.texture = Texture.create(size=self.fig.canvas.get_width_height(), colorfmt='rgb')
        self.texture.blit_buffer(buf.tostring(), colorfmt='rgb', bufferfmt='ubyte')

        with self.canvas:
            self.canvas.clear()
            self.canvas.add(self.texture)

class MyApp(App):
    def build(self):
        layout = BoxLayout()
        self.matplotlib_widget = MatplotlibWidget()
        layout.add_widget(self.matplotlib_widget)
        return layout

if __name__ == '__main__':
    MyApp().run()
