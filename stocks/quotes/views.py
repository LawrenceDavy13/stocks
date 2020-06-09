from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages

def home(request):
    import requests
    import json

    # If someone has filled out the form, they have POSTed
    if request.method == 'POST':
        ticker = request.POST['ticker'] # Store data entered in form using ticker variable

        # Retrive and save the api stocks data to variable
        # Use ticker to retrieve the corresponding comapny stock data ie. ticker=appl=apple
        api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ ticker +"/quote?token=pk_21d2bc7c11234558a6e3cb03e2abc7a7")   

        # If there is JSON data avaiable, convert it into a python object/dictonary 
        try:
            api = json.loads(api_request.content)
        
        # If there is not data avaiable, just say there was an error
        except Exception as e:
            api = "Error..."
        return render(request, 'home.html', {'api' : api})


    # If no one filled out the form
    else:
        return render(request, 'home.html', {'ticker' : "Enter company name to get stock quote"})



# About page
def about(request):
    return render(request, 'about.html', {})




# Add stock page
def add_stock(request):
    import requests
    import json


    # If someone has filled out the form, they have POSTed
    if request.method == 'POST':
        form = StockForm(request.POST or None)

        # Has the correct information been added
        if form.is_valid():
            # If so, save the info
            form.save()
            # Write message saying stock has been added successly
            messages.success(request, ("Stock has been added"))
            return redirect('add_stock')

    else:
        # Get all stock info that was added to the database
        ticker = Stock.objects.all()

        # Save data to output list
        output = []

        # Loop through every ticker item and amke an api call
        for ticker_item in ticker:


            api_request = requests.get("https://cloud.iexapis.com/stable/stock/"+ str(ticker_item) +"/quote?token=pk_21d2bc7c11234558a6e3cb03e2abc7a7")   

            # If there is JSON data avaiable, convert it into a python object/dictonary 
            try:
                api = json.loads(api_request.content)
                output.append(api)
            # If there is not data avaiable, just say there was an error
            except Exception as e:
                api = "Error..."




        return render(request, 'add_stock.html', {'ticker': ticker, 'output': output})




# Delete stock button
def delete(request, stock_id):
    item = Stock.objects.get(pk=stock_id) # 
    item.delete()
    messages.success(request, ("Stock has been deleted"))
    return redirect(delete_stock)


# Delete stock page
def delete_stock(request):

    # Get all stock info that was added to the database
    ticker = Stock.objects.all()
    return render(request, 'delete_stock.html', {'ticker': ticker })
        