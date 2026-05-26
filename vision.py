import cv2

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def start(self):

        while True:
            ret, frame = self.cap.read()

            if not ret: 
                break

            cv2.imshow('Camera', frame)  


            if cv2.waitKey(1)==ord('1'):
                break

        self.cap.release()
        self.cap.destroyAllWindows()

def main():
    camera = Vision()
    camera.start()

if __name__ == "__main__":
    main()