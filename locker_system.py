import uuid
import json
from locker import Locker
from qr_generator import QRGenerator
from jwt_utils import JWTUtils

class LockerSystem:
    def __init__(self, qr_generator: QRGenerator, jwt_utils: JWTUtils):
        self.lockers = []
        self.qr_generator = qr_generator
        self.jwt_utils = jwt_utils

    def add_locker(self, locker: Locker):
        self.lockers.append(locker)

    def find_locker(self, locker_id: int):
        for locker in self.lockers:
            if locker.id == locker_id:
                return locker
        return None

    def smallest_difference_locker(self, package_width: int, package_height: int):
        eligible_lockers = [locker for locker in self.lockers if locker.is_fit(package_width, package_height)]
        return min(eligible_lockers, key=lambda locker: locker.width - package_width + locker.height - package_height, default=None)

    def send_package(self, package_width: int, package_height: int):
        locker = self.smallest_difference_locker(package_width, package_height)
        if locker:
            locker.set_empty(is_empty=False)
            package_id = self.jwt_utils.encode({"id": str(uuid.uuid4())})
            locker.package_id = package_id
            print(f"The package was sent. Locker ID: {locker.id}, Package ID: {package_id}")
        else:
            print("No suitable locker available for this package size.")

    def take_package(self, locker_id: int):
        locker = self.find_locker(locker_id)
        if locker and not locker.is_empty:
            decoded_id = self.jwt_utils.decode(locker.package_id)
            if decoded_id:
                decoded_id_str = json.dumps(decoded_id)
                self.qr_generator.generate_and_display_qr(decoded_id_str)

                package_id = input("Enter package ID to take the package: ")
                if package_id == locker.package_id:
                    locker.set_empty()
                    locker.package_id = None
                    self.qr_generator.show_success_message("Package taken successfully!")  # Show success message
                else:
                    print("Wrong package ID.")
                    self.qr_generator.close_qr()  # Close the QR code window even if wrong
            else:
                print("Invalid package ID.")
        else:
            print("Invalid locker ID or the locker is empty.")
