import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel("", self)
        self.emoji_label = QLabel("", self)
        self.description_label = QLabel("", self)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.get_weather_button.setObjectName("get_weather_button")

        self.setStyleSheet("""
                            QLabel, QPushButton{
                                font-family: calibri;
                            }
                        
                           QLabel#city_label{
                                font-size: 40px;
                                font-style: italic;
                           }

                           QLineEdit#city_input{
                                font-size: 40px;

                           }

                           QPushButton#get_weather_button{
                                font-size: 30px;
                                font-weight: bold;
                           }
                           QLabel#temperature_label{
                                font-size: 75px;
                           }

                           QLabel#emoji_label{
                                font-size: 100px;
                                font-family: Segoe UI Emoji
                           }

                           QLabel#description_label{
                                font-size: 50px;
                           
                           }
                        """)

        self.get_weather_button.clicked.connect(self.get_weather)

    def get_weather(self):
        API_KEY =  "4779a383e5fda800b1d0e38de7bb8543"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data["cod"] == 200:
                self.display_weather(data)
        
        except requests.exceptions.HTTPError as http_error:
            match response.status_code:
                case 404:
                    self.display_error("Not found!")
                case _:
                    self.display_error("An error occured!")
        except requests.exceptions.RequestException:
            self.display_error("An error occured!")

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.setText("")
        self.description_label.setText("")

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px;")
        temp_k = data["main"]["temp"]
        temp_c = temp_k - 273.15

        self.temperature_label.setText(str(f"{temp_c:.0f}°C"))

        weather_description = data["weather"][0]["description"]
        self.description_label.setText(weather_description)

        weather_id = data["weather"][0]["id"]
        self.emoji_label.setText(self.display_weather_emoji(weather_id))

    @staticmethod
    def display_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weatherapp = WeatherApp()
    weatherapp.show()
    sys.exit(app.exec_())