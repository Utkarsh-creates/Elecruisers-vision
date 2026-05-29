import cv2
import numpy as np
import torch
class Vision:
    def __init__(self):
        self.device = "cuda"
        self.model = torch.jit.load("yolopv2.pt")
        self.model = self.model.to(self.device)
        self.model.eval()
        self.cap = cv2.VideoCapture("File.mp4")

    def prepprocess(self, frame):
        frame=cv2.resize(frame,(640,480))
        frame = cv2.GaussianBlur(frame, (5, 5), 0)
        return frame 
    
    def normalizer(self, frame):
        frame = frame/255
        #dummy method for normalization :)

    def features(self, frame):
        gray=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        edges=cv2.Canny(gray, 100, 200)
        return edges


    def lane_detection(self, frame):

        original_h, original_w = frame.shape[:2]

        img = cv2.resize(frame, (640, 640))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        tensor = torch.from_numpy(
            img.transpose(2, 0, 1)
        ).float()

        tensor = tensor.unsqueeze(0)
        tensor = tensor.to(self.device)

        tensor /= 255.0

        with torch.no_grad():
            outputs = self.model(tensor)

    # ------------------------
    # DRIVABLE AREA
    # ------------------------

        drivable = outputs[1]

        drivable = torch.argmax(
            drivable,
            dim=1
        )

        drivable = drivable.squeeze()

        drivable = (
        drivable
        .detach()
        .cpu()
        .numpy()
        .astype(np.uint8)
    )

    # ------------------------
    # LANE MARKINGS
    # ------------------------

        lane_mask = outputs[2]

        lane_mask = lane_mask.squeeze()

        lane_mask = (
        lane_mask
        .detach()
        .cpu()
        .numpy()
    )

        lane_mask = (
        lane_mask > 0.5
    ).astype(np.uint8)

    # ------------------------
    # RESIZE TO VIDEO SIZE
    # ------------------------

        drivable = cv2.resize(
        drivable,
        (original_w, original_h),
        interpolation=cv2.INTER_NEAREST
    )

        lane_mask = cv2.resize(
        lane_mask,
        (original_w, original_h),
        interpolation=cv2.INTER_NEAREST
    )

    # ------------------------
    # FIND RIGHTMOST LANE
    # ------------------------

        bottom = lane_mask[
        int(original_h * 0.8):,
        :
    ]

        column_sum = np.sum(
        bottom,
        axis=0
    )

        lane_columns = np.where(
        column_sum > 0
    )[0]

        if len(lane_columns) > 0:

            right_boundary = lane_columns.max()

            drivable[:, right_boundary:] = 0

    # ------------------------
    # CLEANUP
    # ------------------------

        kernel = np.ones(
            (7, 7),
            np.uint8
    )

        drivable = cv2.morphologyEx(
            drivable,
            cv2.MORPH_CLOSE,
            kernel
    )

    # ------------------------
    # GREEN OVERLAY
    # ------------------------

        overlay = frame.copy()

        overlay[
        drivable > 0
    ] = (0, 255, 0)

    # Optional:
    # draw lane markings blue

        overlay[
        lane_mask > 0
    ] = (255, 0, 0)

        result = cv2.addWeighted(
        frame,
        0.7,
        overlay,
        0.3,
        0
    )

        return result

    def start(self):

        while True:
            ret, frame = self.cap.read()

            if not ret: 
                break
            real = frame.copy()
            processed_frame = self.prepprocess(frame)
            edges=self.features(processed_frame)
            cv2.imshow("Original Camera", real)
            cv2.imshow('Features', edges) 
            lane_frame = self.lane_detection(processed_frame)
            cv2.imshow("Lane Detection", lane_frame)    


            if cv2.waitKey(1)==ord('q'):
                break

        self.cap.release()
        cv2.destroyAllWindows()

def main():
    camera = Vision()
    camera.start()

if __name__ == "__main__":
    main()