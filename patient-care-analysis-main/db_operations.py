from pymongo import MongoClient
import streamlit as st
import bcrypt
import uuid

# Connect to MongoDB    
@st.cache_resource
def get_client():
    return MongoClient(st.secrets['connection_string'])  # Update the URI as needed


client=get_client()
db = client["patientDB"]
collection = db["patient_records"]

def hash_password(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_password(hashed_password, password):
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)

# Function to add a data record


def add_user(email,password):
    user=collection.find_one({"email":email})
    if not user:
        hashed_pass=hash_password(password)
        result=collection.insert_one({"email":email,'password':hashed_pass})
        return 'new'
    else:
        if check_password(user['password'],password):
            return True
        return False

    


def add_data(record):
    user=collection.find_one({"email":record['email']})
    if not user:
        email=record['email']
        record['id']=str(uuid.uuid4())
        result = collection.find_one_and_update({"email":email},{"$push":{"diseases":record}})
        return result
    else:
        email=record['email']
        record['id']=str(uuid.uuid4())
        if 'diseases' in user and len(user['diseases'])>=3:
            collection.find_one_and_update({"email":email},{"$pop":{"diseases":-1}})
        result = collection.find_one_and_update({"email":email},{"$push":{"diseases":record}})
        return result

# Function to get an existing data record
def get_data(query):
    result = collection.find_one(query)
    return result

def get_all_data():
    result = collection.find()
    results=[]
    for i in result:
        if 'diseases' in i:
            results.extend(i['diseases'])
    return results
