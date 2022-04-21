import pickle
import csv
import os

path2models = "../models/"

models = []
subjects = []
for filename in os.listdir(path2models):
    if filename[-4:] == ".pkl":
        subjects.append(filename[:-4])
        file = os.path.join(path2models,filename)
        with open(file,'rb') as fp:
            model = pickle.load(fp)
            models.append(model)

with open("../models.csv", 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Subject-Trial","eye_contact_length", "gaze_aversion_length", "gaze_aversion_theta", "gaze_aversion_r", "gaze_aversion_freq", "blink_freq", "test_time"])
    for i in range(len(models)):
        row = [subjects[i]]
        for item in models[i].values():
            row.append(str(item))
        writer.writerow(row)
    