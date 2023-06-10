from transformers import pipeline

# Create a text generation pipeline
text_generator = pipeline('text-generation', model='gpt2')

# Generate text
input_text = "가게명 추천해줘"
generated_text = text_generator(input_text)

# Print the generated text
print(generated_text)