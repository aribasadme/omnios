# Live Coding Challenge

## Goals
1. Scrape the provided website to get the following data for all the listed books: title, star rating, price and picture URL.
2. Process: Complete previous data with the following params:
- Generate an ID for each book.
- Get the text of the book from this API*. The input text param should be like “The text of {title} is: “
- Translate the field text to some popular languages.
- Convert the price of the book to euros.
Output: Generate a file that contains all scraped data.

3. Create a database and fill it programmatically with the previously scraped data. The DB can be deployed in AWS or managed locally (but be aware of step 4!).

4. Query the database in a new script to retrieve the text of a book given its ID and language.

5. Deploy your solution to the cloud (step 4): Create a REST API in your favourite cloud provider that returns the text of a book when given ID as input and language.
