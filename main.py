import requests

from bs4 import BeautifulSoup


def details_page(pageUrl, index, f):
    # print(pageUrl)
    req = requests.get(pageUrl)

    html = req.content

    bsoup = BeautifulSoup(html, 'html.parser')

    job_des = bsoup.find('div', class_="jd-desc job-description-main")
    skilltype = bsoup.find_all('span', class_='jd-skill-tag')
    # print(skilltype)

    f.write(f"Job job_des : {job_des} \n\n")
    f.write(f"skilltype : {skilltype} \n\n")
    f.close()


def mainPage(id):
    url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=I&sequence=1&startPage={id}"
    r = requests.get(url)

    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    # print(jobs)

    for index, job in enumerate(jobs):
        title = job.find('h2').text.strip()

        company_name = job.find('h3', class_='joblist-comp-name').text.strip()

        skill = job.find('span', class_='srp-skills').text.strip()

        job_description = job.find('ul', class_='list-job-dtl clearfix').find('li').text.replace('Job Description:',
                                                                                                 '').replace(
            'Job Description :',
            '').strip()

        extra = job.find('ul', class_='top-jd-dtl clearfix').find_all('li')

        details_url = job.header.h2.a['href']

        experience = extra[0].text.replace('card_travel', '').strip()
        Location = extra[1].text.replace('location_on', '').strip()

        pageNo =(id-1)*25
        pageNo+=index+1

        print(pageNo)

        with open(f"posts/job {pageNo}.txt", 'w', encoding='ut'
                                                           ''
                                                           ''
                                                           ''
                                                           ''
                                                           'f8') as f:
            f.write(f"Job title : {title} \n\n")
            f.write(f"Company_name : {company_name} \n\n")
            f.write(f"Experience : {experience} \n\n")
            f.write(f"Location : {Location} \n\n")
            f.write(f"Required Skills : {skill} \n\n")
            f.write(f"Job_description : {job_description} \n\n")
            f.write(f"details_url : {details_url} \n\n")
            details_page(details_url, index, f)


idx = 1

emlen = 1000

while emlen > 2:
    mainPage(idx)
    idx += 1
    url = f"https://www.timesjobs.com/candidate/job-search.html?from=submit&actualTxtKeywords=python&searchBy=0&rdoOperator=OR&searchType=personalizedSearch&luceneResultSize=25&postWeek=60&txtKeywords=python&pDate=I&sequence=21&startPage={idx}"

    r = requests.get(url)

    htmlContent = r.content

    soup = BeautifulSoup(htmlContent, 'html.parser')

    allEm = soup.find('div', class_='srp-pagination clearfix')

    emLen = 0 if allEm is None else len(allEm.find_all('em'))
