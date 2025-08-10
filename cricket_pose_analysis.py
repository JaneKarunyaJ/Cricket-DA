import cv2
import mediapipe as mp
import numpy as np
import os
import csv

# Setup MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)

def calculate_angle(a, b, c):
    a, b, c = np.array(a), np.array(b), np.array(c)
    radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    return 360 - angle if angle > 180 else angle

# Find all .mp4 files in current folder
videos = [f for f in os.listdir() if f.endswith(".mp4")]
if not videos:
    print("❌ No MP4 files found.")
    exit()

for video_file in videos:
    print(f"🎬 Processing video: {video_file}")

    cap = cv2.VideoCapture(video_file)
    if not cap.isOpened():
        print(f"❌ Could not open {video_file}")
        continue

    # Setup video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out_filename = f"{os.path.splitext(video_file)[0]}_analysis.mp4"
    out = cv2.VideoWriter(
        out_filename,
        fourcc,
        int(cap.get(cv2.CAP_PROP_FPS)),
        (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    )

    # Setup CSV output
    csv_filename = f"{os.path.splitext(video_file)[0]}_stats.csv"
    csv_file = open(csv_filename, mode='w', newline='')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Frame", "Bat Angle", "Feedback"])

    frame_num = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_num += 1
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)
        h, w, _ = frame.shape

        feedback = "No pose detected"
        angle = None

        if results.pose_landmarks:
            mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            lm = results.pose_landmarks.landmark
            shoulder = [lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x * w,
                        lm[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y * h]
            elbow = [lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x * w,
                     lm[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y * h]
            wrist = [lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].x * w,
                     lm[mp_pose.PoseLandmark.RIGHT_WRIST.value].y * h]

            angle = calculate_angle(shoulder, elbow, wrist)

            if angle < 120:
                feedback = "Increase bat swing angle for more power."
            elif angle > 160:
                feedback = "Swing too wide; reduces control."
            else:
                feedback = "Good swing angle!"

            cv2.putText(frame, f"Bat Angle: {angle:.1f}", (30, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            cv2.putText(frame, feedback, (30, 100),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Save frame data into CSV
        csv_writer.writerow([frame_num, f"{angle:.1f}" if angle else "N/A", feedback])

        cv2.imshow("Cricket Pose Feedback", frame)
        out.write(frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    csv_file.close()
    print(f"✅ Saved video as {out_filename} and stats as {csv_filename}")

cv2.destroyAllWindows()
