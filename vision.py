import cv2

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def prepprocess(self, frame):
        frame=cv2.resize(frame,(640,480))

        frame = frame/255
        frame = cv2.GaussianBlur(frame, (5, 5), 0)

        return frame 
    
    def start(self):

        while True:
            ret, frame = self.cap.read()

            if not ret: 
                break
            
            processed_frame = self.prepprocess(frame)
            display_frame=(processed_frame*255).astype('uint8')
            cv2.imshow('Camera', display_frame)  


            if cv2.waitKey(1)==ord('1'):
                break

        self.cap.release()
        self.cap.destroyAllWindows()

def main():
    camera = Vision()
    camera.start()

if __name__ == "__main__":
    main()