Development Log — Day 1
Date: 01 July 2026

Objective: Set up the Equity Scanner project and build the initial version of the NSE historical data downloader.

Work Completed: Project Initialization, Created GitHub repository Equity-Scanner, Set up Python virtual environment, Added requirements.txt, .gitignore, and initial README.md, Created the project folder structure.

Project Architecture

Designed a modular project structure with separate folders for: Downloader, Processing, Scanner, Data, Database, Documentation and Downloader Development

Developed the core downloader modules:
calendar.py
urls.py
downloader.py
validator.py
logger.py
statistics.py
manager.py
NSE Archive Research
Studied the NSE Daily Reports page.
Verified the archive URL format for sec_bhavdata_full.
Tested downloading a single day's report successfully.
Downloader Features Implemented
Date generation
Weekend detection
URL generation
Retry mechanism
Download manager
Progress tracking
CSV validation
Logging
Download statistics
Testing
Successfully downloaded a single bhavcopy file.
Verified file naming convention and storage.
Challenges Faced
Python package import issues.
Understanding the NSE archive URL structure.
Designing a scalable project architecture.
Outcome
✅ Project architecture finalized and initial downloader implemented successfully.

Development Log — Day 2

Date: 02 July 2026

Objective

Complete and validate the historical NSE downloader for two years of market data.

Work Completed
Architecture Finalization
Froze the overall project structure.
Converted the project into a package-based architecture using __init__.py.
Standardized imports across all modules.
Downloader Improvements

Enhanced the downloader by implementing:

Modular download manager
Lightweight CSV validation
Detailed download logging
Download statistics with execution time
Resume support (skip existing files)
Better progress reporting
Debugging & Issue Resolution

Investigated a major issue where all downloads were marked as failed.

Observed:

HTTP status returned 200 OK.
Files were being downloaded.
Validator rejected every file.

Root Cause:

NSE CSV files contained a UTF-8 Byte Order Mark (BOM).
Header validation failed because the first column was read as \ufeffSYMBOL.

Solution:

Updated file reading to use encoding="utf-8-sig".
Successfully resolved the validation issue.
Full Historical Download

Downloaded historical Full Bhavcopy + Security Delivery reports.

Period Covered

01 July 2024
01 July 2026

Download Summary

Total Dates       : 731
Weekend           : 208
Trading Days      : 523

Downloaded        : 510
Already Exists    : 1
Holiday           : 12
Failed            : 0

Elapsed Time      : 07:04
Achievements
Built a production-ready historical downloader.
Successfully collected two years of NSE equity data.
Completed Downloader v1.0.
Key Learnings
Python package management and imports.
HTTP session handling.
Debugging download pipelines.
CSV encoding (UTF-8 BOM) issues.
Building modular and maintainable software.
Outcome

✅ Milestone 1 Completed — Historical Data Ingestion Engine