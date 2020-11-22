from django import forms
from app.models import Item, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class Search(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


class CategoryFilter(forms.Form):
    CategorySelection = forms.ModelChoiceField(queryset=Category.objects.all().values_list('name', flat=True))


class SignUpForm(UserCreationForm):
    birthdate = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birthdate', 'password1', 'password2',)


SORT_CHOICES = (
    ("1", "Price Ascending"),
    ("2", "Price Descending"),
    ("3", "Best Sellers"),
    ("4", "Biggest Discount"),
    ("5", "New")
)

brand_choices = Item.objects.all().values_list('brand')
brand_choice_list = []
for brand in brand_choices:
    brand_choice_list.append(brand)

# category_choices = Category.objects.all().values_list


class Filters(forms.Form):
    sort = forms.ChoiceField(choices=SORT_CHOICES),
   # brand = forms.ChoiceField(choices=brand_choice_list)

#
# cat_choices = Category.objects.filter(parent__isNull=True).values_list('name')
# class CategoryFilters(forms.Form):
