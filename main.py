#!/usr/bin/env python3
from get_meal import get_meals
import json
from typing import Optional
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def web_root():
    return "Hello, world!"

@app.get("/weekly_meals")
def weekly_meal():
    return get_meals()

@app.get("/daily_meal")
def daily_meal(date_str: Optional[str] = None):
    if date_str:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            return {
                'result': 'error',
                'reason': 'date_str is invalid. date_str should in YYYY-MM-DD'
            }
    else:
        date = datetime.today().date()
    
    meals = get_meals()
    for meal in meals:
        if meal['date'] == date:
            return {
                'result': 'succeed',
                'body': meal
            }
    
    return {
        'result': 'error',
        'reason': 'meals on date not found'
    }
    
    

def main():
    meals = get_meals()
    # print(meals[0])
    pretty = json.dumps(meals, ensure_ascii=False, indent=2, default=str)
    print(pretty)


if __name__ == "__main__":
    main()