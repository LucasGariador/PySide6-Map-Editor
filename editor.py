import sys
import json
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QGridLayout, 
                               QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, 
                               QLabel, QSpinBox, QLineEdit) # Importamos QLineEdit
from PySide6.QtCore import Qt

class MapEditor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("3D Pipeline - Level Editor Demo")
        self.cols = 10 
        self.rows = 10 
        self.map_data = []
        
        self.initUI()
        self.rebuild_grid(self.rows, self.cols)

    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.main_layout = QVBoxLayout(central_widget)
        
        # --- Controles Superiores ---
        control_layout = QHBoxLayout()
        control_layout.addWidget(QLabel("Width (X):"))
        self.spin_width = QSpinBox()
        self.spin_width.setRange(5, 50)
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
        
        control_layout.addStretch() 
        self.main_layout.addLayout(control_layout)
        
        # --- Contenedor de la grilla ---
        self.grid_layout = QGridLayout()
        self.grid_layout.setSpacing(1)
        self.main_layout.addLayout(self.grid_layout)

        # --- Leyenda de colores ---
        self.add_legend()
        
        # --- Sección de Exportar ---
        export_layout = QHBoxLayout()
        self.filename_input = QLineEdit("level_data.json")
        export_layout.addWidget(QLabel("Filename:"))
        export_layout.addWidget(self.filename_input)
        
        export_btn = QPushButton("Export Level to JSON")
        export_btn.setStyleSheet("background-color: #4CAF50; color: white; font-weight: bold; padding: 10px;")
        export_btn.clicked.connect(self.export_to_json)
        export_layout.addWidget(export_btn)
        
        self.main_layout.addLayout(export_layout)

    def add_legend(self):
        legend_layout = QHBoxLayout()
        legend_layout.addWidget(QLabel("Legend: "))
        
        colors = {0: "Empty", 1: "Wall", 2: "Floor", 3: "Health", 4: "Ammo", 5: "", 6: "", 7: "Player", 8: "", 9 : "Enemy"}
        
        for val, name in colors.items():
            lbl = QLabel(f"{val}:{name}")
            bColors = {
            0: "white", 1: "black", 2: "gray", 3: "darkred",
            4: "blue", 5: "green", 6: "gold", 7: "purple", 8: "darkgreen", 9: "red"
        }
            lbl.setStyleSheet(f"background-color: {bColors[val]}; color: {'white' if val==1 else 'black'}; padding: 3px; border: 1px solid gray;")
            legend_layout.addWidget(lbl)
            
        self.main_layout.addLayout(legend_layout)

    def on_resize_clicked(self):
        new_w = self.spin_width.value()
        new_h = self.spin_height.value()
        self.rebuild_grid(new_h, new_w)

    def rebuild_grid(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.map_data = [[0 for _ in range(cols)] for _ in range(rows)]
        self.buttons = []
        
        # 1. Limpiar la grilla anterior
        while self.grid_layout.count():
            child = self.grid_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # --- SOLUCIÓN: Anclar la grilla arriba a la izquierda ---
        self.grid_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        
        # 2. Crear los nuevos botones dinámicamente
        for r in range(rows):
            row_btns = []
            for c in range(cols):
                btn = QPushButton("0")
                btn.setFixedSize(30, 30)
                btn.clicked.connect(lambda checked, r=r, c=c: self.cycle_tile(r, c))
                btn.setStyleSheet("background-color: white; border: 1px solid gray;")
                self.grid_layout.addWidget(btn, r, c)
                row_btns.append(btn)
            self.buttons.append(row_btns)
            
        # --- SOLUCIÓN: Ajustar el tamaño de la ventana al contenido ---
        self.adjustSize()

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
        filename = self.filename_input.text()
        if not filename.endswith(".json"):
            filename += ".json"
            
        export_data = {
            "version": "1.1",
            "width": self.cols,
            "height": self.rows,
            "map": self.map_data
        }
        
        try:
            with open(filename, "w") as f:
                json.dump(export_data, f, indent=4)
            QMessageBox.information(self, "Success", f"Map exported to {filename}!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Could not save file: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapEditor()
    window.show()
    sys.exit(app.exec())