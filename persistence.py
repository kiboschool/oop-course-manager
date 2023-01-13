
import os
import course_enrollment
import jsonpickle

filename = 'course_enrollment_persistence.json'

def load():
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            json_text = f.read()
            persisted = jsonpickle.decode(json_text)
            
        return persisted
    else:
        return course_enrollment.EnrollmentManager()
    

def save(enrollment_manager):
    with open(filename, 'w') as f:
        json_text = jsonpickle.encode(enrollment_manager)
        f.write(json_text)

