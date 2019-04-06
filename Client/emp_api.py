from Server import URL
import requests


def get_all(url):
    req = requests.get(url)
    req.raise_for_status()
    return req.json()


def get_emp(url, **kwargs):
    req = requests.get(url, params=kwargs)
    req.raise_for_status()
    return req.json()


def add_emp(url, **kwargs):
    req = requests.post(url, data=kwargs)
    req.raise_for_status()
    return req.json()


def delete_emp(url, **kwargs):
    req = requests.delete(url, data=kwargs)
    req.raise_for_status()
    return req.text


def update_emp(url, **kwargs):
    req = requests.put(url, json=kwargs)
    req.raise_for_status()
    return req.text


if __name__ == "__main__":
    emp_url = URL + 'employees'
    # print(json.dumps(get_all(URL+'employees'), indent=4))
    # print(add_emp(emp_url, id=1, employee_name='Ben'))
    # print(get_emp(emp_url, employee_name="Ben"))
    # print(delete_emp(emp_url, id=1))
    # print(get_emp(emp_url, employee_name="Ben"))
    # print(update_emp(emp_url, changes={'employee_salary': 20000},
    #                  who={'employee_name': 'other', 'id': '2'}))
