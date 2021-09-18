# Resume-Shortlisting-and-Ranking-Tool

Resume Shortlisting and Ranking Tool - RSART

## Problem Statement

> Finding suitable candidates for an open role could be a daunting task, especially when there are many applicants. It can impede team progress for getting the right person on the right time. An automated way of “Resume Shortlisting and Ranking Tool” could really ease the tedious process of fair screening and shortlisting, it would certainly expedite the candidate selection and decisionmaking process.


## Introduction 

Resume shortlisting and screening is the process of determining whether a candidate is qualified for a role based his or her education, experience, and other information captured on their resume.

In a nutshell, it’s a form of pattern matching between a job’s requirements and the qualifications of a candidate based on their resume.
The goal of screening resumes is to decide whether to move a candidate forward – usually onto an interview – or to reject them.


## Why NLP

NLP for resume shortlisting and screening can handle massive volumes of data. In fact, NLP requires a lot of data in order to make accurate recommendations about which candidates to move forward to the next stage.
This means this Resume Shortlisting and Ranking software is most valuable for high volume recruitment such as retail sales or customer service roles.
The time you save screening resumes can be used in more valuable ways, whether it’s sourcing, engaging, or interviewing candidates to help determine how well they’ll fit in the job and company culture.

## Solution Overview

The main feature of the current solution is that it searches the entire resume database to select and display the resumes which fit the best for the provided job description(JD). This is, in its current form, achieved by assigning a score to each resume by intelligently comparing them against the corresponding Job Description.

## Instructions to Run the Tool 

* Download the code files

```
git clone https://github.com/PawanRamaMali/Resume-Shortlisting-and-Ranking-Tool.git 

```

* Install the required dependencies 

```
pip install -r requirements.txt 
```

* Run the tool

```
python app.py
```

* Open browser and visit `http://localhost:8000/` to view the application 

## Screenshots

### Home Page 

![image](https://user-images.githubusercontent.com/11299574/133888335-7104722a-32d1-4ba6-b897-242bb5a12176.png)

### Login Page

![image](https://user-images.githubusercontent.com/11299574/133888481-e645ddf8-15a4-48bd-acea-6b2d392bb58d.png)

Credentials 
* Username : admin
* Password : root

### Select Job Description

![image](https://user-images.githubusercontent.com/11299574/133888495-b83a0bae-e840-484d-914a-18e45803252d.png)

### View Candidates

![image](https://user-images.githubusercontent.com/11299574/133888501-2d15ba2e-5e52-41da-9115-5624925a65cd.png)


### Download Candidates 

![image](https://user-images.githubusercontent.com/11299574/133888509-77cf19eb-ac2d-4c7d-8592-336979f6c068.png)



## Version Control

### Version 0.1.0

#### Features
* Users can Login with default credentials
* Users can Select Job description from dropdown to search for all candidates matching with that job description
* The NLP algorithm will search for resumes matching the job description
* The resume search process has parser functions to match the text using NLP 
* The matching resumes are assigned a score and resumes with top 10 scores are selected
* The results page displays the list of resumes based on the score ranking 
* The results table also has a link to download column from where corresponding resume can be downloaded

### Issues
* The results is not showing showing the phone numbers correctly 
* Need to parse more information from resumes to be displayed in the results page
