from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsPixmapItem
from PyQt5.QtGui import QPen, QBrush, QColor, QPixmap
from PyQt5.QtCore import QRectF, Qt

class CraftingTableWidget(QGraphicsView):
    def __init__(self, rows=3, cols=3, cell_size=80, parent=None):
        super().__init__(parent)
        self.rows = rows
        self.cols = cols
        self.cell_size = cell_size
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self._draw_grid()
        self.items = {}

    def _draw_grid(self):
        pen = QPen(QColor("black"))
        brush = QBrush(QColor("lightgray"))
        for row in range(self.rows):
            for col in range(self.cols):
                rect = QRectF(col * self.cell_size, row * self.cell_size, self.cell_size, self.cell_size)
                cell = QGraphicsRectItem(rect)
                cell.setPen(pen)
                cell.setBrush(brush)
                self.scene.addItem(cell)

    def update_from_ast(self, recipe_ast):

        for item in self.items.values():
            self.scene.removeItem(item)
        self.items.clear()

        for item in recipe_ast.get("input", []):
            position = item["position"]
            quantity = item["quantity"]
            material = item["material"]
            try:
                row, col = int(position[0]), int(position[1])
            except Exception as e:
                print(f"Invalid position format for item: {item}")
                continue
            image_path = f"resources/images/{material}.png"
            pixmap = QPixmap(image_path)
            if pixmap.isNull():
                print(f"Image not found for material: {material}")
                continue

            pixmap = pixmap.scaled(self.cell_size - 10, self.cell_size - 10, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            pixmap_item = QGraphicsPixmapItem(pixmap)

            x = col * self.cell_size + (self.cell_size - pixmap.width()) / 2
            y = row * self.cell_size + (self.cell_size - pixmap.height()) / 2
            pixmap_item.setPos(x, y)

            self.scene.addItem(pixmap_item)
            self.items[(row, col)] = pixmap_item