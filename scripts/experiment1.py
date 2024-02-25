# pylint: skip-file

import tarfile
import os
import json
import requests
import csv
import sys
from datetime import datetime

from constants import ADDRESS, PORT, DATABASENAME, AUTH_DATABASE, AUTH_MECHANISM, USERNAME, PASSWORD, API_URL, API_STEPS_ALL, DATA_FOLDER

latex_template_begin = """
\\begin{table}[h]
\centering
\caption{Experiment 1 Reults} 
\scalebox{0.85} {
\\begin{tabular}{|l|c|c|c|c|c|c|}
\hline
\\textbf{Collection} & \\textbf{N\_JSON} & \\textbf{TB} & \\textbf{TT} & \\textbf{TB/TT} & \\textbf{TB/TT > 99\%} \\\ \hline 
"""

latex_template_end = """
\end{tabular}
}
\label{tab:exp1_result}
\end{table}
"""

def get_milisec_time(date):
    t = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return t.timestamp() * 1000


def extract_tarfile(dir_path):
    print(f"Extracting tarfiles in {dir_path}")

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.startswith("freebase") and file.endswith(".tar.bz2"):
                tarfile_path = os.path.join(root, file)
          
                with tarfile.open(tarfile_path, "r:bz2") as tar:
                    tar.extractall(path=root)
                    print(f"Extracted {tarfile_path} to {root}")
def get_ml(date):
    t = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%fZ")
    return t.timestamp() * 1000


def add_data(db_conn, dir):
    extract_tarfile(dir)
    print("Experiment 1: Adding data to the database")
    
    print(f"Adding data to the database from directory {dir}")
    collections = set()

    for root, dirs, files in os.walk(dir):
        for file in files:
            if file.endswith(".json"):
                curr_collection = root.split("/")[-1]

                if not curr_collection in collections:
                    print(f"Creating collection {curr_collection}")
                    collections.add(curr_collection)

                print(f"Adding data to collection {curr_collection}")

                file_path = os.path.join(root, file)
                print(f"Reading json data from {file_path}")

                with open(file_path, "r", encoding="utf-8-sig") as file_name:
                    for line in file_name.readlines():
                        try:
                            data = json.loads(line)
                        except json.JSONDecodeError as e:
                            line = "".join([char for char in line if ord(char) >= 32 and ord(char) <= 126])
                            data = json.loads(line)

                        db_conn[curr_collection].insert_one(data)

                    print(f"Inserted data from {file} into the database")

    return collections


def experiment_1(collections, token):
    print("Running Experiment")

    params = {
        "address": ADDRESS,
        "port": PORT,
        "databaseName": DATABASENAME,
        "authentication": {
            "authDatabase": AUTH_DATABASE,
            "authMechanism": AUTH_MECHANISM,
            "userName": USERNAME,
            "password": PASSWORD,
        }
    }

    results = []
    for collection in collections:
        print(f"Running experiment for collection {collection}")
        params["collectionName"] = collection
        response = requests.post(API_STEPS_ALL, json=params, headers={"Authorization": f"Bearer {token}"})

        if response.status_code == 200:
            result = response.json()
            batch_id = result["batchId"]
            response = requests.get(f"{API_URL}/batch/{batch_id}", headers={"Authorization": f"Bearer {token}"})
            results.append(response.json())

            print(f"Experiment for collection {collection} successful")
        else:
            print(f"Experiment for collection {collection} failed")
            print(response.text)
            sys.exit(1)

    return results
   
def verify_results_exp1(results):
    print("Verifying results for experiment 1")
    
                
def generate_results_exp1(results):
    print("Generating table for experiment 1")

    data = ""
    for result in results:
        start_date = get_milisec_time(result["startDate"])
        end_date = get_milisec_time(result["endDate"])
        union_date = get_milisec_time(result["unionDate"])
        tb = int(union_date - start_date)
        tt = int(end_date - start_date)
        tb_tt = round((tb / tt) * 100, 2)
        valid = "True" if tb_tt > 99 else "False"

        data += f"{result['collectionName']}&{result['collectionCount']}&{tb} ms & {tt} ms & {tb_tt}\\% & {valid} \\\\ \hline \n"
            
    latex_table = latex_template_begin + data + latex_template_end

    with open("/report/exp_1.tex", "w", encoding="utf-8") as file:
        file.write(latex_table)
        
def perform_experiment1(db_conn, token):
    print("==================================================================================")
    print("Performing experiment 1")
    add_data(db_conn, DATA_FOLDER)
    collections = ["drugs", "companies", "movies"]
    results = experiment_1(collections, token)
    verify_results_exp1(results)
    generate_results_exp1(results)
    print("Experiment 1 completed")
    print("==================================================================================")
    