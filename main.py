import cv2
from pyzbar import pyzbar
import time


def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    read_qr_codes = []
    while ret:
        ret, frame = camera.read()
        barcodes = pyzbar.decode(frame)
        if len(barcodes) == 1: # csak ha egy QR kód van a képen
          barcode_info = barcodes[0].data.decode('utf-8') 
          # mivel másodpercenként rengeteg frame jön be, ezért rengetegszer is ismeri fel ugyanazt a qr kódot, viszont nekünk
          # csak egyszer kell vele dolgoznunk, ezért a read_qr_codes listában tároljuk, hogy melyiket ismertük már fel, -> uaz. a qr kódot
          # csak egyszer fogjuk feldolgozni
          if barcode_info not in read_qr_codes:
            read_qr_codes.append(barcode_info)
            print(f"New Barcode: {barcode_info}")
            print("most csinálunk valamit, de csak egyszer")
            if len(read_qr_codes) >= 30:
              read_qr_codes = []

        cv2.imshow('Barcode/QR code reader', frame)
        if cv2.waitKey(100) & 0xFF == 27:
          break
    camera.release()
    cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()
  