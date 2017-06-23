# Log Analysis Project

## Overview

This project creates a data analysis tool to interpret data retrieved from a website data log. This tool attempts to find the answer to the following questions.

1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3.  On which days did more than 1% of requests lead to errors?

## Setup

This project requires the use of a Vagrant, a virtual machine, which runs PostgreSQL, a relational database server.

### Install Virtual Box

Vagrant runs on Virtual Box, so it will need to be installed first. Install from [here.][44e599f1]

  [44e599f1]: https://www.virtualbox.org/wiki/Downloads "Virtual Box Installation"

### Install Vagrant
Vagrant configures the virtual machine and enables file sharing between your computer and the virtual machine. It can be installed [here.][d1fb35c2]

  [d1fb35c2]: https://www.vagrantup.com/downloads.html "Vagrant Download"

### Download Virtual Machine Configuration

This Github repository contains the files necessary to configure the virtual machine and access the SQL data base. It can be forked  [here.][505f3dcf]

  [505f3dcf]: https://github.com/udacity/fullstack-nanodegree-vm "VM configuration files"

### Starting the Virtual Machine

From a terminal window, from within the vagrant subdirectory, run the command `vagrant up`. After the VM completes its startup, you can run `vagrant ssh` to log into the machine.

### Running newsdata.py

The newsdata.py file contains the python and SQL code that will analyze the news database. This file should be located within the vagrant shared directory. From a terminal window, log into vagrant and `cd /vagrant` to open the shared directory. Enter `python newsdata.py` to run the analysis tool. You should see the report within your terminal window and it should output to the logreader.txt file.

### Files

newsdata.py - The python file which performs the analysis on the SQL database.

logreader.txt - This is the output of the newsdata.py. It should report the analysis done on the SQL database.

### Resources used

I was unable to connect to the news database when it was intially installed, this [forum post.][867a8aeb] contained instructions to create an empty news databse, which enabled me to connect.

  [867a8aeb]: https://discussions.udacity.com/t/fixed-psql-fatal-database-news-does-not-exist-even-after-reinstalling-vagrant/247490 "Database post"

  This [forum post][69ca8226] outlined the `'CONCAT/article/'` method used in questions 1 and 2 to compare the data in `atricles.slug` and `log.path`.

  [69ca8226]: https://discussions.udacity.com/t/comparing-articles-slug-to-log-path/249717 "forum post"

  This [forum post][a6769ce6] clued me into the `CASE` method an allowed me to create question 3 SQL query with the suggestion to use views in the database and, in particular, using FLOAT to eliminate rounding, since my intial queries were coming back as zero.

  [a6769ce6]: https://discussions.udacity.com/t/logs-analysis-query-3/249907/2 "forum post"

  These resources were also used:

[  POSTGRESQL Documentation](https://www.postgresql.org/docs/)

[Stack Overflow- Convert to FLOAT](https://stackoverflow.com/questions/28736227/postgresql-9-3-convert-to-float)

[SQL Beautifier](http://www.cleancss.com/sql-beautify/)

[MSDN Sub Query Fundamentals](https://msdn.microsoft.com/en-us/library/ms189575(v=sql.105).aspx)

[Stack Overflow- How do I combine multiple SQL Queries](https://stackoverflow.com/questions/4441590/how-do-i-combine-multiple-sql-queries)

[W3 Schools SQL Tutorial](https://www.w3schools.com/sql/default.asp)

[Using SQL to Define, Measure and Analyze User Sessions](https://segment.com/blog/using-sql-to-define-measure-and-analyze-user-sessions/)

[Python-Writing to Files](http://www.afterhoursprogramming.com/tutorial/Python/Writing-to-Files/)
