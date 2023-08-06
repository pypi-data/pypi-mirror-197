# Package of Measurement of Digital Economy



### Intro

> Based on the analysis of newspaper text and network dynamics, this index can extract the implied information in newspapers to replace traditional economic data to construct the measurement of digital economy. The advantage of this measure is that it includes both direct hard information and indirect soft factors. In addition, it can dynamically simulate influence indicators to provide suggestions for accurate decision-making of the government

### **function**

```db_out():
db_out
```

Get all the data about digital economy,you will get a DataFrame data.

```
db_year(data,city)
```

Output digital economy index for all regions by year,and you will alos get a DataFrame data.

```
db_city(data,city)
```

Output digital economy index for time by city,and you will alos get a DataFrame data.

```
tolist(data)
```

Transform data from DataFrame to a list