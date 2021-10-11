import requests

from bs4 import BeautifulSoup

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit / 537.36(KHTML, like Gecko) Chrome / '
                  '92.0.4515.159Safari / 537.36',
}


def get_request(url, text=True):
    html_content = requests.get(url, headers=headers)
    val = html_content.text if text else html_content
    return val


class ExamVeda:
    def __init__(self, params):
        self.site_link = f"https://www.examveda.com/{params}"
        self.allQuestions = []

    def question_scrap_from_page(self, url):

        r = requests.get(url, headers=headers)
        htmlContent = r.content
        soup = BeautifulSoup(htmlContent, 'html.parser')
        question_list = soup.select('article.single-question.question-type-normal')
        print(question_list)

        for idx, x in enumerate(question_list):
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

                        self.all_questions.append(questionDetails)

            except (IndexError, Exception):
                print("Error something\n\n\n")
                continue

    def pagination_scrap(self, url):
        html_content = get_request(url)
        soup = BeautifulSoup(html_content, 'html.parser')
        page_len = len(soup.select('.pagination'))

        if page_len == 0:
            pass
            # print(url, soup.select('.pagination'), '\nwarn')
            # print('\n\n\n\n\n\n\n')

        else:
            soup = soup.select('.pagination')[0].text.strip().split('\n')
            page_len = len(soup)

            if "?section=" in url:
                url += "&page="

            else:
                if url[-1] != '/':
                    url += '/'

                url += "?page="

            page_no = 1

            while page_no <= page_len:
                self.question_scrap_from_page(f"{url}{page_no}")
                page_no += 1

    def question_scrap_from_section(self, soup, data):
        soup = soup.select('.page-content.chapter-section')

        all_section_url = []

        if len(soup) > 0:
            soup = soup[0].select('a')
            for url in soup:
                if "Section" in url.text:
                    all_section_url.append(url['href'])

        else:
            all_section_url.append(data['link'])

        for url in all_section_url:
            self.pagination_scrap(url)

    def all_questions_scrap(self, data):
        html_content = get_request(data['link'])
        soup = BeautifulSoup(html_content, 'html.parser')
        self.question_scrap_from_section(soup, data)
        # page_len = len(soup.select('.pagination')[0].text.strip().split('\n'))
        # page_no = 1
        #
        # while page_no<=page_len:
        #
        #     page_no += 1

    @staticmethod
    def sub_category_list(soup):
        soup = soup.select('.page-shortcode')[0].select('a')
        all_category_list = []

        for category in soup:
            all_category_list.append({'title': category.text, 'link': category['href']})

        return all_category_list

    def scrap_category(self):
        html_content = get_request(self.site_link)
        soup = BeautifulSoup(html_content, 'html.parser')
        all_category_list = self.sub_category_list(soup)

        # testing

        for data in all_category_list:
            self.all_questions_scrap(data)
            break


if __name__ == '__main__':
    obj = ExamVeda('mcq-question-on-competitive-english/')
    obj.scrap_category()
    print(obj.allQuestions)
