# Contributors:
    - Jake Becker
    - Evan Ciancio
    - Phillip Mathew
    - Justin Liss
    - Sri Garlapati
    - Brendan Hart

# Trust the Process:

### Run the generate_dates.py
	- Job: Loads any new dates into the new_dates table from the range that was specified
	- Configure startYearP, startMonthP, startDayP or endYearP, endMonthP, or endDayP to coorespond to the dates from which you want to pull new dates (set startYearP, startMonthP, startDayP, endYearP, endMonthP, and endDayP to the same date if you just want to pull in one date)
	- Could probably just run this once and generate all the dates for a basketball season
	- Note: only run if date is not in table!

### Run the playerRefScraper.py
	- Job: Loads any new players into the player reference table that have played the night or season or whenever before
	- Configure startYearP, startMonthP, startDayP or endYearP, endMonthP, or endDayP to coorespond to the dates from which you want to pull new players from basketball reference (set startYearP, startMonthP, startDayP, endYearP, endMonthP, and endDayP to the same date if you just want to pull in one date)

### Run generateBoxScoreURLs.py
	- Job: Loads potential Box Score URLs into the database from the specified date range in constants.py so that the performance scraper can pull in all of data from the box score
	- Configure startYearP, startMonthP, startDayP or endYearP, endMonthP, or endDayP to coorespond to the dates from which you want to pull new potential box score URLS from basketball reference (set startYearP, startMonthP, startDayP, endYearP, endMonthP, and endDayP to the same date if you just want to pull in one date)

### Run performanceScraper.py
	- Job: Scrape the box score data and put it into player performance table
	- Configure startYearP, startMonthP, startDayP or endYearP, endMonthP, or endDayP to coorespond to the dates from which you want to pull the box scores URLS from the database to scrape the data (set startYearP, startMonthP, startDayP, endYearP, endMonthP, and endDayP to the same date if you just want to pull in one date)

### Run team_performance.py
	- Job: Scrape the box score data and put it into team performance table
	- Configure startYearP, startMonthP, startDayP or endYearP, endMonthP, or endDayP to coorespond to the dates from which you want to pull the box scores URLS from the database to scrape the data (set startYearP, startMonthP, startDayP, endYearP, endMonthP, and endDayP to the same date if you just want to pull in one date)

### Run the extrapolators!
	- Job: Extrapolate the data scraped from the performance tables to the average tables to get a player's average for a season on that day, a team's average for a season on that day, and a team's result vs a defense on that day
	- How:
		○ Run dailyPreformanceExtrapolation.py
			§ Specify the date id for which you want to extrapolate the data according to the first day for which you have not scraped data all the way till the day you are predicting in constants.py (specify date id)
		○ Run teamPerformanceExtrapolation.py
			§ Specify the date id for which you want to extrapolate the data according to the first day for which you have not scraped data all the way till the day you are predicting in constants.py (specify date id)
		○ Run teamVsDefenseExtrapolation.py
			§ Specify the date id for which you want to extrapolate the data according to the first day for which you have not scraped data all the way till the day you are predicting in constants.py (specify date id)

### Download new rotoguru file
	- Move into rotoguru20172018data.csv
	- Delimite by comma (,) and colon (:)
	- Filter only the days you need
		○ Note: only need to run when didn't pull FanDuel information from FanDuel competition

### If need to run rotoguru file, Run pos_sallary.py
	- Job: align the rotoguru player ID with the basketball reference id
	- Job: put the fanduel and draftkings position and salary into the performance table

### Run sumPoints.sql
    - Job: creates fanduel and draftkings pts based off performance

### Scrape FanDuel
    - Job: put current players playing in the performance table
    - Pull in the FanDuel file that you are scraping from the competition you are entering
    - Split the first column into two columns and delimit by the dash (-)
    - Save and specify the location of the file in constants.py
    - Run fanduelScraper.py

### Run projMinutues.sql
	- Job: projects the minutes for the people playing

### Run projMagic.py
	- Job: predict player performances using past data and ridge regression
    - Must specify YearP, MonthP, and DayP for the day you are predicting
    - Note the regression coefficents are stored in a file

### Run optimizer.py
    - Job: generate FanDuel lineups


## Regression Management
    - Goal: To efficently calculate the regregression coefficents on our training set so that variance and bias is balanced
    - How: Run magic.py once a month, and save the regression coefficents to coef.npz
        - Must train over entire data set (leaving out first two weeks of seasons and last week of seasons)
        - Currently evaluating different methods of cross validation....
    - File Data:
        - coef_DEC_2017: 189 Features, coefficents for Decemeber of 2017


