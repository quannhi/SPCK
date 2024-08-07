from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QWidget
from PyQt6 import uic
import sys
import os
import logging
from PyQt6 import QtWidgets, uic
import sys


class AccountWindow(QMainWindow):
    def __init__(self, parent=None, username=None, password=None):
        super().__init__(parent)
        uic.loadUi("Account.ui", self)
        self.username = username
        self.password = password
        self.parent_window = parent

        self.delete_button = self.findChild(QWidget, "delete_2")
        if self.delete_button:
            self.delete_button.clicked.connect(self.delete_account)

        self.widget_6 = self.findChild(QWidget, "widget_6")
        if self.widget_6:
            self.widget_6.mousePressEvent = self.show_sign_out_confirmation

    def delete_account(self):
        reply = QMessageBox.question(self, 'Confirm Account Deletion',
                                    'Are you sure you want to delete your account?',
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.remove_user_from_files()
            self.close()
            self.parent_window.show_signup_page()
            QMessageBox.information(self, 'Account Deleted', 'Account removed successfully.')

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
                                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No, QMessageBox.StandardButton.No)

        if reply == QMessageBox.StandardButton.Yes:
            self.close()
            self.parent_window.show_login_page()

import os
import logging

class MainPage(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("MainPage.ui", self)
        self.setWindowTitle("Eventer")  # Set the window title

        # Connect the "Book Now" button clicks to the show_notification function
        self.pushButton.clicked.connect(self.show_notification)
        self.pushButton_2.clicked.connect(self.show_notification)
        self.pushButton_3.clicked.connect(self.show_notification)

        # Connect the "Add Event" button to the add_event method
        self.pushButton_addevent.clicked.connect(self.add_event)

    def show_notification(self):
        # Placeholder for notification logic
        print("Notification button clicked!")

    def add_event(self):
        # Get text from input fields
        name = self.txtName.text()  # QLineEdit for event name
        price = self.txtPrice.text()  # QLineEdit for price
        tags = self.txtTags.currentText()  # QComboBox for tags
        privacy = self.txtPrivacy.currentText()  # QComboBox for privacy setting

        # Update the display labels with the new information
        self.label_name.setText(name)
        self.label_price.setText(price)
        self.label_tag.setText(tags)
        self.label_privacy.setText(privacy)

        # Optionally, you can create new labels or update existing ones here
        # self.create_label(name, self.label_15.geometry(), self.label_15.font())

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainPage()
    window.show()
    sys.exit(app.exec())


class SignupPage(QMainWindow):
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
class LoginPage(QMainWindow):
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
    app = QApplication(sys.argv)
    loginWindow = LoginPage()
    loginWindow.show()
    sys.exit(app.exec())