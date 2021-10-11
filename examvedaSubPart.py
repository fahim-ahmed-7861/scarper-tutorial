import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / 92.0.4515.159Safari / 537.36',
}
url = "https://www.examveda.com/competitive-english/practice-mcq-question-on-grammar/?section=2"

r = requests.get(url, headers=headers)

htmlContent = r.content

soup = BeautifulSoup(htmlContent, 'html.parser')

question_list = soup.select('article.single-question.question-type-normal')

all_questions = []

for idx, x in enumerate(question_list):

    # print('len :',len(x.select('.page-content')),x.select('.page-content').select('.div'))

    try:
        options = x.select('.question-inner')

        if len(options):
            questionDetails = {'question': x.select('div.question-main')[0].text, 'options': []}

            options = options[0].select('p')
            correct_ans = -1

            for index, op in enumerate(options):
                op = op.text.strip()

                if len(op) == 0:
                    correct_ans = int(options[index].select('input')[0]['value']) - 1
                    break

                optionDetails = {
                    'option': op[op.find('.') + 1:].strip(),
                    "is_correct": False, "explanation": ""
                }
                questionDetails['options'].append(optionDetails)

            if correct_ans != -1:
                questionDetails['options'][correct_ans]['is_correct'] = True

                if (len(x.select('.page-content'))) > 0:
                    explanation = x.select('.page-content')[0].select('div')[2].text
                    questionDetails['options'][correct_ans]['explanation'] = explanation[
                                                                             explanation.find(':') + 1:].strip()

                all_questions.append(questionDetails)

    except (IndexError, Exception):
        print("rorreeoamfdasdk")
        continue

for op in all_questions:
    print("question : ", op['question'])
    for os in op['options']:
        print(os)

    print('\n\n\n')
