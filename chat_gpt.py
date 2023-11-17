from dotenv import load_dotenv
import requests
import openai
import os

load_dotenv()

openai.api_key = os.environ.get("AI_API_KEY")
openai.organization = os.environ.get("AI_ORG")
gpt_3_url = "https://api.openai.com/v1/chat/completions"

class chatGPT():

  def image_generation(self, title, ingredients):
    prompt = f"{title}. {ingredients}"
    response = openai.Image.create(
      prompt = prompt,
      n = 2,
      size = "512x512"
    )
    urls = []
    urls.append(response.data[0].url)
    urls.append(response.data[1].url)
    return urls
  
  def child_image(self, prompt):
    response = openai.Image.create(
      prompt = prompt,
      n = 2,
      size = "512x512"
    )
    urls = []
    urls.append(response.data[0].url)
    urls.append(response.data[1].url)
    return urls
    

  def recipe_generation(self, include, exclude):
    prompt = f"Write a recipe with a descriptive name that includes {include} and any other needed ingredients but does not contain {exclude}. Output the Title, Description, Ingredients, and Instructions. Format the output using html tags, tagging the title with the <h2> tag." 
    response = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "user", "content": prompt}
      ]
    )
    recipe = response.choices[0].message.content
    return recipe
    
