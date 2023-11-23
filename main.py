#!/usr/bin/env python3
from get_meal import BUFSMeals
import json
from typing import Optional
from datetime import datetime
from fastapi import FastAPI

app = FastAPI()
meals = BUFSMeals()

@app.get("/")
def web_root():
    return "Hello, world!"

@app.get("/meals/weekly")
def weekly_meal():
    return meals.get_weekly()

@app.get("/meals/daily")
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
    
    meal = meals.get_daily(date)
    if meal:
        return {
            'result': 'succeed',
            'body': meal
        }
    else:
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