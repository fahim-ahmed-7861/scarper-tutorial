import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs


class BdJobsScrapper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'authority': 'jobs.bdjobs.com'
        })
        self.base_url = 'https://www.bdjobs.com/'
        self.jobs_base_url = 'https://jobs.bdjobs.com/'
        self.job_search_url = 'https://jobs.bdjobs.com/jobsearch.asp'
        self.government_jobs_url = 'https://jobs.bdjobs.com/JobSearch.asp?fcatId=-1&icatId=0&requestType=government'
        self.dictionary = {
            'Published on:': 'published_on',
            'Vacancy:': 'vacancy',
            'Employment Status:': 'emp_status',
            'Experience:': 'experience',
            'Gender:': 'gender',
            'Age:': 'age',
            'Job Location:': 'job_location',
            'Salary:': 'job_salary',
            'Application Deadline:': 'deadline',
            'Job Responsibilities': 'responsibilities',
            'Job Context': 'context'
        }

    @staticmethod
    def parse_location(text):
        location = {
            'street_address': '',
            'country': 'Bangladesh'
        }
        if text.find('(') != -1:
            location['state'] = text[:text.find('(')].strip()
            location['city'] = text[text.find('(') + 1:-1].strip()
        else:
            location['state'] = text
        return location

    @staticmethod
    def _scrape_functional_industrial(soup, c_type):
        categories = []
        for category in soup:
            try:
                link = category['href']
                title = category['title']
                parsed_url = urlparse(link)
                _id = 0
                if c_type == 'Industrial':
                    _id = int(parse_qs(parsed_url.query).get('icatId')[0])
                else:
                    _id = int(parse_qs(parsed_url.query).get('fcatId')[0])

                categories.append({
                    'id': _id,
                    'type': c_type,
                    'url': "https:" + link,
                    'title': title
                })
            except (KeyError, Exception):
                pass
        return categories

    def scrape_categories(self):
        res = self.session.get(self.base_url)
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')

        functional_soup = soup.select('.category-list')[0].select('a')
        industrial_soup = soup.select('.category-list')[1].select('a')
        special_skilled_soup = soup.select('.category-list')[2].select('a')

        categories = []
        categories.extend(self._scrape_functional_industrial(functional_soup, 'Functional'))
        categories.extend(self._scrape_functional_industrial(industrial_soup, 'Industrial'))
        categories.extend(self._scrape_functional_industrial(special_skilled_soup, 'Special Skilled'))

        return categories

    @staticmethod
    def _scrape_content_from_class(soup, class_str, index=0):
        try:
            return soup.select(f'.{class_str}')[index].prettify()
        except (IndexError, Exception) as e:
            return ''

    @staticmethod
    def _scrape_text_from_class(soup, class_str, index=0):
        try:
            return soup.select(f'.{class_str}')[index].text.strip()
        except (IndexError, Exception) as e:
            return ''

    @staticmethod
    def _scrape_content_from_tag(soup, tag_str, index=0):
        try:
            return soup.select(f'{tag_str}')[index].prettify().replace('\n', '')
        except (IndexError, Exception) as e:
            return ''

    @staticmethod
    def _scrape_text_from_tag(soup, tag_str, index=0):
        try:
            return soup.select(f'{tag_str}')[index].text.strip()
        except (IndexError, Exception) as e:
            return ''

    @staticmethod
    def _scrape_text_from_class_and_tag(soup, class_str, tag_str, cls_index=0, tg_index=0):
        try:
            return soup.select(f'.{class_str}')[cls_index].select(f'{tag_str}')[tg_index].text.strip()
        except (IndexError, Exception) as e:
            return ''

    @staticmethod
    def _scrape_content_from_class_and_tag(soup, class_str, tag_str, cls_index=0, tg_index=0):
        try:
            return soup.select(f'.{class_str}')[cls_index].select(f'{tag_str}')[tg_index].prettify().replace(
                '\n', ''
            )
        except (IndexError, Exception) as e:
            return ''

    def _get_description_obj(self, soup, class_str='job_des'):
        description = {}
        for des in soup.select(f'.{class_str}'):
            key = self._scrape_text_from_tag(des, 'h4')
            description[self.dictionary.get(key, 'unknown')] = self._scrape_content_from_tag(des, 'ul')
        return description

    def _get_summary_obj(self, soup):
        summary = {}
        try:
            soup = soup.select('.job-summary')[0].select('.panel-body')[0]
            for h4 in soup.select('h4'):
                key = self._scrape_text_from_tag(h4, 'strong')
                summary[self.dictionary.get(key, 'unknown')] = h4.contents[-1].strip()
        except (IndexError, Exception):
            pass
        return summary

    def _get_requirements(self, soup, class_str='edu_req'):
        req_str = ''
        for req in soup.select(f'.{class_str}'):
            req_str += self._scrape_content_from_tag(req, 'ul')
        return req_str

    def _get_job_category(self, soup):
        soup = soup.select('.category-wrapper')[0]
        text = self._scrape_text_from_tag(soup, 'p')
        key = text[:text.find(':')].strip()
        value = text[text.find(':') + 1:].strip()
        return value if key == 'Category' else 'Government'

    @staticmethod
    def _get_company_info(soup):
        info = {'address': '', 'web': '', 'business': ''}
        try:
            soup = soup.select('.company-info')[0].select('.information')[0]
            for index, span in enumerate(soup.select('span')):
                if index < 2:
                    continue
                text = span.text.strip()
                key = text[:text.find(':')].strip()
                value = text[text.find(':') + 1:].strip()
                if key:
                    info.update({key.lower(): value})
        except (IndexError, Exception):
            pass
        return info

    def _get_location(self, soup):
        return self._scrape_text_from_class_and_tag(soup, 'job_loc', 'p')

    @staticmethod
    def _get_image(soup):
        try:
            return soup.select('.image')[0].select('img')[0]['src']
        except (IndexError, Exception):
            return ''

    def scrape_job(self, job_url: str):
        print(job_url)
        res = self.session.get(job_url)
        soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')

        if len(soup.select('.job_source')) > 1:
            # TODO: Implement foreign job detection in proper way
            print("Foreign Job skipped")
            return None

        # TODO: EmploymentStatus is not scrapped properly for some jobs, needs modifications
        # TODO: parse_location function is not valid for some jobs, needs modifications

        job_details = {
            'url': job_url,
            'title': self._scrape_text_from_class(soup, 'job-title'),
            'image': self._get_image(soup),
            'category': self._get_job_category(soup),
            'company_name': self._scrape_text_from_class(soup, 'company-name'),
            'company_info': self._get_company_info(soup),
            'company_location': self.parse_location(self._get_location(soup)),
            'vacancy': self._scrape_text_from_class_and_tag(soup, 'vac', 'p'),
            'employment_status': self._scrape_text_from_class_and_tag(soup, 'job_nat', 'p'),
            'workspace': self._scrape_text_from_class_and_tag(soup, 'job_nat', 'ul', cls_index=1),
            'salary': self._scrape_content_from_class_and_tag(soup, 'salary_range', 'ul'),
            'benefits': self._scrape_content_from_class_and_tag(soup, 'oth_ben', 'ul'),
            'reference': self._scrape_text_from_class_and_tag(soup, 'job_source', 'p'),
            'requirements': self._get_requirements(soup),
            'additional_requirements': self._get_requirements(soup, class_str='job_req'),
            'instructions': self._scrape_content_from_class(soup, 'instruction-details')
        }
        job_details.update(self._get_description_obj(soup))
        job_details.update(self._get_summary_obj(soup))
        print(
            '''
            {}
            '''
        )
        return job_details

    def scrape_jobs(self, category_id, param_key='fcatId', govt_job=False):
        page, jobs = 1, []
        url = self.job_search_url + f'?{param_key}={category_id}' if not govt_job else self.government_jobs_url
        cookies = {'JOBSRPP': '40'}
        data = {
            param_key[:4]: category_id,
            'hClickLog': 1,
            'hPopUpVal': 1
        }

        while True:
            data.update({
                'pg': page
            })
            res = self.session.post(url, data=data, cookies=cookies)
            soup = BeautifulSoup(res.content.decode('utf-8'), 'html.parser')
            list1 = soup.select('.norm-jobs-wrapper')
            list2 = soup.select('.sout-jobs-wrapper')
            for job in list1:
                _job = self.scrape_job(self.jobs_base_url + job.select('a')[0]['href'])
                _job and jobs.append(_job)
            for job in list2:
                _job = self.scrape_job(self.jobs_base_url + job.select('a')[0]['href'])
                _job and jobs.append(_job)

            print(f"Scrapped {len(jobs)} jobs from {page} pages")
            if not len(list1) or not len(list2):
                break
            break
            page += 1

        return jobs

    def scrape(self):
        data = {
            'categories': self.scrape_categories(),
            'jobs': self.scrape_jobs(-1, govt_job=True)  # scrapes government jobs
        }

        for category in data['categories']:
            if category.get('type') == 'Industrial':
                data['jobs'].extend(self.scrape_jobs(category.get('id'), 'icatId'))
            else:
                data['jobs'].extend(self.scrape_jobs(category.get('id')))

            print(f"Scrapped {len(data['jobs'])} jobs")

        return data


BdJobsScrapper().scrape_job('https://jobs.bdjobs.com/jobdetails.asp?id=995764&fcatId=4&ln=1')
