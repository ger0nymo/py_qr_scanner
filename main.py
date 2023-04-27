import cv2
from pyzbar import pyzbar
import time
import requests
import jwt
import secrets_env

API_URL = 'https://qrhazi-backend.azurewebsites.net';

def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    last_read = ""
    while ret:
        ret, frame = camera.read()
        barcodes = pyzbar.decode(frame)
        if len(barcodes) == 1:
          barcode_info = barcodes[0].data.decode('utf-8') 

          if barcode_info != last_read:
            last_read = barcode_info

            header = {"Authorization": f"Bearer {barcode_info}"}
            response = requests.get(f"{API_URL}/qr/verify", headers=header)

            print(barcode_info)

            if response.status_code == 200:
              try: 
                log_result = requests.post(f"{API_URL}/logging/create", headers=header)
                print("User entered: " + log_result.text)
              except:
                print("User can't enter / qr code is invalid")

            else: 
              print(f"User can't enter / qr code is invalid: {response.text}")

        cv2.imshow('QR code reader', frame)

        if cv2.waitKey(1) & 0xFF == 27:
          break
    camera.release()
    cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()