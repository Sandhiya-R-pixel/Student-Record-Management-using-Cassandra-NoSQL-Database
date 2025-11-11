# Student-Record-Management-using-Cassandra-NoSQL-Database
## 🎯 SDG 4 – Quality Education
## 📌 Project Title
Student Record Management using Cassandra NoSQL Database
## 🧠 Objective
The main objective of this project is to design and implement a simple student record management system using Apache Cassandra, a distributed NoSQL database that provides high availability, scalability, and fault tolerance.
This project demonstrates how to store, retrieve, update, and delete student data efficiently in a non-relational environment — supporting the Sustainable Development Goal (SDG) 4: Quality Education by promoting better educational data management systems.
## 🧩 Abstract
In educational institutions, handling student records efficiently is essential. Traditional relational databases face challenges in scalability and high availability when the data volume increases.
This project uses Cassandra, a NoSQL key–value and column-family database, to overcome those limitations by providing distributed data storage, replication, and high fault tolerance.
It allows administrators to perform CRUD operations on student data such as name, age, gender, department, email, and admission date in a distributed, reliable manner.
## ⚙️ Features
✅ Create a new student record
✅ Retrieve student details using Student ID
✅ Update existing student information (e.g., email)
✅ Delete a student record
✅ View all stored students
✅ Keyspace and Table auto-created if not available
✅ Uses UUID for unique student identification
✅ Supports Cassandra data replication for reliability
✅ Uses prepared statements for efficient and secure queries
## 💡 Tools and Technologies 
Used
Category
Technology
Programming Language
Python 3.x
Database
Apache Cassandra (NoSQL)
Driver / Library
cassandra-driver
Query Language
CQL (Cassandra Query Language)
IDE / Editor
VS Code / PyCharm
Version Control
Git and GitHub
Concept
Key-Value Model, Data Replication
## 🏗️ System Architecture
Copy code

+------------------------+
|   Python Application   |
| (student_cassandra.py) |
+-----------+------------+
            |
            |  Cassandra Driver
            v
+---------------------------+
|    Apache Cassandra DB    |
|  Keyspace: school         |
|  Table: students          |
+---------------------------+
## 🧮 Database Design
Keyspace: school
Table: students
Column Name
Data Type
Description
student_id
uuid
Unique identifier (Primary Key)
name
text
Student's full name
age
int
Student's age
gender
text
Gender
department
text
Department name
email
text
Email ID
admission_date
date
Date of admission
## 🧑‍💻 Operations Performed (CRUD)
Operation
Description
Function
Create
Add new student record
insert_student()
Read
Retrieve student details
get_student_by_id()
Update
Modify student email
update_student_email()
Delete
Remove a student record
delete_student()
List
Display all student records
list_all_students()
## 🟢 Benefits

Scalability: Cassandra handles large volumes of student data across multiple servers efficiently.

High Availability: Even if one node fails, data remains accessible due to replication.

Fast Performance: Supports quick read/write operations, improving access speed for student records.

Data Consistency & Reliability: Ensures reliable data management through tunable consistency.

Simplified Data Model: Uses a flexible NoSQL structure suitable for unstructured or semi-structured student data.

## 🌍 Impacts

Supports SDG 4 (Quality Education): Enables institutions to manage and analyze student information effectively for better learning outcomes.

Enhances Administrative Efficiency: Reduces manual work in maintaining and searching records.

Data-Driven Decision Making: Helps educators analyze performance trends for better academic planning.

Promotes Digital Transformation: Shifts traditional paper-based systems to digital, accessible databases.

## 🚀 Future Scope

Integration with Machine Learning models to predict student performance and dropout risks.

Addition of web or mobile dashboards for student and admin access.

Implementing role-based authentication for data privacy.

Connecting with cloud-based Cassandra clusters (e.g., DataStax AstraDB) for global scalability.

Adding real-time analytics and automated report generation features.

## 💡 Real-Life Example

Universities and Schools: Large institutions like MIT or Stanford could use Cassandra-based systems to manage thousands of student profiles, attendance, marks, and course data in real-time.

Online Education Platforms (e.g., Coursera, edX): They use scalable NoSQL databases to store learner activity, progress, and certifications globally with minimal downtime.
