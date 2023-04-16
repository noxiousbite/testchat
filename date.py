import openai_secret_manager
from notion_client import Client
from random import choices

# Retrieve secrets
secrets = openai_secret_manager.get_secret("notion")

# Initialize Notion client
notion = Client(auth=secrets["secret_CHdDdchMswpXWV8vrjSHZkC7aDRYAR0xZWHof8fJ6Ay"])

# Retrieve the girl's activity and food choices from her database
girl_database_id = secrets["0ca392e2b54b4dad997cc01cc32af946?v"]

girl_database = notion.databases.retrieve(database_id=girl_database_id)
girl_results = notion.databases.query(
    **{
        "database_id": girl_database_id,
        "sorts": [{"property": "Rating", "direction": "descending"}],
    }
).get("results")

# Convert the girl's activity and food results to a list of tuples
girl_activity_choices = [(activity["properties"]["Name"]["title"][0]["text"]["content"], activity["properties"]["Rating"]["number"]) for activity in girl_results if activity["properties"]["Type"]["select"]["name"] == "Activity"]
girl_food_choices = [(food["properties"]["Name"]["title"][0]["text"]["content"], food["properties"]["Rating"]["number"]) for food in girl_results if food["properties"]["Type"]["select"]["name"] == "Food"]

# Retrieve the boy's activity and food choices from his database
boy_database_id = secrets["6024a1e6510646b2bc0521ca4ca7eda9?v"]

boy_database = notion.databases.retrieve(database_id=boy_database_id)
boy_results = notion.databases.query(
    **{
        "database_id": boy_database_id,
        "sorts": [{"property": "Rating", "direction": "descending"}],
    }
).get("results")

# Convert the boy's activity and food results to a list of tuples
boy_activity_choices = [(activity["properties"]["Name"]["title"][0]["text"]["content"], activity["properties"]["Rating"]["number"]) for activity in boy_results if activity["properties"]["Type"]["select"]["name"] == "Activity"]
boy_food_choices = [(food["properties"]["Name"]["title"][0]["text"]["content"], food["properties"]["Rating"]["number"]) for food in boy_results if food["properties"]["Type"]["select"]["name"] == "Food"]

# Merge the girl's and boy's activity and food choices
activity_choices = girl_activity_choices + boy_activity_choices
food_choices = girl_food_choices + boy_food_choices

# Select a random activity and food based on the specified weights
num_activities = 1  # Replace with desired number of activities
num_foods = 1  # Replace with desired number of foods

activity_weights = [activity[1] for activity in activity_choices]
activity_selected = choices(activity_choices, weights=activity_weights, k=num_activities)

food_weights = [food[1] for food in food_choices]
food_selected = choices(food_choices, weights=food_weights, k=num_foods)

# Print the selected activity and food
print(f"Selected activity: {activity_selected[0][0]}")
print(f"Selected food: {food_selected[0][0]}")
