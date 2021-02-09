import scrapy
from ..items import ArbisoftItem

class JobsSpider(scrapy.Spider):
    name = 'jobs'
    start_urls = [
        'https://news.ycombinator.com/jobs'
    ]

    def parse(self, response):

        things = ArbisoftItem()

        items = response.css("tr.athing, td.subtext")
        # main_list=[]
        for item in items:

            job_title = item.css("td.title a.storylink::text").get()
            company_url = item.css("td.title span.sitebit.comhead a span.sitestr::text").get()
            job_url = item.css("td.title a.storylink ::attr(href)").get()
            job_posting_date = item.css("span.age a::text").get()
            if job_title is not None:
                # main_list.append(job_title)
                # main_list.append(company_url or '')
                things['job_title'] = job_title
                things['company_url'] = company_url
            if job_url is not None:
                # main_list.append(job_url)
                things['job_url'] = job_url
            if job_posting_date is not None:
                # main_list.append(job_posting_date)
                things['job_posting_date'] = job_posting_date

            # things['job_title'] = job_title
            # things['company_url'] = company_url
            # things['job_url'] = job_url
            # things['job_posting_date'] = job_posting_date

            yield things

            print('done')
        # Job Titles Code:
        # job_titles = response.css(".storylink::text").getall()
        # titles = []
        # for item in job_titles:
        #     if 'hiring ' in item:
        #         item = item.split("hiring ")[1]
        #         if item.startswith('– '):
        #             item = item.replace('– ', '')
        #     elif 'Hiring ' in item:
        #         item = item.split("Hiring ")[1]
        #         if item.startswith('– '):
        #             item = item.replace('– ', '')
        #     titles.append(item)

        # Company Links Code:
        # full_jobs = response.css("tr.athing")
        # main_site_list = []
        # for item in full_jobs:
        #     company_link=item.css(".sitestr::text").get()
        #     main_site_list.append(company_link or "")

        # Job Links Code:
        # job_links = response.css(".storylink ::attr(href)").getall()
        # ycombinatorlink = 'https://news.ycombinator.com/'
        # links = []
        # for item in job_links:
        #     if 'http' not in item:
        #         item = ycombinatorlink + item
        #     links.append(item)

        # Time Ago Code:
        # time_ago = response.css(".age a::text").getall()
        # dates = []
        # for item in time_ago:
        #     if 'days' in item or 'day' in item:
        #         dates.append(str(datetime.date.today()-datetime.timedelta(days=int(item[:2]))))
        #     else:
        #         full_date = datetime.datetime.now()-datetime.timedelta(hours=int(item[:2]))
        #         simple_date = full_date.date()
        #         dates.append(str(simple_date))

        # For Next Page:
        # ycombinatorlink = 'https://news.ycombinator.com/'
        # next_page = ycombinatorlink + response.css("a.morelink::attr(href)")
        # if next_page:
        #     yield response.follow(next_page, callback=self.parse)

# job_titles = response.css(".storylink::text")[i].getall().lower().split("hiring")[1] # for job titles
# company_links = response.css(".sitestr::text").getall() # for company site (ycombinator links missing)
# job_links = response.css(".storylink ::attr(href)").getall() # for job sites (ycombinator jobs have id(RESOLVED))
# time_ago = response.css(".age a::text").getall()  # datetime.datetime.now()-datetime.timedelta(days_ago)) gives the
# posted date
