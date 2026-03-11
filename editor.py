import sys
import json
from PySide6.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QVBoxLayout, QMessageBox

class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("IKEA 3D Pipeline - Level Editor Demo")
        self.grid_size = 10 # Tamaño del mapa 10x10
        # Matriz 2D llena de ceros (espacio vacío)
        self.map_data = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        
        self.initUI()

    def initUI(self):
        # Widget principal y Layouts
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        
        # Layout de la grilla (el mapa)
        grid_layout = QGridLayout()
        grid_layout.setSpacing(1) # Espacio entre los "tiles"
        self.buttons = []
        
        # Crear los botones del mapa
        for r in range(self.grid_size):
            row_btns = []
            for c in range(self.grid_size):
                btn = QPushButton("0")
                btn.setFixedSize(40, 40)
                # Al hacer clic, llama a la función para cambiar el tipo de tile (pared, jugador, etc.)
                btn.clicked.connect(lambda checked, r=r, c=c: self.cycle_tile(r, c))
                
                # Colores básicos para que se vea bien
                btn.setStyleSheet("background-color: white; border: 1px solid gray;")
                
                grid_layout.addWidget(btn, r, c)
                row_btns.append(btn)
            self.buttons.append(row_btns)
            
        main_layout.addLayout(grid_layout)
        
        # Botón para exportar a JSON (Lo que leerá tu C++)
        export_btn = QPushButton("Export Level to JSON")
        export_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        export_btn.clicked.connect(self.export_to_json)
        main_layout.addWidget(export_btn)

    def cycle_tile(self, r, c):
        # Cicla entre los valores 0 al 7
        self.map_data[r][c] = (self.map_data[r][c] + 1) % 8
        val = self.map_data[r][c]
        
        self.buttons[r][c].setText(str(val))
        
        # Cambiar colores según el valor para feedback visual
        colors = {
            0: "white",        # Vacío
            1: "black",        # Pared 1
            2: "gray",         # Pared 2
            3: "darkred",      # Puerta
            4: "blue",         # Player Spawn
            5: "green",        # Pickup / Munición
            6: "gold",         # Tesoro
            7: "purple"        # Enemigo
        }
        text_color = "white" if val not in [0, 6] else "black"
        self.buttons[r][c].setStyleSheet(f"background-color: {colors[val]}; color: {text_color}; border: 1px solid gray;")

    def export_to_json(self):
        # Guarda el mapa en un formato fácil de parsear en C++
        export_data = {
            "version": "1.0",
            "size": self.grid_size,
            "map": self.map_data
        }
        
        with open("level_data.json", "w") as f:
            json.dump(export_data, f, indent=4)
            
        # Mostrar alerta de éxito
        msg = QMessageBox()
        msg.setWindowTitle("Export Successful")
        msg.setText("level_data.json has been created in your project folder!\n\nReady for the C++ engine.")
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEditor()
    window.show()
    sys.exit(app.exec())