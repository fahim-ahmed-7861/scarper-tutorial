import requests

from bs4 import BeautifulSoup


def details_page(pageUrl):
    # print(pageUrl)
    req = requests.get(pageUrl)

    html = req.content

    bsoup = BeautifulSoup(html, 'html.parser')

    job_des = bsoup.find('div', class_="jd-desc job-description-main")
    basic_info = bsoup.find('div', class_='job-basic-info').find('a', class_='')
    skilltype = bsoup.find_all('span', class_='jd-skill-tag')
    # if len(job_des) > 0:
    #     if job_des[0] == ":":
    #         job_des = job_des[1:]

    print(skilltype, '\n\n\n\n\n')


url = "https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords" \
      "=python&txtLocation= "

r = requests.get(url)

htmlContent = r.content

soup = BeautifulSoup(htmlContent, 'html.parser')

jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

# print(jobs)

for index, job in enumerate(jobs):
    title = job.find('h2').text.strip()

    # print(title.string)

    company_name = job.find('h3', class_='joblist-comp-name').text.strip()

    # experience = job.find('ul', class_="top-jd-dtl clearfix")

    skill = job.find('span', class_='srp-skills').text.strip()

    job_description = job.find('ul', class_='list-job-dtl clearfix').find('li').text.replace('Job Description:',
                                                                                             '').replace(
        'Job Description :',
        '').strip()

    extra = job.find('ul', class_='top-jd-dtl clearfix').find_all('li')

    details_url = job.header.h2.a['href']
    # .text.strip().replace('card_travel','')

    # print('job title : ', title)
    # print('company name : ', company_name)
    # print('experience : ', extra[0].text.replace('card_travel', '').strip())
    # print("location :", extra[1].text.replace('location_on', '').strip())
    # print('skill : ', skill)
    # print('job_description : ', job_description)
    # print('\n\n\n\n\n\n')
    experience = extra[0].text.replace('card_travel', '').strip()
    Location = extra[1].text.replace('location_on', '').strip()
    details_page(details_url)

    with open(f"posts/job {index + 1}.txt", 'w', encoding='utf8') as f:
        f.write(f"Job title : {title} \n\n")
        f.write(f"Company_name : {company_name} \n\n")
        f.write(f"Experience : {experience} \n\n")
        f.write(f"Location : {Location} \n\n")
        f.write(f"Required Skills : {skill} \n\n")
        f.write(f"Job_description : {job_description} \n\n")
        f.write(f"details_url : {details_url} \n\n")
        f.close()
    #     f.write(f'''
    # Job title : {title}
    # Company Name: {company_name}
    # Experience : {extra[0].text.replace('card_travel', '').strip()}
    # location : { extra[1].text.replace('location_on', '').strip()}
    # Required Skills: {skill}
    # job_description: {job_description}
    # details_url: {details_url}''')
