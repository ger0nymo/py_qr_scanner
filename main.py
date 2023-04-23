import cv2
from pyzbar import pyzbar
import time


def main():
    camera = cv2.VideoCapture(0)
    ret, frame = camera.read()
    last_read = ""
    while ret:
        ret, frame = camera.read()
        barcodes = pyzbar.decode(frame)
        if len(barcodes) == 1:
          barcode_info = barcodes[0].data.decode('utf-8') 
          
          # Visualizing the QR code for debugging purposes
          barcode = barcodes[0]
          cv2.rectangle(frame, (barcode.rect.left, barcode.rect.top),
            (barcode.rect.left + barcode.rect.width, barcode.rect.top + barcode.rect.height),
           (0, 255, 0), 2)
          cv2.putText(frame, barcode.data.decode('utf-8'), (barcode.rect.left, barcode.rect.top),
          cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

          if barcode_info != last_read:
            last_read = barcode_info
            print(f"New Barcode: {barcode_info}")
            

        cv2.imshow('QR code reader', frame)

        if cv2.waitKey(100) & 0xFF == 27:
          break
    camera.release()
    cv2.destroyAllWindows()
  
if __name__ == '__main__':
    main()
  