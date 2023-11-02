from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.camera import Camera
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image
from kivy.core.window import Window
import sqlite3
import os
import datetime

class CameraLayout(BoxLayout):
    def capture(self):
        description = self.ids.description_input.text
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        image_path = f'photos/{timestamp}.png'
        self.ids.camera.export_to_png(image_path)
        self.ids.image_preview.source = image_path
        self.save_to_database(image_path, description)
        print(f'Image captured and saved at: {image_path} with description: {description}')

    def view_photos(self):
        # Logic to view photos from the database
        pass

    def save_to_database(self, image_path, description):
        conn = sqlite3.connect('photos.db')
        cursor = conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS photos (id INTEGER PRIMARY KEY AUTOINCREMENT, path TEXT, description TEXT)')
        cursor.execute('INSERT INTO photos (path, description) VALUES (?, ?)', (image_path, description))
        conn.commit()
        conn.close()

class CameraApp(App):
    def build(self):
        Window.size = (480, 800)  # Set the initial window size
        return CameraLayout()

if __name__ == '__main__':
    if not os.path.exists('photos'):
        os.makedirs('photos')
    CameraApp().run()
