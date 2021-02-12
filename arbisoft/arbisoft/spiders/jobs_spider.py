import scrapy
import datetime
from ..items import JobItem
import re


class JobsSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://news.ycombinator.com/jobs'
    ]

    def parse(self, response):

        jobs = JobItem()

        items = response.css("tr.athing td.title, td.subtext")
        job_titles = []
        company_urls = []
        job_urls = []
        job_posting_dates = []
        ycombinatorlink = 'https://news.ycombinator.com/'
        for item in items:

            job_title = item.css("a.storylink::text").get()
            company_url = item.css("span.sitebit.comhead a span.sitestr::text").get()
            job_url = item.css("a.storylink ::attr(href)").get()
            job_posting_date = item.css("span.age a::text").get()
            if job_posting_date:
                if 'days' in job_posting_date and int(job_posting_date[:2]) > 5:
                    break
            if job_posting_date:
                if 'day' in job_posting_date:
                    job_posting_dates.append(str(datetime.date.today() -
                                                 datetime.timedelta(days=int(job_posting_date[:2]))))
                elif 'hour' in job_posting_date:
                    full_date = datetime.datetime.now() - datetime.timedelta(hours=int(job_posting_date[:2]))
                    simple_date = full_date.date()
                    job_posting_dates.append(str(simple_date))

            if job_title:
                pattern = re.compile(r'(?<=[hH]iring ).*')
                matches = pattern.finditer(job_title)
                for match in matches:
                    job_titles.append(match[0])

                company_urls.append(company_url or '')

            if job_url:
                if 'http' not in job_url:
                    job_url = ycombinatorlink + job_url
                job_urls.append(job_url)
            # print('done')
        jobs_zip_object = zip(job_titles, company_urls, job_urls, job_posting_dates)
        jobs_list = list(jobs_zip_object)
        for item in jobs_list:
            if jobs_list:
                jobs['job_title'] = job_titles[jobs_list.index(item)]
                jobs['company_url'] = company_urls[jobs_list.index(item)]
                jobs['job_url'] = job_urls[jobs_list.index(item)]
                jobs['job_posting_date'] = job_posting_dates[jobs_list.index(item)]
                yield jobs
        next_page = response.css("a.morelink::attr(href)").get()
        # print(next_page)
        if next_page:
            if job_posting_date:
                if 'days' in job_posting_date and int(job_posting_date[:2]) > 5:
                    yield response.follow(next_page, callback=self.parse)


            # if job_title:
            #     if 'hiring ' in job_title:
            #         job_title = job_title.split("hiring ")[1]
            #         if job_title.startswith('– '):
            #             job_title = job_title.replace('– ', '')
            #     elif 'Hiring ' in job_title:
            #         job_title = job_title.split("Hiring ")[1]
            #         if job_title.startswith('– '):
            #             job_title = job_title.replace('– ', '')
            #     job_titles.append(job_title)
            #     company_urls.append(company_url or '')
