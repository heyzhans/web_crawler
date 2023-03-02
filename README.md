# web_crawler

0. Crawling, saving to database, has HTTP API. Frontend is working, searching, showing pages.
1. IaaC - All infrastructure created using terraform and ansible. Based on lecture notes:
 - 3 docker nodes for stateless backend&frontend
 - 1 database machine for state
2. CI/CD - All deployment done automatically
3. Load test - 2 minutes test at least 1 req/sec (10k requests):
 - count percentage of errors
