import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                               QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, 
                               QLabel, QSpinBox)

class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Pipeline - Level Editor Demo")
        # Empezamos con un tamaño por defecto
        self.cols = 10 
        self.rows = 10 
        self.map_data = []
        
        self.initUI()
        self.rebuild_grid(self.rows, self.cols) # Dibuja la grilla inicial

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # --- NUEVO: Barra de controles superior ---
        control_layout = QHBoxLayout()
        
        control_layout.addWidget(QLabel("Width (X):"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(5, 50) # Límite de 5 a 50 bloques
        self.spin_width.setValue(self.cols)
        control_layout.addWidget(self.spin_width)
        
        control_layout.addWidget(QLabel("Height (Y):"))
        self.spin_height = QSpinBox()
        self.spin_height.setRange(5, 50)
        self.spin_height.setValue(self.rows)
        control_layout.addWidget(self.spin_height)
        
        resize_btn = QPushButton("Resize Map")
        resize_btn.clicked.connect(self.on_resize_clicked)
        control_layout.addWidget(resize_btn)
        
        control_layout.addStretch() # Empuja los controles hacia la izquierda
        self.main_layout.addLayout(control_layout)
        
        # --- Contenedor de la grilla ---
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.main_layout.addLayout(self.grid_layout)
        
        # Botón de exportar
        export_btn = QPushButton("Export Level to JSON")
        export_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px; margin-top: 10px;")
        export_btn.clicked.connect(self.export_to_json)
        self.main_layout.addWidget(export_btn)

    def on_resize_clicked(self):
        # Lee los valores de las cajitas y reconstruye
        new_w = self.spin_width.value()
        new_h = self.spin_height.value()
        self.rebuild_grid(new_h, new_w)

    def rebuild_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.map_data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = []
        
        # 1. Limpiar la grilla anterior (Clave para evitar memory leaks)
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
                
        # 2. Crear los nuevos botones dinámicamente
        for r in range(rows):
            row_btns = []
            for c in range(cols):
                btn = QPushButton("0")
                btn.setFixedSize(30, 30) # Un poco más chico para que entren mapas más grandes
                btn.clicked.connect(lambda checked, r=r, c=c: self.cycle_tile(r, c))
                btn.setStyleSheet("background-color: white; border: 1px solid gray;")
                self.grid_layout.addWidget(btn, r, c)
                row_btns.append(btn)
            self.buttons.append(row_btns)

    def cycle_tile(self, r, c):
        self.map_data[r][c] = (self.map_data[r][c] + 1) % 8
        val = self.map_data[r][c]
        self.buttons[r][c].setText(str(val))
        
        colors = {
            0: "white", 1: "black", 2: "gray", 3: "darkred",
            4: "blue", 5: "green", 6: "gold", 7: "purple"
        }
        text_color = "white" if val not in [0, 6] else "black"
        self.buttons[r][c].setStyleSheet(f"background-color: {colors[val]}; color: {text_color}; border: 1px solid gray;")

    def export_to_json(self):
        export_data = {
            "version": "1.1",
            "width": self.cols,
            "height": self.rows,
            "map": self.map_data
        }
        with open("level_data.json", "w") as f:
            json.dump(export_data, f, indent=4)
            
        msg = QMessageBox()
        msg.setWindowTitle("Export Successful")
        msg.setText(f"Map ({self.cols}x{self.rows}) exported to level_data.json!")
        msg.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEditor()
    window.show()
    sys.exit(app.exec())