import pandas as pd
import pickle
from flask import Flask, request, Response
from valmir.Valmir import Valmir

# Carrega o modelo oriundo da fase de teste do jupyter notebook
model = pickle.load(open("/model/model_valmir.pkl", "rb"))

# Inicializa a API
app = Flask(__name__)


@app.route("/valmir-model/predict", methods=["POST"])
def valmir_model_predict():
    test_json = request.get_json()

    if test_json:  # existe dados
        if isinstance(test_json, dict):  # pega apenas uma linha para testar
            test_raw = pd.DataFrame(test_json, index=[0])

        else:  # pega mais de uma linha
            test_raw = pd.DataFrame(test_json, columns=test_json[0].keys())

        # Chama a Classe Valmir com toda a pipeline de preprocessamento
        pipeline = Valmir()

        # data cleaning
        df1 = pipeline.data_cleaning(test_raw)

        # feature engineering
        df2 = pipeline.feature_engineering(df1)

        # data preparation
        df3 = pipeline.data_preparation(df2)

        # prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)

        return df_response

    else:
        return Response("{}", status=200, mimetype="application/json")


if __name__ == "__main__":
    app.run("0.0.0.0")
