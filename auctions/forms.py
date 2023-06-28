from django import forms
from .models import *

class NewListingForm(forms.Form):
    listing_name = forms.CharField(label = "", required=True, widget=forms.TextInput(attrs={'placeholder': 'Listing Name', 'class':'col-5', 'style':'margin-bottom:9px;'}))
    starting_bid = forms.DecimalField(label = "", required=True, widget=forms.NumberInput(attrs={'placeholder': 'Starting Bid Price', 'style':'margin-bottom:9px;','class':'col-2'}))
    buy_now = forms.DecimalField(label = "", required=False, widget=forms.NumberInput(attrs={'placeholder': 'Buy Now Price', 'style':'margin-bottom:9px;','class':'col-2'}))
    listing_description = forms.CharField(label = "", required= False,
                                widget=forms.Textarea(
                                    attrs={'placeholder': 'Enter listing description', 'class':'col-11'}
                                ))
    listing_image = forms.ImageField(label="", required=False)


class BidForm(forms.Form):
    value = forms.DecimalField(label="")

class CommentForm(forms.Form):
    comment = forms.CharField(label="", required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Comment', 'class':'col-7'}))
                                



    
    
