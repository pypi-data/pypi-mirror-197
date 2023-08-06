import requests
import csv

# Set up the API request
api_url = 'https://api.stackexchange.com/2.3/questions'
params = {
    'site': 'stackoverflow',
    'tagged': 'python',
    'filter': 'withbody'
}
response = requests.get(api_url, params=params)
print(response.status_code) # should print 200 if the request is successful

questions = response.json()

print(f"API returned {len(questions['items'])} questions")
# Create a list to store the input and label values
data = []

# Loop through all the questions and answers and extract the content
for question in questions['items']:
    print(f"Processing question '{question['title']}'")
    if 'answers' in question:
        # Get the accepted answer if it exists
        accepted_answer = next((a for a in question['answers'] if a['is_accepted']), None)
        if accepted_answer:
            # Use the accepted answer if it exists
            input_value = question['title']
            label_value = accepted_answer['body']
            if input_value and label_value:
                data.append((input_value, label_value))
            else:
                print(f"Skipped question {question['question_id']} because input_value or label_value is empty.")
        else:
            print(f"Skipped question {question['question_id']} because it doesn't have an accepted answer.")
    else:
        print(f"Skipped question {question['question_id']} because it doesn't have any answers.")

# Write the data to a CSV file
with open('stackoverflow_python.csv', mode='w', newline='', encoding='utf-8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['input', 'label'])
    writer.writerows(data)
    print("Data written successfully to CSV file")
# Print the number of questions added to the CSV file
print(f"Added {len(data)} questions to the CSV file.")
