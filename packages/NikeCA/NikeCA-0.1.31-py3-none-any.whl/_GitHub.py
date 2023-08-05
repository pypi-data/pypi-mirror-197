

class GitHub:

    def github_dependencies(self, tables: list | str = None, token: str = None, save_path: str | None = None):

        import pandas as pd
        import requests
        import re
        import random
        import time
        import json
        import os
        from github import Github as g
        import github

        from warnings import simplefilter
        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)

        if tables is str:
            tables = [tables]

        g = g(token)
        headers = {'Authorization': 'token ' + token}

        tables = [*set(tables)]
        print('Searching for ' + str(len(tables)) + ' tables in github')

        df = {}
        if save_path is not None:
            if os.path.isfile(save_path):
                with open(save_path) as f:
                    df = json.load(f)

        if 'TABLES_SEARCHED' not in df.keys():
            df['TABLES_SEARCHED'] = []
        if 'TABLES_NOT_SEARCHED' not in df.keys() or df['TABLES_NOT_SEARCHED'] is None:
            df['TABLES_NOT_SEARCHED'] = tables
        else:
            df['TABLES_NOT_SEARCHED'].append(tables)

        n = 3
        chunks = [tables[i:i + n] for i in range(0, len(tables), n)]

        lucky = 0
        counter = 1
        for chunk in chunks:

            used = requests.get('https://api.github.com/rate_limit', headers=headers).json()

            while used['resources']['search']['remaining'] < 3:
                lucky = 0
                dice = random.choice([2, 3, 4, 6, 7, 9, 10, 11, 12])

                print(f"\nWant to play?\nLet's roll the dice: \n\tYou rolled a {dice}\n\nIn the Jungle you must wait "
                      f"until the dice roll 5 or 8")

                print('\nYou must wait ' + str(int(used['resources']['search']['reset']) - int(time.time()) + 3) +
                      ' seconds before rolling again.\n')

                time_now = int(time.time())

                if int(used['resources']['search']['reset']) - int(time_now) > 0:
                    time.sleep(int(used['resources']['search']['reset']) - (time.time()) + 3)

                used = requests.get('https://api.github.com/rate_limit', headers=headers).json()

            if lucky == 0:
                lucky = 5
                dice = random.choice([5, 8])

                print(f"\nLet's roll the dice: \n\tYou rolled a {dice}\nPlease proceed:\n")

            for table in chunk:
                if table in df['TABLES_SEARCHED']:
                    if df['TABLES_NOT_SEARCHED'] is not None:
                        df['TABLES_NOT_SEARCHED'] = df['TABLES_NOT_SEARCHED'].remove(table)
                    continue

                while True:
                    try:
                        print(table)
                        search = g.search_code('org:nike-impr-analytics ' + table)
                    except StopIteration:
                        break
                    except:
                        print('sleeping')
                        time.sleep(600)
                        continue

                print('Searching ' + str(table) + ':\t\t\t\ttable number: ' + str(counter))

                for file in search:

                    result = requests.get(file.download_url)

                    result = result.text

                    indexes = [index.start() for index in re.finditer(table.upper(), result.upper())]

                    instance = 1
                    for index in indexes:
                        if index < 250:
                            index = 250
                        instance += 1

                        df[table] = {}
                        df[table][str(file.repository.name) + '/' + str(file.path)] = {}
                        df[table][str(file.repository.name) + '/' + str(file.path)]['Start'] = result[:1000]
                        df[table][str(file.repository.name) + '/' + str(file.path)]['lines'] = {}
                        df[table][str(file.repository.name) + '/' + str(file.path)]['lines'][str(index)] = \
                            result[index - 250: index + 250]

                time.sleep(2.001)

                counter += 1

                df['TABLES_SEARCHED'].append(table)

                if df['TABLES_NOT_SEARCHED'] is not None:
                    df['TABLES_NOT_SEARCHED'] = df['TABLES_NOT_SEARCHED'].remove(table)

            if save_path is not None:
                with open(save_path, "w+") as f:
                    json.dump(df, f, indent=4)

        return df
