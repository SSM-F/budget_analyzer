def formated_data(columns,raw_data):
    formated_result = []
    for data in raw_data:
        data_dict = dict(zip(columns,data))
        formated_result.append(data_dict)
    return formated_result