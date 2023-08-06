from debater_python_api.api.debater_api import DebaterApi

def run_experiment(api_key, splits, validate=True):
    debater_api = DebaterApi(api_key)
    pro_con_client = debater_api.get_pro_con_client()
    if validate:
        df_test = splits["validate"]
    else:
        df_test = splits["test"]
    list_of_instances = []
    for i, record in df_test.iterrows():
        instance = record['claims.claimCorrectedText'], record["topicText"]
