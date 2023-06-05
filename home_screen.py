# home_screen.py
import os

from kivy.uix.screenmanager import Screen
from kivy_garden.pdfviewer import PDFViewer

class HomeScreen(Screen):
    def open_pdf(self):
        from kivy.uix.filechooser import FileChooserIconView
        self.filechooser = filechooser = FileChooserIconView(path=os.path.join(os.path.dirname(os.path.realpath(__file__)), '..', '..', 'pdf'))
        self.filechooser.bind(on_submit=self.load_pdf)
        self.add_widget(self.filechooser)

    def load_pdf(self, instance, value, touch):
        self.pdfviewer = PDFViewer()
        self.pdfviewer.open(value[0])
        self.pdfviewer.go_to_page(1)
