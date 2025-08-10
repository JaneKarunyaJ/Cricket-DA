
Cricket Pose Analysis
📌 Overview
This project uses MediaPipe Pose and OpenCV to perform pose estimation and bat angle analysis in cricket videos. It processes each frame of an input cricket video to detect body landmarks, calculate the bat angle, and provide basic performance feedback. The results are saved as both a CSV file and an annotated output video for visual review.

Currently, the script focuses on batting mechanics (bat angle) and can be extended for bowling and fielding biomechanics.

⚙️ Features
Pose Detection – Detects key body landmarks using MediaPipe Pose.

Bat Angle Calculation – Calculates the angle between the shoulder, elbow, and wrist to measure bat positioning.

Performance Feedback – Generates basic feedback based on the detected bat angle.

Video Output – Creates an annotated video with pose landmarks and feedback text.

CSV Output – Saves frame-by-frame bat angles and feedback for further analysis.

📂 Input & Output
Input
Original cricket video (.mp4)

Output
Annotated Video – <video_name>_analysis.mp4 with drawn pose landmarks and feedback.

Statistics CSV – <video_name>_stats.csv with columns:

Frame number

Bat angle (in degrees)

Feedback

🛠 Requirements
Install the required Python libraries:

bash
Copy
Edit
pip install opencv-python mediapipe numpy
🚀 Usage
Place the cricket video (.mp4) in the project directory.

Run the script:

bash
Copy
Edit
python cricket_pose_analysis.py
The annotated video and CSV will be saved in the same directory.

🧠 Approach
The script follows these steps:

Video Reading – Uses OpenCV to read frames from the input video.

Pose Detection – Uses MediaPipe Pose to detect body landmarks for each frame.

Angle Calculation – Applies a trigonometric formula to compute the bat angle from three key points.

Feedback Generation – Compares the bat angle to predefined thresholds and assigns feedback.

Output Generation – Writes annotated frames to a new video file and logs stats in a CSV file.

📌 Current Limitations
Only analyzes batting mechanics (bat angle).

Does not yet evaluate stance, timing, shot selection, bowling mechanics, or fielding performance.

Works best with clear, well-lit videos where the player is fully visible.

🔮 Future Enhancements
Detect bowling phases: run-up, load-up, front foot landing, release.

Evaluate follow-through: balance, wrist motion, shoulder–hip torque.

Analyze fielding actions: anticipation, dives, throwing technique.

Support multi-role cricket analysis (batting, bowling, fielding) as per biomechanics requirements.
