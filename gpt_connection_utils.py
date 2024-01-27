# determine the columns that we want to pass to the API
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

columns_to_select = {
    "Name": 0,
    "Department": 1,
    "GEO": 1,
    "Role": 1,
    "Rising_Star": 1,
    "Will_Relocate": 0,
    "Critical": 1,
    "Trending Perf": 1,
    "Talent_Level": 1,
    "Percent_Remote": 1,
    "EMP_Sat_OnPrem_1": 1,
    "EMP_Sat_Remote_1": 1,
    "EMP_Engagement_1": 1,
    "last_evaluation": 1,
    "number_project": 0,
    "average_montly_hours": 0,
    "time_spend_company": 1,
    "left_Company": 0,
    "promotion_last_5years": 1,
    "salary": 1,
    "Gender": 1,
    "Emp_Work_Status2": 1,
    "Emp_Identity": 1,
    "Emp_Role": 1,
    "Emp_Position": 1,
    "Emp_Title": 1,
    "Emp_Satisfaction": 0,
    "Emp_Competitive_1": 1,
    "Emp_Collaborative_1": 1,
}


def get_recommendation_for_agent(agent_details):
    prompt = "give me recommendation for agent with the following info : \n"
    for key in agent_details.keys():
        prompt += (
            f"{key} : {agent_details[key]}, "
            if columns_to_select.__contains__(key) and columns_to_select[key] == 1
            else ""
        )
    return prompt


def get_recommendation(agent_details):
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        # seed=7,
        messages=[
            {"role": "system", "content": open("./storage/system_prompt.txt").read()},
            {"role": "user", "content": get_recommendation_for_agent(agent_details)},
        ],
    )
    print(completion.choices[0].message.content)
    return completion.choices[0].message.content
