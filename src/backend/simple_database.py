"""
Simple in-memory database for development when MongoDB is not available
"""

from typing import Dict, Any

# In-memory storage
activities_data = {}
teachers_data = {}

class SimpleCollection:
    def __init__(self, data_dict):
        self.data = data_dict
    
    def find(self, query=None):
        """Find documents matching query"""
        if query is None:
            query = {}
        
        results = []
        for doc_id, doc in self.data.items():
            doc_copy = doc.copy()
            doc_copy['_id'] = doc_id
            
            # Simple query matching for day filter
            if 'schedule_details.days' in query:
                days_query = query['schedule_details.days']
                if '$in' in days_query:
                    required_days = days_query['$in']
                    doc_days = doc.get('schedule_details', {}).get('days', [])
                    if not any(day in doc_days for day in required_days):
                        continue
                        
            # Simple query matching for time filters
            if 'schedule_details.start_time' in query:
                start_time_query = query['schedule_details.start_time']
                if '$gte' in start_time_query:
                    required_start = start_time_query['$gte']
                    doc_start = doc.get('schedule_details', {}).get('start_time', '')
                    if doc_start < required_start:
                        continue
                        
            if 'schedule_details.end_time' in query:
                end_time_query = query['schedule_details.end_time']
                if '$lte' in end_time_query:
                    required_end = end_time_query['$lte']
                    doc_end = doc.get('schedule_details', {}).get('end_time', '')
                    if doc_end > required_end:
                        continue
            
            results.append(doc_copy)
        
        return results
    
    def find_one(self, query):
        """Find one document"""
        if isinstance(query, dict) and '_id' in query:
            doc_id = query['_id']
            if doc_id in self.data:
                doc_copy = self.data[doc_id].copy()
                doc_copy['_id'] = doc_id
                return doc_copy
        return None
    
    def update_one(self, query, update):
        """Update one document"""
        if '_id' in query:
            doc_id = query['_id']
            if doc_id in self.data:
                if '$push' in update:
                    for field, value in update['$push'].items():
                        if field not in self.data[doc_id]:
                            self.data[doc_id][field] = []
                        self.data[doc_id][field].append(value)
                if '$pull' in update:
                    for field, value in update['$pull'].items():
                        if field in self.data[doc_id] and value in self.data[doc_id][field]:
                            self.data[doc_id][field].remove(value)
                return type('MockResult', (), {'modified_count': 1})()
        return type('MockResult', (), {'modified_count': 0})()
    
    def count_documents(self, query):
        """Count documents"""
        return len(self.data)
    
    def aggregate(self, pipeline):
        """Simple aggregation for getting unique days"""
        # For the specific case of getting unique days
        days = set()
        for doc in self.data.values():
            if 'schedule_details' in doc and 'days' in doc['schedule_details']:
                days.update(doc['schedule_details']['days'])
        
        return [{'_id': day} for day in sorted(days)]
    
    def insert_one(self, doc):
        """Insert one document"""
        doc_id = doc.pop('_id')
        self.data[doc_id] = doc

# Initialize collections
activities_collection = SimpleCollection(activities_data)
teachers_collection = SimpleCollection(teachers_data)

def hash_password(password):
    """Simple password hashing for development"""
    return f"hashed_{password}"

def init_database():
    """Initialize database if empty"""
    
    # Initialize activities if empty
    if not activities_data:
        for name, details in initial_activities.items():
            activities_data[name] = details
            
    # Initialize teacher accounts if empty  
    if not teachers_data:
        for teacher in initial_teachers:
            username = teacher.pop('username')
            teachers_data[username] = teacher

# Initial database if empty
initial_activities = {
    "Chess Club": {
        "description": "Learn strategies and compete in chess tournaments",
        "schedule": "Mondays and Fridays, 3:15 PM - 4:45 PM",
        "schedule_details": {
            "days": ["Monday", "Friday"],
            "start_time": "15:15",
            "end_time": "16:45"
        },
        "max_participants": 12,
        "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
    },
    "Programming Class": {
        "description": "Learn programming fundamentals and build software projects",
        "schedule": "Tuesdays and Thursdays, 7:00 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "07:00",
            "end_time": "08:00"
        },
        "max_participants": 20,
        "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
    },
    "Morning Fitness": {
        "description": "Early morning physical training and exercises",
        "schedule": "Mondays, Wednesdays, Fridays, 6:30 AM - 7:45 AM",
        "schedule_details": {
            "days": ["Monday", "Wednesday", "Friday"],
            "start_time": "06:30",
            "end_time": "07:45"
        },
        "max_participants": 30,
        "participants": ["john@mergington.edu", "olivia@mergington.edu"]
    },
    "Soccer Team": {
        "description": "Join the school soccer team and compete in matches",
        "schedule": "Tuesdays and Thursdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Tuesday", "Thursday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 22,
        "participants": ["liam@mergington.edu", "noah@mergington.edu"]
    },
    "Basketball Team": {
        "description": "Practice and compete in basketball tournaments",
        "schedule": "Wednesdays and Fridays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Wednesday", "Friday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["ava@mergington.edu", "mia@mergington.edu"]
    },
    "Art Club": {
        "description": "Explore various art techniques and create masterpieces",
        "schedule": "Thursdays, 3:15 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Thursday"],
            "start_time": "15:15",
            "end_time": "17:00"
        },
        "max_participants": 15,
        "participants": ["amelia@mergington.edu", "harper@mergington.edu"]
    },
    "Drama Club": {
        "description": "Act, direct, and produce plays and performances",
        "schedule": "Mondays and Wednesdays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Monday", "Wednesday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 20,
        "participants": ["ella@mergington.edu", "scarlett@mergington.edu"]
    },
    "Math Club": {
        "description": "Solve challenging problems and prepare for math competitions",
        "schedule": "Tuesdays, 7:15 AM - 8:00 AM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "07:15",
            "end_time": "08:00"
        },
        "max_participants": 10,
        "participants": ["james@mergington.edu", "benjamin@mergington.edu"]
    },
    "Debate Team": {
        "description": "Develop public speaking and argumentation skills",
        "schedule": "Fridays, 3:30 PM - 5:30 PM",
        "schedule_details": {
            "days": ["Friday"],
            "start_time": "15:30",
            "end_time": "17:30"
        },
        "max_participants": 12,
        "participants": ["charlotte@mergington.edu", "amelia@mergington.edu"]
    },
    "Weekend Robotics Workshop": {
        "description": "Build and program robots in our state-of-the-art workshop",
        "schedule": "Saturdays, 10:00 AM - 2:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "10:00",
            "end_time": "14:00"
        },
        "max_participants": 15,
        "participants": ["ethan@mergington.edu", "oliver@mergington.edu"]
    },
    "Science Olympiad": {
        "description": "Weekend science competition preparation for regional and state events",
        "schedule": "Saturdays, 1:00 PM - 4:00 PM",
        "schedule_details": {
            "days": ["Saturday"],
            "start_time": "13:00",
            "end_time": "16:00"
        },
        "max_participants": 18,
        "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
    },
    "Sunday Chess Tournament": {
        "description": "Weekly tournament for serious chess players with rankings",
        "schedule": "Sundays, 2:00 PM - 5:00 PM",
        "schedule_details": {
            "days": ["Sunday"],
            "start_time": "14:00",
            "end_time": "17:00"
        },
        "max_participants": 16,
        "participants": ["william@mergington.edu", "jacob@mergington.edu"]
    },
    "Manga Maniacs": {
        "description": "Dive into epic adventures, discover incredible superpowers, and experience unforgettable friendships through the captivating world of Japanese manga! Join fellow otaku to discuss your favorite series and discover new ones.",
        "schedule": "Tuesdays, 7:00 PM - 8:00 PM",
        "schedule_details": {
            "days": ["Tuesday"],
            "start_time": "19:00",
            "end_time": "20:00"
        },
        "max_participants": 15,
        "participants": []
    }
}

initial_teachers = [
    {
        "username": "mrodriguez",
        "display_name": "Ms. Rodriguez",
        "password": hash_password("art123"),
        "role": "teacher"
     },
    {
        "username": "mchen",
        "display_name": "Mr. Chen",
        "password": hash_password("chess456"),
        "role": "teacher"
    },
    {
        "username": "principal",
        "display_name": "Principal Martinez",
        "password": hash_password("admin789"),
        "role": "admin"
    }
]