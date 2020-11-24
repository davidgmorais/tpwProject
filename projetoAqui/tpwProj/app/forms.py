from django import forms
from app.models import Item, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators
from django.forms import widgets

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


# cat_choices = Category.objects.filter(parent__isNull=True).values_list('name')
# class CategoryFilters(forms.Form):


class ItemForm(forms.Form):
    name = forms.CharField(label="Name", max_length=50)
    description = forms.CharField(label="Description", max_length=500)
    specification = forms.CharField(label="Specifications", max_length=10000)
    price = forms.FloatField(label="Price", validators=[validators.MinValueValidator(0)])
    brand = forms.CharField(max_length=30)
    quantity = forms.IntegerField(validators=[validators.MinValueValidator(0)])
    cat = Category.objects.all()
    category = forms.ChoiceField(choices=[(c.name, [(sc.id, sc.name) for sc in Category.objects.all()
                                                            if sc.parent is not None and sc.parent.name == c.name])
                                          for c in Category.objects.all() if c.parent is None])
    discount = forms.IntegerField(label="Discount",
                                  validators=[validators.MinValueValidator(0), validators.MaxValueValidator(100)])
    picture = forms.ImageField(label="Picture")
    sellMoney = forms.FloatField(label="Money for users")


class CategoryForm(forms.Form):
    category = forms.CharField()


class SubcategoryForm(forms.Form):
    subcategory = forms.CharField()

