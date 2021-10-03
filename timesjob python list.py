import requests

from bs4 import BeautifulSoup

url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords" \
      "=python&txtLocation= "

r = requests.get(url)

htmlContent = r.content

soup = BeautifulSoup(htmlContent, 'html.parser')

jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')



for job in jobs:
    title = job.find('h2').text.strip()

    # print(title.string)

    company_name = job.find('h3', class_='joblist-comp-name').text.strip()

    experience = job.find('ul', class_="top-jd-dtl clearfix")

    skill = job.find('span', class_='srp-skills').text.strip()

    job_description = job.find('ul', class_='list-job-dtl clearfix').find('li').text.replace('Job Description:',
                                                                                             '').replace(
        'Job Description :',
        '').strip()

    extra = job.find('ul', class_='top-jd-dtl clearfix').find_all('li')
    # .text.strip().replace('card_travel','')

    print('job title : ', title)
    print('company name : ', company_name)
    print('experience : ', extra[0].text.replace('card_travel', '').strip())
    print("location :", extra[1].text.replace('location_on', '').strip())
    print('skill : ', skill)
    print('job_description : ', job_description)
    print('\n\n\n\n\n\n')

    print(f'''
    Job title : {title}
    Company Name: {company_name}
    Experience : {extra[0].text.replace('card_travel', '').strip()}
    location : { extra[1].text.replace('location_on', '').strip()}
    Required Skills: {skill}
    job_description: {job_description}
''')

#
# # print(soup.find_all('li').get_text())
#
# # for x in soup.find_all('p'):
# # #     print(x.get_text())
#
#
# # all_links = set()
# #
# # for link in soup.find_all('a'):
# #     if "https" in link.get('href'):
# #         all_links.add(link.get('href'))
# #
# # print(all_links)
# #
# # print(soup.find(id='job_des').content)
#
#
# for x in soup.find_all('div', class_='job_nat'):
#     print(x.contents)
