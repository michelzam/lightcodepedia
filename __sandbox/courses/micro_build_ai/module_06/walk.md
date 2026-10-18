# 🌦 Walk now, or later?

The dogs go out when it is dry and not too hot. The sky says when.

```csv
campus,neighborhood,lat,lng
Milwaukee,Brewers Hill,43.0530,-87.9720
Ozaukee,Saukville,43.3839,-87.9403
Racine,Lathrop Ave,42.7261,-87.7828
```
{: .dataset #shelters }

[the shelters](#)
{: .datagrid source="shelters" #campus_grid height="150" }

[where they are](#)
{: .map source="shelters" bind="campus_grid" bindicon="🐕" tiles="liberty" height="220" }

[the sky over the shelter you pick](https://api.open-meteo.com/v1/forecast?latitude={campus_grid.row.lat}&longitude={campus_grid.row.lng}&hourly=temperature_2m,precipitation_probability,weather_code&forecast_hours=8&timezone=auto)
{: .dataset #sky path="hourly" }

```csv
icon,weather,low,high
☀️,clear,0,1
☁️,cloudy,2,50
🌦,drizzle,51,60
🌧,rain,61,70
🌨,snow,71,79
⛈,showers or storm,80,99
```
{: .dataset #skies }

```sql
SELECT k.icon, k.weather, s.time, s.temperature_2m,
       ROUND(s.temperature_2m * 9 / 5 + 32, 0) AS fahrenheit,
       s.precipitation_probability
FROM sky s LEFT JOIN skies k ON s.weather_code BETWEEN k.low AND k.high
ORDER BY s.time
```
{: .query bind="sky,skies" #forecast }

Now over **{= campus_grid.row.campus }**: {= forecast.first.icon } {= forecast.first.temperature_2m } °C · {= forecast.first.fahrenheit } °F

[the next eight hours](#)
{: .datagrid source="forecast" #hours hints="icon: the sky, from the service's weather code | weather: the same, in a word | time: the hour, the shelter's own time | temperature_2m: °C, measured 2 m above the ground | fahrenheit: the same hour in °F | precipitation_probability: the chance of rain, in %" }

[the sky, hour by hour: °C and the chance of rain](#)
{: .chart source="sky" type="line" x="time" y="temperature_2m" bars="precipitation_probability" }

### 📝 TODO

- [ ] a query that keeps the good hours
- [ ] a sentence that says when to go