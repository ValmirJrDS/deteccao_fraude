def get_prediction(model, original_data, test_data):
    # Predição
    pred = model.predict(test_data)

    # Concatena a predicao aos dados originais e, se necessário,
    # aplica alguma operação aos resultados da predição.
    original_data["prediction"] = np.expm1(pred)

    return original_data.to_json(orient="records", date_format="iso")
