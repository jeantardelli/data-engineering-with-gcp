# Exercises

You are a data engineer at a book publishing company and your product manager has asked you to build a dashboard to show the total revenue and customer satisfaction index in a single dashboard.

Your company doesn't have any data infrastructure yet, but you know that your company has these three applications that contain TBs of data:

- The company website
- A book sales application using MongoDB to store sales transactions, including transactions, book ID, and author ID
- An author portal application using MySQL Database to store authors' personal information, including age

Do the following:

1. List important follow-up questions for your manager.

If we want to display information to our end users, undertanding of the data life cycle is important, therefore, important questions to ask include:

- Who will consume the data?
- What data sources should we use?
- Where should we store the data?
- When should the data arrive?
- Why does the data need to be stored in this place?
- How should the data be processed?
- Should it be streamlined data or it can be snapshots?

2. List your technical thinking process of how to do it at a high level.

 
Because we already have applications that collect data, that is, two applications with databases and one website (which generally have Google Analytics set up), the best approach here should be to use a Cloud Platform to collect and store data on a new Data Lake/Data Warehouse. Google Cloud Platform is a nice bet, because if the website uses Google Analytics we can have an [easy ingestion strategy with the website application](https://support.google.com/analytics/answer/9358801?hl=en&ref_topic=9359001). For the other two applications, we will need to think about how to collect this data.

It will certainly be an ETL or ELT, depending on the necessities of the business and the requirements of the data users. Anyway, we can use different techniques and approaches to collect such things, including building an Flask app that extracts data, using third-party tools or any available feature available on the Cloud Platform chosen.


3. Draw a data pipeline architecture.

The data pipeline can be something like this:

![imagen](https://user-images.githubusercontent.com/42701946/212650151-2f2caf5d-fe84-47f4-ab03-e9cf4f1683b9.png)
