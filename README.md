# Employee Attendance Record

Executes facial Recognition to record the employee's Attendance via Rasperry pi 4

The Employee can also make a post, check Attendance and contact system administrator on the Web-site.
```bash
# Take the face samples
python3 samplefecth.py

# To train the samples 
python3 FaceTraining.py

# open up Face Recognition to record the attendence
python3 Face_Sets.py

# boost flask 
python3 run.py
```

