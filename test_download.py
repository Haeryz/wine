import requests

# Test batch prediction with download
files = {'file': open('test_batch.csv', 'rb')}
response = requests.post('http://localhost:8000/batch-predict?download=true', files=files)

print('Content-Type:', response.headers.get('Content-Type'))

# Save the CSV file
with open('predictions_result.csv', 'wb') as f:
    f.write(response.content)
    
print('Downloaded to predictions_result.csv')

# Read the csv content
with open('predictions_result.csv', 'r') as f:
    print('\nFirst few lines of the CSV:')
    for i, line in enumerate(f):
        print(line.strip())
        if i >= 5:
            break
