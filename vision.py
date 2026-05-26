import cv2

class Vision:
    def __init__(self):
        self.cap = cv2.VideoCapture(0)

    def prepprocess(self, frame):
        frame=cv2.resize(frame,(640,480))
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return frame 
    
    def normalizser(self, frame):
        frame = frame/255
        #dummy method for normalization :)

    def features(self, frame):
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges=cv2.Canny(gray, 100, 200)
        return edges
    
    def start(self):

        while True:
            ret, frame = self.cap.read()

            if not ret: 
                break
            
            processed_frame = self.prepprocess(frame)
            features=self.features(processed_frame)
            cv2.imshow('Features', features)  


            if cv2.waitKey(1)==ord('q'):
                break

        self.cap.release()
        self.cap.destroyAllWindows()

def main():
    camera = Vision()
    camera.start()

if __name__ == "__main__":
    main()