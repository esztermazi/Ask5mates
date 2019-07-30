import csv


def get_header(data_type):
    if data_type == "question":
        question_header = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
        return question_header
    elif data_type == "answer":
        answer_header = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']
        return answer_header


def get_file_path(data_type):
    if data_type == "question":
        question_file_path = 'sample_data/question.csv'
        return question_file_path
    elif data_type == "answer":
        answer_file_path = 'sample_data/answer.csv'
        return answer_file_path


def get_data_from_csv(data_type):
    file_path = get_file_path(data_type)
    with open(file_path, newline='') as data_file:
        all_data = csv.DictReader(data_file)
        return list(all_data)


def write_new_line_to_csv(dicti, data_type):
    file_path = get_file_path(data_type)
    fieldnames = get_header(data_type)
    with open(file_path, 'a') as data_file:
        all_data = csv.DictWriter(data_file, fieldnames)
        all_data.writerow(dicti)


def rewrite_csv(dictionaries, data_type):
    file_path = get_file_path(data_type)
    fieldnames = get_header(data_type)
    with open(file_path, 'w') as data_file:
        all_data = csv.DictWriter(data_file, fieldnames)
        all_data.writeheader()
        all_data.writerows(dictionaries)



