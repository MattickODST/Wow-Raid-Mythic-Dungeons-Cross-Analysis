# Wow-Raid-Mythic-Dungeons-Cross-Analysis
#    Hi! Welcome to my cross analysis of my World of Warcraft guild's raiders.
#
#    Some Background.
#        I am the guild leader and raid leader of a World of Warcraft guild of about 300 players.  Twice a week we have a raid that includes about 20 or so players. Some of these players also do dungeons outside of our normal raid times. I want to compare the performance of those raiders and see how much improvement they're gaining in raid by also doing dungeons.

# This project will combine multiple week over week raid logs and compare them with an overview of the players numbers of dungeons done.

# This project will have the following features: 
# It will merge multiple log files.
# It will extrapolate the necessary data to perform the analysis.
# It will compare the data sets.
# It will clean the data to make it usable.
# It will present the data in 3 different visualizations and create a usable .csv file.
#   The 3 graphs are as follows:
#       #1 The total number of Dungeons completed.
#       #2 Each players performance in each of the raids completed
#       #3 A rating of their raid performance VS number of dungeons completed.
# To note: Ilvl % is a measure of performance based on total dps done compared to everyone withn the same gear level as that player.


# To Use: 
# Clone the repository
# Start a virtual environment and install requirements:
#   Terminal commands:
#       python3 -m venv venv
#       source venv/Scripts/activate
#       pip install -r requirements.txt
# Run the WowMythicToRaidComparison.py file