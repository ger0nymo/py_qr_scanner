import cv2
from pyzbar import pyzbar
import time
import requests

API_URL = 'https://qrhazi-backend.azurewebsites.net/qr';

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
            response = requests.get(API_URL + '/verify', headers=header)

            if response.status_code == 200:
              print(f"QR code is valid")
            else: 
              print(f"QR code is invalid: {response.text}")

        cv2.imshow('QR code reader', frame)

        if cv2.waitKey(1) & 0xFF == 27:
          break
    camera.release()
    cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()