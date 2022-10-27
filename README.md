# Doubtfire

<img src="https://m.media-amazon.com/images/M/MV5BMTExNzU0MTM0OTBeQTJeQWpwZ15BbWU4MDUyOTQwODEx._V1_.jpg" alt="RIP" style="zoom: 20%;" />

# What it does
 - Checks up on your regular data harvesting tasks
 - Send an email if something is out of date for more than 24 hours
 - All times in UTC


# Usage
- Point MS Task Scheduler (or other to the `.bat` file)
- Add new directories and files in `.cfg`
  - Actually, need to add some code before this works for new dirs
- Make sure the files are `.csv` and that the most recent rows are on the bottom with a date time index on the left

