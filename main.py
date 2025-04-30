import argparse
from findCompanies import Extract_text_from_pdf,Firecrawl_crawl,Extract_titles,parse_job_listings,scrape_google_jobs

def main():
    parser = argparse.ArgumentParser(description="Job Matcher CLI")
    
    parser.add_argument('--resume', type=str, required=True, help='Path to your resume PDF')
    parser.add_argument('--threshold', type=float, default=0.8, help='Matching threshold (default: 0.8)')
    parser.add_argument('--company', type=str, nargs='+',default="", help='List of company names to target')

    args = parser.parse_args()

    # print(f"Resume: {args.resume}")
    # # print(Extract_text_from_pdf(args.resume))
    # print(Firecrawl_crawl('https://www.google.com/about/careers/applications/jobs/results/'))

    #titles = Extract_titles()
    # for t in titles:
    #     print("-", t)


    # Usage
    jobs = scrape_google_jobs("https://www.google.com/about/careers/applications/jobs/results/")
if __name__ == "__main__":
    main()