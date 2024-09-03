import requests
from locker_system import LockerSystem
from locker import Locker
from qr_generator import QRGenerator
from jwt_utils import JWTUtils

def fetch_locker_status(api_url):
    try:
        response = requests.get(api_url)
        return response.status_code == 200  # Assuming 200 indicates a successful response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching locker status: {e}")
        return False

def extract_number_from_url(url):
    parts = url.split('/')
    try:
        return int(parts[-1])
    except (ValueError, IndexError):
        return 0

def main():
    qr_generator = QRGenerator()
    jwt_utils = JWTUtils("your_secret_key")
    locker_system = LockerSystem(qr_generator, jwt_utils)

    locker_system.add_locker(Locker(id=1, width=30, height=30))
    locker_system.add_locker(Locker(id=2, width=10, height=20))
    locker_system.add_locker(Locker(id=3, width=50, height=45))
    locker_system.add_locker(Locker(id=4, width=5, height=20))

    while True:
        url_or_id = input("Enter '0' to send a package or enter a locker ID to take a package (or 'exit' to quit): ")
        if url_or_id.lower() == 'exit':
            break

        if url_or_id == '0':
            package_height = int(input("Enter the package height: "))
            package_width = int(input("Enter the package width: "))
            locker_system.send_package(package_width, package_height)
        else:
            # Determine if the input is a URL or an ID
            if url_or_id.startswith("http://") or url_or_id.startswith("https://"):
                if fetch_locker_status(url_or_id):
                    locker_id = extract_number_from_url(url_or_id)
                    locker_system.take_package(locker_id)
                else:
                    print("Failed to fetch locker status from the API.")
            else:
                try:
                    locker_id = int(url_or_id)
                    locker_system.take_package(locker_id)
                except ValueError:
                    print("Invalid locker ID or URL entered.")

if __name__ == "__main__":
    main()
