from typing import Dict, Optional
import requests
from tabulate import tabulate
from bs4 import BeautifulSoup
from getpass import getpass
 

def get_result(session: requests.Session, data: Dict[str, str]) -> str:

    url = 'https://sis.nileuniversity.edu.ng/my/index.php'
    params = {
        'ajx': '1',
        'mod': 'grader',
        'action': 'GetDetails',
        'did': data.get("did"),
        'sid': data.get("sid"),
        'stid': data.get("stid"),
        'yt': data.get("yt")
    }
    try:
        response = session.post(url, params=params, verify=False)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error: {str(e)}"

def check_my_future():

    username = str(input("Enter your student id: "))
    password = getpass(prompt="Enter password (Your Nile portal password): ")

    details = {
        "username": username,
        "password": password,
        "LogIn": "LOGIN"
    }

    try:
        session = requests.Session()
        dashboard = session.post('https://sis.nileuniversity.edu.ng/my/loginAuth.php', data=details, verify=False)
        soup = BeautifulSoup(dashboard.text, 'lxml')
        menus = soup.find_all("a", class_="has-arrow waves-effect waves-dark")

        for menu in menus:
            if menu["href"] == "?mod=grades":
                transcript = session.get('https://sis.nileuniversity.edu.ng/my/index.php', params={"mod": "grades"},
                                         verify=False)
                soup = BeautifulSoup(transcript.text, 'lxml')
                table = soup.find("table", class_="table table-hover vm no-th-brd pro-of-month")

                if table:
                    rows = table.find_all('tr')
                    rows_list = []

                    for row in rows:
                        cells = row.find_all(['th', 'td'])
                        cells_list = []

                        for cell in cells:
                            cells_list.append(cell.get_text(strip=True))

                            if cell.find('a'):
                                ajax_params = cell.a['onclick'].split("'")
                                data = {
                                    "did": ajax_params[1],
                                    "sid": ajax_params[3],
                                    "stid": ajax_params[5],
                                    "yt": int(ajax_params[6].split(")")[0].replace(",", ""))
                                }
                                # details = get_result(session, data) # This function doesn't seem to return the right response :(

                        rows_list.append(cells_list)

                    headers = rows_list[0]
                    body = rows_list[1:]

                    # Print the tabulated data
                    print(tabulate(body, headers=headers, tablefmt="grid"))
                    print("Created by Attahirny")
                else:
                    print("Table not found!")
                break

    except Exception as e:
        print(f"An Error occurred: {e}")

    
if __name__=="__main__":
    check_my_future()

    
