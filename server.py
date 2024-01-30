import requests
import json
import os
from fastapi import FastAPI, HTTPException

app = FastAPI()

def get_bmi(weight, height):
    height = height / 100
    return weight / (height ** 2)

def get_response():
    
    key=os.environ.get('GEMINI_API_KEY')
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key="+key

    headers = {
    'Content-Type': 'application/json',
}

    data = {
    "contents": [
        {
            "parts": [
                {
                    #TO DO: ADD PROMPT and GET response
                    "text": "tell me formula of gravity"
                }
            ]
        }
    ]
}

    response = requests.post(url, headers=headers, data=json.dumps(data))
    data=response.json()
    print(data)
    data=data['candidates'][0]['content']['parts'][0]['text']
    return data

@app.post("/get_recipe")
async def get_recipe(data: dict):
    try:
        ingredients = data["ingredients"]
       
        current_weight = data["current_weight"]
        current_height = data["current_height"]  #height is in centimeter
        
        #response = get_response()
        #return response
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"Missing required field: {e}")
    
    return ingredients, current_weight, current_height, {"bmi":round(get_bmi(current_weight, current_height), 2)}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=5555)


