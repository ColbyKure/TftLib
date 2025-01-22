import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLineEdit, QLabel, QGridLayout
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

class TFTCalculator(QWidget):
    def __init__(self):
        super().__init__()

        # Set the window title and size
        self.setWindowTitle('TFT 4-Cost 3-Star Probability Calculator')
        self.setFixedSize(400, 300)

        # Set a professional font for the entire application
        self.setFont(QFont('Arial', 12))

        # Set dark background for the window
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        # Data Sheet for Shop Odds and Champions
        self.data_sheet = self.create_data_sheet()

        # Main Layout using GridLayout
        self.layout = QGridLayout()
        self.layout.setSpacing(10)

        # Player Level Input with explanation
        self.level_label = QLabel('Player Level (4-10):')
        self.level_input = QLineEdit()
        self.level_input.setPlaceholderText('Enter your level (4-10)')
        self.level_input.setToolTip('Input your current player level (from 4 to 10).')

        # Gold Input with explanation
        self.gold_label = QLabel('Available Gold:')
        self.gold_input = QLineEdit()
        self.gold_input.setPlaceholderText('Enter your available gold')
        self.gold_input.setToolTip('Input the amount of gold you have for rerolls.')

        # Custom Champion Drop Rate Input with explanation
        self.champion_label = QLabel('4-Cost Champion Drop Rate (%):')
        self.champion_input = QLineEdit()
        self.champion_input.setPlaceholderText('Enter drop rate for 4-cost champion')
        self.champion_input.setToolTip('Input the drop rate (as a percentage) of getting a 4-cost champion.')

        # Calculate Button
        self.calculate_button = QPushButton('Calculate Probability')
        self.calculate_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        self.calculate_button.clicked.connect(self.calculate_probability)

        # Result Label
        self.result_label = QLabel('Probability: ')
        self.result_label.setAlignment(Qt.AlignCenter)

        # Adding widgets to the layout in a grid format
        self.layout.addWidget(self.level_label, 0, 0)
        self.layout.addWidget(self.level_input, 0, 1)
        self.layout.addWidget(self.gold_label, 1, 0)
        self.layout.addWidget(self.gold_input, 1, 1)
        self.layout.addWidget(self.champion_label, 2, 0)
        self.layout.addWidget(self.champion_input, 2, 1)
        self.layout.addWidget(self.calculate_button, 3, 0, 1, 2)
        self.layout.addWidget(self.result_label, 4, 0, 1, 2)

        # Set Layout
        self.setLayout(self.layout)

    def calculate_probability(self):
        try:
            level = int(self.level_input.text())
            gold = int(self.gold_input.text())
            champion_odds = float(self.champion_input.text())

            if level < 4 or level > 10:
                self.result_label.setText('Level must be between 4 and 10.')
                return

            # Get the shop odds for the specified level and champion cost
            odds = self.get_shop_odds(level, champion_odds)

            # Calculate the number of rolls
            cost_per_roll = 2  # Can be adjusted for a more accurate model
            rolls = gold // cost_per_roll

            # Calculate the probability of hitting a 3-star for the custom champion
            p = odds / 100  # Convert percentage to decimal
            probability = 1 - (1 - p)**rolls

            # Display the result
            self.result_label.setText(f'Probability of 3-Star: {probability * 100:.2f}%')
        except ValueError:
            self.result_label.setText('Please enter valid numbers.')

    def get_shop_odds(self, level, champion_odds):
        """Fetches the probability of getting a 4-cost champion at a given level."""
        level_odds = self.data_sheet.get(level, {})
        return level_odds.get(4, champion_odds)  # Defaults to provided champion odds

    def create_data_sheet(self):
        """Creates a static data sheet for TFT odds and champions."""
        return {
            4: {  # Level 4
                1: 55,  # 50% chance of getting 1-cost champions
                2: 30,  # 30% chance of getting 2-cost champions
                3: 15,  # 15% chance of getting 3-cost champions
                4: 0,   # 5% chance of getting 4-cost champions
            },
            5: {  # Level 5
                1: 45,
                2: 33,
                3: 20,
                4: 2,
            },
            6: {  # Level 6
                1: 30,
                2: 40,
                3: 25,
                4: 5,
            },
            7: {  # Level 7
                1: 19,
                2: 30,
                3: 40,
                4: 10,
            },
            8: {  # Level 8
                1: 18,
                2: 25,
                3: 32,
                4: 22,
            },
            9: {  # Level 9
                1: 15,
                2: 20,
                3: 25,
                4: 30,
            },
            10: {  # Level 10
                1: 5,
                2: 10,
                3: 20,
                4: 40,
            },
        }

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TFTCalculator()
    window.show()
    sys.exit(app.exec_())
