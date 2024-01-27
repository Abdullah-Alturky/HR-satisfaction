from flask import Blueprint, request, jsonify, make_response
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from validation import validated_user
from bson import ObjectId  # Import ObjectId from bson
from utils import stringify_mongo_id, paginate
from math import ceil
from model_functions import predict_attrition
from gpt_connection_utils import get_recommendation
import pandas as pd

api_bp = Blueprint("api", __name__)

load_dotenv()
client = MongoClient(
    os.getenv("CONNECTION_STRING"),
    connectTimeoutMS=30000,
)
db = client["chat-gpt-connection"]
users_collection = db["users"]

@api_bp.post("/users/recommend")
def recommendForUser():
    user = request.get_json()
    user["is_satisfied"] = predict_attrition(user)
    validated, user = validated_user(request.get_json())
    if not validated:
        return make_response(jsonify({"error": user}), 400)
    if user['is_satisfied'] == 0:
        user["recommendation"] = get_recommendation(user)
    return {"message": "We Recommend this to the user", "user": user}

@api_bp.post("/users/")
def adduser():
    validated, user = validated_user(request.get_json())
    if not validated:
        return make_response(jsonify({"error": user}), 400)
  
    
    usr = users_collection.insert_one(user)
  
    return {"message": "User has been added successfully", "user": stringify_mongo_id(user)}

@api_bp.get("/users/<user_id>")
def userInfo(user_id):
    user = users_collection.find_one({"_id": ObjectId(user_id)})
    if( not user.__contains__("recommendation") or user["recommendation"] == None) and user["is_satisfied"] == 0:
        # ensure that the user isn't satistfied with his job
        recommendation = get_recommendation(user)
        users_collection.update_one(
            {"_id": ObjectId(user_id)}, {"$set": {"recommendation": recommendation}}
        )
        user["recommendation"] = recommendation
    return jsonify({"user": stringify_mongo_id(user)})

@api_bp.get("/users/statistics")
def stats():
    # return the following statistics:
    # 1. the total number of employees in the company
    # 2. percentage of male and female employees
    # 3. average years in company (time_spend_company)
    # 4. average employees satisfaction(for current and employee that left company)
    
    # 1. the total number of employees in the company
    total_employees = users_collection.count_documents({"left_Company":0})
    #total_employees2 = users_collection.count_documents({"left_Company":1})
    males = users_collection.count_documents({"Gender":"M","left_Company":0})
    average = users_collection.aggregate([{"$group":{  "_id":None,
                                                                        "average_years_in_company":{"$avg":"$time_spend_company"},
                                                                        "average_employees_satisfaction":{"$avg":"$Emp_Satisfaction"}}}])
    average = list(average)
    return jsonify({
        "total_employees": total_employees,
        "males": males,
        "females": total_employees - males,
        "average_years_in_company": average[0]["average_years_in_company"],
        "average_employees_satisfaction": average[0]["average_employees_satisfaction"]})


@api_bp.get("/users/salaries-statistics")
def salaries_stats():
    # return the salaries average grouped by department map the enum of LOW MEDIUM HIGH to 1 2 3 and return the average
    salaries = users_collection.aggregate([{"$group":{  "_id":"$Department",
                                                                        "average_salary":{"$avg":{"$switch":{
                                                                                                            "branches":[
                                                                                                                {"case":{"$eq":["$salary","low"]},"then":1},
                                                                                                                {"case":{"$eq":["$salary","medium"]},"then":2},
                                                                                                                {"case":{"$eq":["$salary","high"]},"then":3}
                                                                                                            ],
                                                                                                            "default":0}}}}}])
    return jsonify(list(salaries))
    

@api_bp.get("/users/time-spend-statistics")
def time_spend_stats():
    # return the average time spend grouped by department
    time_spend = users_collection.aggregate([{"$group":{  "_id":"$time_spend_company",
                                                                        "average_time_spend":{"$count":{}}}},
                                             {"$sort": {"_id": 1}}])
    return jsonify(list(time_spend))

@api_bp.get("/users")
def users():
    page = int(request.args.get("page", 1))
    limit = int(request.args.get("limit", 10))
    query = request.args.get("query", "")
    find_query = {'left_Company':0}
    if(query != ""):
        find_query['$or'] =  [
            {'Name': {'$regex': query, '$options': 'i'}},
            {'Department': {'$regex': query, '$options': 'i'}},
            {'Role': {'$regex': query, '$options': 'i'}},
        ]
    all_users = users_collection.find(find_query)
    count = users_collection.count_documents(find_query)
    paginated_users = list(map(stringify_mongo_id, paginate(all_users, page, limit)))
    pages_count = int(ceil(count / limit))
    for user in paginated_users:
        if not user.__contains__("is_satisfied"):
            user["is_satisfied"] = int(predict_attrition(user))
            users_collection.update_one(
                {"_id": ObjectId(user["_id"])}, {"$set": {"is_satisfied": user["is_satisfied"]}}
            )
    return jsonify(
        {
            "meta": {
                "pages_count": pages_count,
                "current_page": page,
                "next_page": page + 1 if page < pages_count else None,
                "limit": limit,
            },
            "users": paginated_users,
        }
    )
