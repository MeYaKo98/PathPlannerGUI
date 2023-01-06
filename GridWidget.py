import numpy as np
from PyQt5.QtWidgets import QWidget, QGridLayout, QPushButton, QFileDialog, QLabel, QLineEdit, QHBoxLayout, QVBoxLayout, QSpacerItem, QSizePolicy, QCheckBox
from PyQt5.QtCore import Qt
from PIL import Image, ImageDraw
from A_star import A_star

class GridDialog(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # create a label and a line edit for the width of the grid
        width_label = QLabel("Width:")
        self.width_edit = QLineEdit()
        self.width_edit.setText('10')
        # create a label and a line edit for the height of the grid
        height_label = QLabel("Height:")
        self.height_edit = QLineEdit()
        self.height_edit.setText('10')
        #
        cell_size_label = QLabel("Cell size:")
        self.cell_size_edit = QLineEdit()
        self.cell_size_edit.setText('60')
        # create a create button
        create_button = QPushButton("Create")
        create_button.clicked.connect(self.create_grid)

        # create a grid layout and add the widgets to it
        layout = QGridLayout()
        layout.addWidget(width_label, 0, 0)
        layout.addWidget(self.width_edit, 0, 1)
        layout.addWidget(height_label, 1, 0)
        layout.addWidget(self.height_edit, 1, 1)
        layout.addWidget(cell_size_label, 2, 0)
        layout.addWidget(self.cell_size_edit, 2, 1)
        layout.addWidget(create_button, 3, 0, 1, 3)


        # set the layout and the window title
        self.setLayout(layout)
        self.setWindowTitle("Create Grid")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Return:
            self.create_grid()

    def create_grid(self):
        # get the width and height from the line edits
        width = int(self.width_edit.text())
        height = int(self.height_edit.text())
        cell_size = int(self.cell_size_edit.text())
        # create a new grid widget with the specified size
        self.grid_widget = GridWidget(width, height, cell_size)
        self.grid_widget.show()
        self.grid_widget.setFixedSize(self.grid_widget.size())
        self.grid_widget.show()
        self.close()

class GridWidget(QWidget):
    def __init__(self, width, height, cell_size):
        super().__init__()
        self.initUI(width, height, cell_size)

    def initUI(self, width, height, cell_size):
        layout = QHBoxLayout()
        # create a grid layout
        grid = QGridLayout()
        # create a button for each cell in the grid
        self.buttons = []
        for i in range(height):
            self.buttons.append([])
            for j in range(width):
                button = QPushButton()
                button.setMinimumHeight(cell_size)
                button.setMaximumHeight(cell_size)
                button.setMaximumWidth(cell_size)
                button.setMinimumWidth(cell_size)
                button.setCheckable(True)
                button.setStyleSheet("QPushButton{background-color : white} QPushButton::checked{background-color : black;}")
                button.clicked.connect(self.update_last_cell)
                grid.addWidget(button, i, j)
                self.buttons[i].append(button)
        # create load and save buttons
        buttons = QVBoxLayout()
        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_grid)
        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_grid)
        buttons.addWidget(load_button)
        buttons.addWidget(save_button)
        # create start and end buttons
        start_button = QPushButton("Start")
        start_button.clicked.connect(self.set_start)
        self.start_flag = False
        end_button = QPushButton("Finish")
        end_button.clicked.connect(self.set_end)
        self.end_flag = False
        buttons.addWidget(start_button)
        buttons.addWidget(end_button)
        spaceItem = QSpacerItem(100, 100,QSizePolicy.Maximum , QSizePolicy.Expanding)
        buttons.addSpacerItem(spaceItem)
        #autosolve checkbox
        self.auto_solve = QCheckBox()
        self.auto_solve.setText("Auto Solve")
        self.auto_solve.setChecked(1)
        buttons.addWidget(self.auto_solve)
        #solve button
        solve_button = QPushButton("Solve")
        solve_button.clicked.connect(self.solve)
        buttons.addWidget(solve_button)
        # set the layout and the window title
        layout.addLayout(grid)
        layout.addLayout(buttons)
        self.setLayout(layout)
        self.setWindowTitle("Custom Grid")

        # initialize the start and end positions to None
        self.start = (0,0)
        self.buttons[0][0].setStyleSheet("background-color: red")
        self.buttons[0][0].setCheckable(False)
        self.buttons[0][0].setText('Start')
        self.end = (height-1, width-1)
        self.buttons[height-1][width-1].setStyleSheet("background-color: green")
        self.buttons[height-1][width-1].setText('Finish')
        self.buttons[height-1][width-1].setCheckable(False)
        

    def load_grid(self):
        # open a file dialog to select a PNG file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_name:
            # load the image
            image = Image.open(file_name)
            # get the width and height of the image
            width, height = image.size
            # check if the image has the same size as the grid
            if width != len(self.buttons) or height != len(self.buttons[0]):
                return
            # iterate over the pixels in the image and set the corresponding button to checked if the pixel is black
            for i in range(height):
                for j in range(width):
                    if image.getpixel((j, i)) == (0, 0, 0):
                        self.buttons[i][j].setChecked(True)
                    else:
                        self.buttons[i][j].setChecked(False)
        self.grid_clear_path()
        self.step_counter = 0

    def save_grid(self):
        # open a file dialog to select a file name for the PNG file
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", "PNG Files (*.png);;All Files (*)", options=options)
        if file_name:
            # create a new image with the same size as the grid
            image = Image.new("RGB", (len(self.buttons), len(self.buttons[0])))
            draw = ImageDraw.Draw(image)
            # iterate over the buttons and draw a black pixel in the image if the button is checked
            for i in range(len(self.buttons)):
                for j in range(len(self.buttons[i])):
                    if not(self.buttons[i][j].isChecked()):
                        draw.point((j, i), (255, 255, 255))
            # save the image
            image.save(file_name)

    def update_last_cell(self):
        last_cell = self.sender()
        if (self.start_flag):
            for i in range(len(self.buttons)):
                for j in range(len(self.buttons[i])):
                    if self.buttons[i][j] == last_cell:
                        self.start = (i, j)
                        # change the color of the start button
                        last_cell.setStyleSheet("background-color: red")
                        last_cell.setCheckable(False)
                        last_cell.setText('Start')
                        self.start_flag = False
                        break
        if (self.end_flag):
            for i in range(len(self.buttons)):
                for j in range(len(self.buttons[i])):
                    if self.buttons[i][j] == last_cell:
                        self.end = (i, j)
                        # change the color of the start button
                        last_cell.setStyleSheet("background-color: green")
                        last_cell.setText('Finish')
                        last_cell.setCheckable(False)
                        self.end_flag = False
                        break
        if self.auto_solve.isChecked():
            self.automatic_solve()
        else:
            self.grid_clear_path()

        self.step_counter = 0

    def set_start(self):
        # reset the starting position
        if (self.start):
            self.buttons[self.start[0]][self.start[1]].setCheckable(True)
            self.buttons[self.start[0]][self.start[1]].setStyleSheet("QPushButton{background-color : white} QPushButton::checked{background-color : black;}")
            self.buttons[self.start[0]][self.start[1]].setText('')
        #wait for the cell to be pressed
        self.start_flag = True
        self.end_flag = False

    def set_end(self):
        # set the end position to the position of the button that was clicked
        if (self.end):
            self.buttons[self.end[0]][self.end[1]].setCheckable(True)
            self.buttons[self.end[0]][self.end[1]].setStyleSheet("QPushButton{background-color : white} QPushButton::checked{background-color : black;}")
            self.buttons[self.end[0]][self.end[1]].setText('')
        #wait for the cell to be pressed
        self.end_flag = True
        self.start_flag = False

    def get_grid(self):
        # create a grid with the same size as the button grid
        grid = np.zeros((len(self.buttons), len(self.buttons[0])))
        # iterate over the buttons and set the value in the grid to 1 if the button is checked
        for i in range(len(self.buttons)):
            for j in range(len(self.buttons[i])):
                if self.buttons[i][j].isChecked():
                    grid[i, j] = 1
        # return the grid and the start and end positions
        return grid, self.start, self.end

    def grid_clear_path(self):
        for i in range(len(self.buttons)):
            for j in range (len(self.buttons[i])):
                self.buttons[i][j].setStyleSheet("QPushButton{background-color : white} QPushButton::checked{background-color : black;}")
                self.buttons[i][j].setText('')
        self.buttons[self.start[0]][self.start[1]].setStyleSheet("QPushButton{background-color : red}")
        self.buttons[self.start[0]][self.start[1]].setText("Start")
        self.buttons[self.end[0]][self.end[1]].setStyleSheet("QPushButton{background-color : green}")
        self.buttons[self.end[0]][self.end[1]].setText("Finish")

    def automatic_solve(self):
        self.grid_clear_path()
        temp = self.get_grid()
        path, reached_set, _ = A_star(temp[0],temp[1],temp[2])
        reached_set.remove(self.start)
        if path:
            reached_set.remove(self.end)
        for reached in reached_set:
            self.buttons[reached[0]][reached[1]].setStyleSheet("QPushButton{background-color : yellow} QPushButton::checked{background-color : black;}")
        if path:
            for step in path[1:len(path)-1]:
                self.buttons[step[0]][step[1]].setStyleSheet("QPushButton{background-color : blue} QPushButton::checked{background-color : black;}")
    
    def solve(self):
        try : 
            self.step_counter
        except:
            self.step_counter = 0
        if self.step_counter == 0:
            self.grid_clear_path()
        temp = self.get_grid()
        path, reached_set, sequence = A_star(temp[0],temp[1],temp[2])
        if (self.step_counter<len(sequence)-1):    
            step = sequence[self.step_counter]
            (coordinates, neighbors) = step
            if not (coordinates==self.start or coordinates==self.end):
                self.buttons[coordinates[0]][coordinates[1]].setStyleSheet("QPushButton{background-color : orange} QPushButton::checked{background-color : black;}")
            for neighbor in neighbors:
                (g_score,f_score) = neighbors[neighbor]
                if not (neighbor==self.start or neighbor==self.end):
                    self.buttons[neighbor[0]][neighbor[1]].setStyleSheet("QPushButton{background-color : yellow} QPushButton::checked{background-color : black;}")
                    self.buttons[neighbor[0]][neighbor[1]].setText("H: "+str(int((f_score-g_score)*10))+"\nG: "+str(int(g_score*10))+"\n"+ str(int(10*f_score)))
            self.step_counter = self.step_counter + 1
        else:
            if path:
                for step in path[1:len(path)-1]:
                    self.buttons[step[0]][step[1]].setStyleSheet("QPushButton{background-color : blue} QPushButton::checked{background-color : black;}")