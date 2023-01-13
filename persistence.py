
import os
import json
import enrollment_manager

filename = 'enrollment_manager_persistence.json'

def load():
    manager = enrollment_manager.EnrollmentManager()
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            persisted = json.load(f)
            
        manager.students = persisted['students']
        manager.courses = persisted['courses']
    return manager
    

def save(manager):
    persisted = {'students': manager.students, 'courses': manager.courses }
    with open(filename, 'w') as f:
        json.dump(persisted, f)

