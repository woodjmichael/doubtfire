# Doubtfire

<img src="https://m.media-amazon.com/images/M/MV5BMTExNzU0MTM0OTBeQTJeQWpwZ15BbWU4MDUyOTQwODEx._V1_.jpg" alt="RIP" style="zoom: 20%;" />

# What it does
 - Checks up on your regular data harvesting tasks
 - Send an email if something is out of date for more than 24 hours
 - All times in UTC


# Usage
## Email API
- Sign up for the SendGrid email API
- Get your key and put in as an OS environment variable (eg especially don't save your key anywhere public like GitHub)
- May need to edit code to include your "from" email address
## East stuff
- Point MS Task Scheduler (or other to the `.bat` file)
  - I've learned to also specify the run-in directory with no quotations
  - But put quotations around the path to the .bat file
- Add new directories and files in `.cfg`
  - Actually, need to add some code before this works for new dirs
- Make sure the files are `.csv` and that the most recent rows are on the bottom with a date time index on the left

