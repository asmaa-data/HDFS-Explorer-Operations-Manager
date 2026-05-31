# HDFS-Explorer-Operations-Manager

A web-based management interface for Hadoop Distributed File System (HDFS) that provides an intuitive graphical alternative to command-line operations. The application enables administrators and data engineers to perform common HDFS file and directory management tasks through a browser-based interface built with Flask, HTML, CSS, and JavaScript.

## Overview

HDFS Operations Manager was developed to simplify interaction with Hadoop Distributed File System environments by providing a centralized graphical interface for file system navigation and administration.

Instead of executing Hadoop commands manually through the terminal, users can manage HDFS resources through an interactive web application that communicates with HDFS using Hadoop CLI commands.

This project demonstrates practical experience in Hadoop ecosystem administration, backend web development, Linux environments, and system integration.

## Features

### File System Navigation

* Browse HDFS directories
* Navigate nested folder structures
* Display file and directory metadata
* Interactive directory exploration

### File Management

* Upload files to HDFS
* Download files from HDFS
* Rename files
* Delete files
* View file contents directly from the interface

### Directory Management

* Upload directories
* Download directories
* Create directories
* Rename directories
* Move directories
* Delete directories

### Data Operations

* Copy files and directories between HDFS locations
* Move files and directories across the file system
* Preview file contents without downloading

### Access Control

* Restricted modification privileges
* Administrative write access limited to authorized user accounts
* Source code modification controls for application management

## System Architecture

Frontend:

* HTML
* CSS
* JavaScript

Backend:

* Python Flask

Storage Layer:

* Hadoop Distributed File System (HDFS) 2.7.3

Communication Layer:

* Hadoop CLI Commands

Operating Environment:

* CentOS 6 Linux

## Architecture Workflow

1. User interacts with the web interface.
2. Flask processes incoming requests.
3. Backend executes Hadoop CLI commands.
4. Commands communicate with HDFS.
5. Results are returned to the web interface.
6. Users receive real-time feedback on operations.

## Technology Stack

| Component            | Technology            |
| -------------------- | --------------------- |
| Frontend             | HTML, CSS, JavaScript |
| Backend              | Flask (Python)        |
| Distributed Storage  | Hadoop HDFS 2.7.3     |
| Operating System     | CentOS Linux          |
| Communication Method | Hadoop CLI Commands   |

## Supported HDFS Operations

| Operation            | Supported |
| -------------------- | --------- |
| Browse Directories   | Yes       |
| Upload Files         | Yes       |
| Upload Directories   | Yes       |
| Download Files       | Yes       |
| Download Directories | Yes       |
| Rename Files         | Yes       |
| Rename Directories   | Yes       |
| Copy Files           | Yes       |
| Copy Directories     | Yes       |
| Move Files           | Yes       |
| Move Directories     | Yes       |
| Delete Files         | Yes       |
| Delete Directories   | Yes       |
| Create Directories   | Yes       |
| View File Contents   | Yes       |
| File Search          | No        |

## Installation

### Prerequisites

* CentOS Linux
* Python 3.x
* Flask
* Hadoop 2.7.3
* Configured HDFS Cluster
* Hadoop CLI accessible from the system path


### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
python app.py
```

The application will be available at:

```text
http://localhost:5000
```

## Use Cases

* Hadoop cluster administration
* Distributed storage management
* Data engineering workflows
* Educational Hadoop environments
* Enterprise HDFS operations
* Rapid file management in distributed systems

## Project Highlights

* Developed a complete web interface for Hadoop HDFS administration.
* Integrated Flask backend with Hadoop CLI operations.
* Implemented file and directory lifecycle management.
* Designed an intuitive browser-based navigation experience.
* Built on Linux-based Hadoop infrastructure.
* Demonstrates practical distributed systems and big data engineering skills.

## Future Enhancements

* File search functionality
* Role-based access control
* Kerberos authentication support
* Multi-user management
* WebHDFS integration
* Docker deployment
* Cluster monitoring dashboard
* Audit logging
* REST API layer

## Disclaimer

This project was developed as a portfolio and learning project to demonstrate Hadoop ecosystem administration, distributed storage management, backend development, and web-based system integration skills.

## Author

Developed by Asmaa Shawkey Abd El-Salam rezk

For professional opportunities related to Big Data Engineering, Data Engineering, Hadoop Administration, or Backend Development, feel free to connect.
