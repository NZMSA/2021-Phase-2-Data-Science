# Gathering data with REST API
Hi! This is a quick guide to gathering data with REST API on PowerBI. Here's a [really good blog post about it](https://blog.crossjoin.co.uk/2016/08/16/using-the-relativepath-and-query-options-with-web-contents-in-power-query-and-power-bi-m-code/) for more info.

<br>

## Importing data

We need to import our data. We're going to be using [Alpha Vantage](https://www.alphavantage.co/) for this example. 
<br>
We're going to need an API key so you'll need to get your free API key first. We're going to be using the TIME SERIES MONTHLY function.

![](https://i.imgur.com/vXD9Tpu.png)

You'll need this URL for the rest of the tutorial:
```
https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo
```

<br>
Now go on to PowerBI. First go select "Get data" on your PowerBI home screen and select the "Web" option.

![](https://i.imgur.com/nS7gptG.png)
<img src="https://i.imgur.com/40VtbQ3.png" width = "500"/>

<br> Paste the URL above into the text box
![](https://i.imgur.com/AAuAi7i.png)

<br>This might be what you see when it's done loading. You'll need to click back to "Converted to Table" to reverse some steps that PowerBI had done in advance if you see something like this.
![](https://i.imgur.com/a6ASoJn.png)

<br>If your screen looks like this, then you're all good to go. Select "Monthly Time Series" then select "Convert to Table"
<img src="https://i.imgur.com/4vjxifh.png" width ="800"/>

<br>You'll get something that looks like this. You'll want to expand the "Value" column to be able to see the actual values of the data.
![](https://i.imgur.com/pQnBMww.png)
<img src="https://i.imgur.com/B1lwygN.png" width = "400" />

## Power Query Editor

<br>Now we're going to want to go to the Advanced Editor.
The Advanced Editor lets you see the code that Power Query Editor is creating with each step. It also lets you create your own shaping code.

![](https://i.imgur.com/YkULvDa.png)

<br>This is what is currently in the Power Query Editor, but we'll need to change it up a bit.
![](https://i.imgur.com/b8QVvLT.png)

<br>We're going to be replacing it with this code:
```
let Source = (symbol) =>
    let
        Source = Json.Document(Web.Contents(
            "https://www.alphavantage.co/",
            [
            RelativePath="query",
            Query = [
                function="TIME_SERIES_MONTHLY",
                symbol=symbol,
                apikey = APIKey
            ]]

            ///"https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey=demo"
        )),
        
        #"Monthly Time Series" = Source[Monthly Time Series],
        #"Converted to Table" = Record.ToTable(#"Monthly Time Series"),
        #"Expanded Value" = Table.ExpandRecordColumn(#"Converted to Table", "Value", {"1. open", "2. high", "3. low", "4. close", "5. volume"}, {"1. open", "2. high", "3. low", "4. close", "5. volume"})
    in
        #"Expanded Value"
in Source
```

<br>The Web.Contents() function in is the key to getting data from web pages and web services.
RelativePath adds some extra text to the base url given in the first parameter for the function, 
while Query allows you to add query parameters to the url, and is itself a record.

<br>Another thing we're doing is making it a function of symbol, rather than statically "IBM" as in the original URL. This means
we can input different symbols (e.g MSFT) to look at their stocks as well, and it will call on the TIME SERIES MONTHLY function based on that symbol.

![](https://i.imgur.com/y9nNWHc.png)

## Creating parameters

<br>As you noticed, the API Key was not included. Instead it was stored as a parameter. You should have gotten your API key in the beginning, so
now we'll be storing it as a parameter.

<br>First, right click along the side of your dashboard where your queries are, and click New Parameter. Fill up the information accordingly. 
It should then be stored as a parameter called APIKey, which is what is referenced in the Power Query Editor.

![](https://i.imgur.com/S4MPfJ7.png)

<img src= "https://i.imgur.com/QLshfUA.png" width = "700" />

## Entering Data
<br>Next, we're going to enter data by clicking "Enter Data" on the Ribbon. For this example we're going to name the column "Stock" and enter IBM and MSFT as our symbols. This means we'll
be gathering IBM and MSFT stock data.
<img src="https://i.imgur.com/hdXSVys.png" width="700" />

<br>Now that we have our table, we're going to apply the function that we created previously on our data. 
<br>Side note: In the screenshot below, I named my function "Stock" but then renamed it in a subsequent step to "Function1" !!
<br>Click on "Add Column" on the top ribbon and select "Invoke Custom Function"
![](https://i.imgur.com/wAzfZjv.png)

<br>(Here my function has been renamed Function1. This is the same function we created earlier. Select your function in the dropdown box and everything else should fill up automatically.
![](https://i.imgur.com/sWuHT1X.png)

<br>You should then have a table that looks like this. We can expand it by clicking the upper corner of the column.
![](https://i.imgur.com/qSYEbkw.png)

<br>This will show all of the data in our columns. Now we're going to modify it a bit using the formula bar. Let's rename the columns to make the data cleaner!
We're just changing "Name" to "Date" and edited the numbers out of the column names.
![](https://i.imgur.com/p4OlSP8.png)

## Tidying data
<br>We also need to convert some of the data types that aren't much use to us. For example, our Date column is not formatted in a Date format yet. Right click the column and
select "Change Type" > "Date"

<img src = "https://i.imgur.com/EJ1FDfX.png" width = "600" />

<br>Next, we're going to select "Stock" and "Date", right click, and select "Unpivot Other Columns"
<img src="https://i.imgur.com/nmuMOVM.png" width = "600" />

<br>Now we have our data in "long" format! Now let's just change the type of the Values column to Decimal.
<img src="https://i.imgur.com/tVm5CMR.png" width = "600" />

<br>Click close and apply, and our data should be all good to go for visualization!

## Data Visualization

<br>Depending on the kind of data and kind of analysis your executing, there are different charts that serve different purposes! [Check it out here](https://docs.microsoft.com/en-us/power-bi/consumer/end-user-visual-type).
<br> Since we're analyzing stock data today, we'll be using a line graph to illustrate the time series data.
<br>So first, select "Line Chart" under "Visualizations"
![](https://i.imgur.com/QgBVYkB.png)

<br>Drag "Date" to Axis and "Value" to Values. This means we'll be looking at the data points by date.
![](https://i.imgur.com/kCLvt2g.png)

<br>Then drag "Stock" and "Attribute" to the Filter panel. This will allow you to filter the data based on attributes.
<img src="https://i.imgur.com/kfBHu9y.png" width = "550" />

<br>"Drill Down" until you reach the lowest heirarchy of Date to see stocks by Year, Month, Quarter, and Day. This shows a wider range of data!
![](https://i.imgur.com/q69kr4u.png)

<br>You can play around the data and see the possible ways you could communicate this information. For example, this is Microsoft's closing value of stock
from 2000 to 2020:
![](https://i.imgur.com/ZZQSChV.png)

### Some other tutorials
<br>
PowerBI REST API - https://www.youtube.com/watch?v=fXbJeIY2CgE&t=282s
<br>
Importing Data from REST APIs | Other Data Sources | Power BI - https://www.youtube.com/watch?v=hhjOHYIeHuY
