import random
from faker import Faker

#Initialize Faker.
fake = Faker()

#Utility to generate employee IDs.
def generate_employee_ids(count, start_id=1):
    """
    Generate a list of sequential employee IDs starting from a given ID.
    The format of each ID is 'E' followed by 7 digits with leading zeros.
    
    Parameters:
        count (int): Number of employee IDs to generate.
        start_id (int): The starting ID number. Default is 1.
    
    Returns:
        list: A list of employee IDs in the format 'E0000001', 'E0000010', etc.
    """
    return [f"E{i:07d}" for i in range(start_id, start_id + count)]
