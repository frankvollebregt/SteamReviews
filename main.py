import crawler
import processor

ids = [379430, 582010, 493340, 275850, 391540]

# Crawl and store reviews
for id in ids:
    crawler.crawl(id, 'data_'+str(id))

# Process results
for id in ids:
    processor.process('data_'+str(id))
