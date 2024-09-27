from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QWidget, QDialog,QListWidget
from PyQt6 import uic
import sys
import os
import logging
from PyQt6 import QtWidgets
import webbrowser

class AccountWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None, username=None, password=None):
        super().__init__(parent)
        uic.loadUi("Account.ui", self)
        self.setWindowTitle("Your Account")
        self.username = username
        self.password = password
        self.parent_window = parent

        # Connect delete button
        self.delete_button = self.findChild(QtWidgets.QPushButton, "delete_2")
        if self.delete_button:
            self.delete_button.clicked.connect(self.delete_account)

        # Connect widget for sign out confirmation
        self.widget_6 = self.findChild(QtWidgets.QWidget, "widget_6")
        if self.widget_6:
            self.widget_6.mousePressEvent = self.show_sign_out_confirmation

    def delete_account(self):
        reply = QMessageBox.question(self, 'Confirm Account Deletion',
                                     'Are you sure you want to delete your account?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.remove_user_from_files()
            QMessageBox.information(self, 'Account Deleted', 'Account removed successfully.')
            self.close()
            self.parent_window.show_signup_page()

    def remove_user_from_files(self):
        self.remove_line_from_file("usernames.txt", self.username)
        self.remove_line_from_file("passwords.txt", self.password)

    def remove_line_from_file(self, filename, line_to_remove):
        if os.path.exists(filename):
            with open(filename, 'r') as file:
                lines = file.readlines()
            with open(filename, 'w') as file:
                for line in lines:
                    if line.strip() != line_to_remove:
                        file.write(line)

    def show_sign_out_confirmation(self, event):
        reply = QMessageBox.question(self, 'Sign Out Confirmation',
                                     'Are you sure you want to sign out?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
            self.parent_window.show_login_page()


class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainPage.ui", self)
        self.setWindowTitle("Eventer")

        # Connect buttons to functions
        self.pushButton_event.clicked.connect(self.open_google_maps_event1)  # Go to Event 1
        self.pushButton_event2.clicked.connect(self.open_google_maps_event2)  # Go to Event 2
        self.pushButton_addevent.clicked.connect(self.add_event)  # Add Event
        self.pushButton_search.clicked.connect(self.search_event)  # Search Event
        self.pushButton_location.clicked.connect(self.set_current_location)  # Use Current Location
        self.pushButton_sort.clicked.connect(self.sort_events)  # Sort By Tags

        self.load_events()  # Load events on startup

    def add_event(self):
        name = self.lineEdit_name.text().strip()
        price = self.lineEdit_price.text().strip()
        tags = self.lineEdit_tags.text().strip()
        privacy = self.lineEdit_privacy.currentText()
        location = self.lineEdit_location.text().strip()

        if self.event_exists(name):
            QMessageBox.warning(self, "Error", "This name already exists.")
            return

        self.save_event(name, price, tags, privacy, location)
        QMessageBox.information(self, "Success", "Event added successfully.")
        self.load_events()  # Reload events after adding

    def save_event(self, name, price, tags, privacy, location):
        with open("events.txt", "a") as file:
            file.write(f"{name},{price},{tags},{privacy},{location}\n")

    def load_events(self):
        # Clear previous event displays
        self.clear_event_displays()

        if os.path.exists("events.txt"):
            with open("events.txt", "r") as file:
                events = file.readlines()
                for index, event in enumerate(events):
                    name, price, tags, privacy, location = event.strip().split(',')
                    if index == 0:
                        self.eventname1.setText(name)
                        self.price1.setText(price)
                        self.tags1.setText(tags)
                        self.privacy1.setText(privacy)
                        self.location1.setText(location)
                    elif index == 1:
                        self.eventname2.setText(name)
                        self.price2.setText(price)
                        self.tags2.setText(tags)
                        self.privacy2.setText(privacy)
                        self.location2.setText(location)

    def clear_event_displays(self):
        # Clear all event labels
        self.eventname1.setText("")
        self.price1.setText("")
        self.tags1.setText("")
        self.privacy1.setText("")
        self.location1.setText("")
        self.eventname2.setText("")
        self.price2.setText("")
        self.tags2.setText("")
        self.privacy2.setText("")
        self.location2.setText("")

    def event_exists(self, name):
        if os.path.exists("events.txt"):
            with open("events.txt", "r") as file:
                events = file.readlines()
                for event in events:
                    if event.strip().split(',')[0] == name:
                        return True
        return False

    def search_event(self):
        search_text = self.lineEdit_search.text().strip()
        matching_events = []

        if os.path.exists("events.txt"):
            with open("events.txt", "r") as file:
                events = file.readlines()
                for event in events:
                    name, price, tags, privacy, location = event.strip().split(',')
                    if search_text.lower() == name.lower():
                        matching_events.append((name, price, tags, privacy, location))

        if matching_events:
            self.display_search_results(matching_events)
        else:
            QMessageBox.information(self, "No Matches", "No events found matching your search.")

    def display_search_results(self, events):
        # Display the first matching event
        name, price, tags, privacy, location = events[0]
        self.eventname1.setText(name)
        self.price1.setText(price)
        self.tags1.setText(tags)
        self.privacy1.setText(privacy)
        self.location1.setText(location)

    def open_google_maps_event1(self):
        if self.location1.text():
            webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={self.location1.text()}")
        else:
            QMessageBox.warning(self, "Error", "No location available to open.")

    def open_google_maps_event2(self):
        if self.location2.text():
            webbrowser.open(f"https://www.google.com/maps/search/?api=1&query={self.location2.text()}")
        else:
            QMessageBox.warning(self, "Error", "No location available to open.")

    def set_current_location(self):
        QMessageBox.information(self, "Feature Not Implemented", "Sorry, this feature hasn't been implemented yet.")

    def sort_events(self):
        # Placeholder for sorting functionality
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())


class SignupPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("SignupPage.ui", self)

        self.pushButton_signup.clicked.connect(self.signupClicked)
        self.pushButton_goLogin.clicked.connect(self.goLoginClicked)

    def signupClicked(self):
        username = self.findChild(QLineEdit, "lineEdit_username").text().strip()
        password = self.findChild(QLineEdit, "lineEdit_password").text().strip()
        confirm_password = self.findChild(QLineEdit, "lineEdit_confirm").text().strip()

        if not username or not password or not confirm_password:
            QMessageBox.warning(self, "Empty Field(s)", "Please fill in all the fields.")
            return

        if self.check_username_exists(username):
            QMessageBox.warning(self, "Username already in use", "This username is already registered.")
        elif password != confirm_password:
            QMessageBox.warning(self, "Passwords don't match", "The password and confirm password fields don't match.")
        else:
            self.save_user_info(username, password)
            QMessageBox.information(self, "Account created", "Your account has been created successfully. Please log in.")
            self.goLoginClicked()

    def check_username_exists(self, username):
        if os.path.exists("usernames.txt"):
            with open("usernames.txt", "r") as file:
                for line in file:
                    if line.strip() == username:
                        return True
        return False

    def save_user_info(self, username, password):
        with open("usernames.txt", "a") as file:
            file.write(f"{username}\n")
        with open("passwords.txt", "a") as file:
            file.write(f"{password}\n")

    def goLoginClicked(self):
        self.login_window = LoginPage()
        self.login_window.show()
        self.hide()


class LoginPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("LoginPage.ui", self)

        self.pushButton_login.clicked.connect(self.loginClicked)
        self.pushButton_createAccount.clicked.connect(self.createAccountClicked)

    def loginClicked(self):
        username_input = self.findChild(QLineEdit, "lineEdit_username").text().strip()
        password_input = self.findChild(QLineEdit, "lineEdit_password").text().strip()

        if not username_input or not password_input:
            QMessageBox.warning(self, "Empty Field(s)", "Please fill in all the fields.")
            return

        if self.check_credentials(username_input, password_input):
            QMessageBox.information(self, "Login Successful", "Welcome!")
            self.main_page = MainPage()
            self.main_page.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "Incorrect username or password.")
            self.findChild(QLineEdit, "lineEdit_username").clear()
            self.findChild(QLineEdit, "lineEdit_password").clear()

    def check_credentials(self, username, password):
        if os.path.exists("usernames.txt") and os.path.exists("passwords.txt"):
            with open("usernames.txt", "r") as usernames_file, open("passwords.txt", "r") as passwords_file:
                usernames = [line.strip() for line in usernames_file.readlines()]
                passwords = [line.strip() for line in passwords_file.readlines()]
                if username in usernames and password in passwords:
                    return True
        return False

    def createAccountClicked(self):
        self.signup_window = SignupPage()
        self.signup_window.show()
        self.hide()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = LoginPage()
    loginWindow.show()
    sys.exit(app.exec())