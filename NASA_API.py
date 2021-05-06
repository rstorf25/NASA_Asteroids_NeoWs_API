from asteroids import nasa_asteroids
import requests

date = "1992-08-15"
output = r"D:\PycharmProjects\NASA_API\Example_Use.xlsx"

NASA_data = nasa_asteroids(date,output)
