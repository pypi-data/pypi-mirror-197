from cohere_sagemaker import Client

client = Client(endpoint_name='my-cohere-endpoint')

# generate prediction for a prompt
response = client.generate(
    prompt="Tell me a story about",
    max_tokens=20)

print(response.generations[0].text)
