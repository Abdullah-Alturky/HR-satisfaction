from marshmallow import Schema, fields, ValidationError, EXCLUDE, pre_load, post_load


class UserSchema(Schema):
    class Meta:
        unknown = EXCLUDE

    Name = fields.Str(required=True)
    id = fields.Int(required=True)
    Department = fields.Str(required=True)
    GEO = fields.Str(required=True)
    Role = fields.Str(required=True)
    Rising_Star = fields.Int(required=True)
   # Will_Relocate = fields.Int(required=True)
    Critical = fields.Int(required=True)
    Trending_Perf = fields.Int(required=True)
    Talent_Level = fields.Int(required=True)
    Percent_Remote = fields.Float(required=True)
    EMP_Sat_OnPrem_1 = fields.Int(required=True)
    EMP_Sat_Remote_1 = fields.Int(required=True)
    EMP_Engagement_1 = fields.Int(required=True)
    last_evaluation = fields.Int(required=True)
    #number_project = fields.Int(required=True)
    #average_montly_hours = fields.Int(required=True)
    time_spend_company = fields.Int(required=True)
    promotion_last_5years = fields.Int(required=True)
    salary = fields.Str(required=True)
    Gender = fields.Str(required=True)
    left_Company = fields.Int(required=True)
    Emp_Work_Status2 = fields.Int(required=True)
    Emp_Identity = fields.Int(required=True)
    Emp_Role = fields.Int(required=True)
    Emp_Position = fields.Int(required=True)
    Emp_Title = fields.Int(required=True)
    #Emp_Satisfaction = fields.Int(required=True)
    Emp_Competitive_1 = fields.Int(required=True)
    Emp_Collaborative_1 = fields.Int(required=True)
    recommendation = fields.Str(required=False)
    is_satisfied = fields.Int(required=False)

    @post_load
    def add_trending_pref(self, data, **kwargs):
        import pdb

        pdb.set_trace()
        data["Trending_Perf"] = data["Trending Perf"]
        return data


def validated_user(user):
    try:
        user = UserSchema().dump(user)
        return True, user
    except ValidationError as err:
        return False, err.messages
