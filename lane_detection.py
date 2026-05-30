import cv2
import numpy as np

print("NEW CODE RUNNING")

cap = cv2.VideoCapture("videos/road.mp4")
saved = False
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

out = cv2.VideoWriter(
    "outputs/result.mp4",
    cv2.VideoWriter_fourcc(*'mp4v'),
    20,
    (width, height)
)

while True:
    ret, frame = cap.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imwrite("screenshots/grayscale_output.png", gray)

    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    edges = cv2.Canny(blur, 50, 150)
    cv2.imwrite("screenshots/edge_detection.png", edges)

    lines = cv2.HoughLinesP(
        edges,
        2,
        np.pi / 180,
        threshold=100,
        minLineLength=50,
        maxLineGap=10
    )

    line_image = np.zeros_like(frame)

    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            cv2.line(
                line_image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                3
            )

    output = cv2.addWeighted(
        frame,
        0.8,
        line_image,
        1,
        1
    )
    if not saved:

     cv2.imwrite("screenshots/original_input.png", frame)

     cv2.imwrite("screenshots/grayscale_output.png", gray)

     cv2.imwrite("screenshots/edge_detection.png", edges)

     cv2.imwrite("screenshots/lane_detection_output.png", output)

    saved = True

    cv2.imwrite("screenshots/lane_detection_output.png", output)
    out.write(output)

    cv2.imshow("Lane Detection", output)

    if cv2.waitKey(25) & 0xFF == ord('q'):
        break

cap.release()
out.release()
cv2.destroyAllWindows()