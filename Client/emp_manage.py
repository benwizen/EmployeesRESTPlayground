import emp_api
import json
import pandas as pd


# all_emp_json = emp_api.get_all("http://dummy.restapiexample.com/api/v1/employees")
# json_data = json.dumps(all_emp_json)
# df = pd.read_json(json_data)
# df = df[['id', 'employee_name', 'employee_age', 'employee_salary']]
# max_id = df[['id']].max()
# df = df[df.employee_age > 0]
# df = df[df.employee_name.str.contains(" ")]
# df.dropna(thresh=1).sort_values(by=['id'])
# df.to_csv("emps_info.csv", encoding='utf8', index=False)
# print(df)
# print(df.head(5))
# print([str(name).capitalize() for name in list(df['employee_name'].values)])
