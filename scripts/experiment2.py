# pylint: skip-file

import tarfile
import os
import json
import requests
import csv
import sys

from constants import ADDRESS, PORT, DATABASENAME, AUTH_DATABASE, AUTH_MECHANISM, USERNAME, PASSWORD, API_URL, API_STEPS_ALL, DATA_FOLDER

latex_template_begin = """
\\begin{table}[h]
\centering
\caption{Experiment 2 Reults} 
\scalebox{0.85} {
\\begin{tabular}{|l|c|c|c|c|c|c|}
\hline
\multicolumn{2}{|c|}{\\textbf{Datasets}} & \multicolumn{2}{c|}{\\textbf{Experiment Results}} &
\multicolumn{2}{c|}{\\textbf{Frozza et al. \cite{frozza2018approach}}} \\\ \hline
\\textbf{Collection} & \\textbf{N\_JSON} & \\textbf{RS} & \\textbf{ROrd} & \\textbf{RS} & \\textbf{ROrd} \\\ \hline 
"""

latex_template_end = """
\end{tabular}
}
\label{tab:exp2_result}
\end{table}
"""

def extract_tarfile(dir_path):
    print(f"Extracting tarfiles in {dir_path}")

    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.startswith("dbpedia") and file.endswith(".tar.bz2"):
                tarfile_path = os.path.join(root, file)
          
                with tarfile.open(tarfile_path, "r:bz2") as tar:
                    tar.extractall(path=root)
                    print(f"Extracted {tarfile_path} to {root}")


def add_data(db_conn, dir):
    extract_tarfile(dir)
    print("Experiment 2: Adding data to the database")
    
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


def experiment_2(collections, token):
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
   
def verify_results_exp2(results):
    print("Verifying results for experiment 2")
    csv_results = {}

    with open("/ground_truth/exp2.csv", mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader) # Skip the header

        for row in csv_reader:
            print(f"Verifying result for collection {row[0]}")
            curr_result = [result for result in results if result["collectionName"] == row[0]][0]
            if curr_result["collectionCount"] == int(row[1]) and \
                curr_result["uniqueUnorderedCount"] == int(row[2]) and \
                curr_result["uniqueOrderedCount"] == int(row[3]):
                print(f"Result for collection {row[0]} matches with ground truth")
                csv_results[row[0]] = row
                continue
            else:
                print(f"Result for collection {row[0]} dont match with ground truth")
                
    return csv_results

def generate_results_exp2(results, csv_results):
    print("Generating table for experiment 2")

    data = ""
    for result in results:
        data += f"{result['collectionName']}&{result['collectionCount']}&{result['uniqueUnorderedCount']} \
            &{result['uniqueOrderedCount']} & {csv_results[result['collectionName']][2] } & {csv_results[result['collectionName']][3]} \
              \\\\ \hline \n"
            
    latex_table = latex_template_begin + data + latex_template_end

    with open("/report/exp_2.tex", "w", encoding="utf-8") as file:
        file.write(latex_table)
        

def perform_experiment2(db_conn, token):
    print("==================================================================================")
    print("Performing experiment 2")
    add_data(db_conn, DATA_FOLDER)
    collections = ["movies", "drugs", "companies"]
    results = experiment_2(collections, token)
    csv_results = verify_results_exp2(results)
    generate_results_exp2(results, csv_results)
    print("Experiment 2 completed")
    print("==================================================================================")