import json

raw_dataset_path = "C:\\Users\\User\\Desktop\\ecg_data_200.json"  # файл с датасетом


def get_signal_snippet(lead_name='i', start_coord=23, end_coord=435):
    case_id = '1102625626'

    with open(raw_dataset_path, 'r') as f:
        data = json.load(f)

        leads = data[case_id]['Leads']
        full_signal = leads[lead_name]['Signal']
        signal_snippet = full_signal[start_coord:end_coord]
        return signal_snippet


if __name__ == "__main__":
    import matplotlib.pyplot as plt

    signal_snippet = get_signal_snippet()

    fig, ax = plt.subplots()
    ax.plot(signal_snippet)
    plt.show()

