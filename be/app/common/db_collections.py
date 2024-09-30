from enum import Enum


class Collections(str, Enum):
    # Customer Management
    CONTACT = 'Contact'
    HISTORY = 'History'
    FEEDBACK = 'Feedback'
    
    # Record Counter
    RECORD_COUNTER = 'RecordCounter'
    
    # AI
    DATASET_CONFIG = 'DatasetConfig'
    MODEL_DATASET = 'ModelDataset'
    SENTIMENT_MODEL = 'SentimentModel'
    TRAINING_EPOCH = 'TrainingEpoch'
    
    
class RootCollections(str, Enum):
    USERS = 'Users'
    # Hotel Detail
    HOTEL = 'Hotel'