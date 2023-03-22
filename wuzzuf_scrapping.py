import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest

def get_numPages(url):
    page = requests.get(url)
    html = BeautifulSoup(page.content, 'html.parser')
    num_pages = html.find("li", class_="css-8neukt").text.split(" ")[-1]
    return num_pages

job_title = []
job_company = []
job_postion = []
job_from = []
job_skill = []
link = []


page_nums = int(get_numPages(f"https://wuzzuf.net/search/jobs/?a=navbl&q=python&start={0}"))
for page_num in range(page_nums):
    try:
        # step 1: check and filtering
        url = f"https://wuzzuf.net/search/jobs/?a=navbl&q=python&start={page_num}"
        page = requests.get(url)
        # print(page.text)
        html = BeautifulSoup(page.content, 'html.parser')

        job_titles = html.find_all("h2", class_="css-m604qf")
        # print(job_titles)
        job_companys = html.find_all("a", class_="css-17s97q8")
        # print(job_companys)
        job_postions = html.find_all("span", class_="css-5wys0k")
        # print(job_postions)
        job_froms = html.find_all("div", class_="css-d7j1kk")
        # print(job_froms)
        job_skills = html.find_all("div", class_="css-y4udm8")
        # print(job_skills)

        # step2: loop on context (go inside href if you want)
        for i in range(len(job_titles)):
            # title: title.text
            job_title.append(job_titles[i].text.strip())

        #     # job_companys: company.text
            job_company.append(job_companys[i].text.strip()[:-1])

        #     # job_postions: job_postion.text
            job_postion.append(job_postions[i].text.strip())

        #     # job_froms: div + class(css-4c4ojb) and div + class(css-do6t5g)
            result = ""
            try:
                # is it 6 / 7 days
                result = job_froms[i].find("div", "css-4c4ojb").text
            except:
                # no
                result = job_froms[i].find("div", "css-do6t5g").text
            job_from.append(result.strip())

            # text but remove previouse element !!
            skill_text = job_skills[i].find("div", class_="css-1lh32fc").text.replace("Â·", '')
            l = len(skill_text)
            job_skill.append(job_skills[i].text[l:].strip())

            link.append("https://wuzzuf.net" + job_titles[i].find("a", class_="css-o171kl")["href"].strip())

        # print(job_title)
        # print()
        #
        # print(job_company)
        # print()
        #
        # print(job_postion)
        # print()
        #
        # print(job_from)
        # print()
        #
        # print(job_skill)
        # print(link)
        print(f"Extracting Page {page_num}")
    except:
        print("Error Happened while Extracting revise div/span/class/..")
        break

# step2`: get data from links
salary = []
req = []
for new_link in link:
    page = requests.get(new_link)
    # print(page.content)
    break
    html = BeautifulSoup(page.content, "html.parser")
    salary.append(html.find("span", class_="css-4xky9y"))
    req.append(html.find("div", class_="css-1t5f0fr"))

print(salary)
print()
print(req)


# step 3: make csv
file_list = [job_title, job_company, job_postion, job_from, job_skill, link, salary, req]
exported = zip_longest(*file_list)
with open("jobs.csv", 'w', encoding='utf-8', newline='') as f:
    thewriter = csv.writer(f)
    header = ['title', 'company', 'postion', 'from', 'skill', 'link', 'salay', 'requirements']
    thewriter.writerow(header)
    thewriter.writerows(exported)
#     # data
#     # for title, company, postion, from_time, skill in zip(job_title, job_company, job_postion, job_from, job_skill):
#     #     info = [title, company, postion, from_time, skill]
#     #     thewriter.writerow(info)





