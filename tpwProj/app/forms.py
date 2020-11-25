from django import forms

from app.models import Item, Category
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core import validators


class Search(forms.Form):
    query = forms.CharField(label='Search', max_length=100)


SORT_CHOICES = (
    ("1", "New"),
    ("2", "Price Ascending"),
    ("3", "Price Descending"),
    ("4", "Best Sellers"),
    ("5", "Biggest Discount")
)

PRICE_CHOICES = (
    ("0-5", "€0 - €5"),
    ("5-10", "€5 - €10 "),
    ("10-20", "€10 - €20 "),
    ("20-30", "€20 - €30 "),
    ("30-40", "€30 - €40 "),
    ("40-50", "€40 - €50 "),
    ("50-100", "€50 - €100 "),
    ("100-200", "€100 - €200 "),
    ("200-300", "€200 - €300 "),
    ("300-400", "€300 - €400 "),
    ("400-50", "€400 - €500 "),
    ("500-750", "€500 - €750 "),
    ("750-1000", "€750 - €1000 "),
    ("1000-2000", "€1000 - €2000 "),
    ("2000-3000", "€2000 - €3000 "),
    ("3000-4000", "€3000 - €4000 "),
    ("4000-5000", "€4000 - €5000 "),
    ("5000-10000", "€5000 - €10000 "),
    ("10000+", "€10000+")
)


class CategoryFilter(forms.Form):
    order = forms.ChoiceField(choices=SORT_CHOICES,
                              label="Sort by:",
                              widget=forms.widgets.Select())

    price = forms.MultipleChoiceField(choices=PRICE_CHOICES,
                                      required=False,
                                      label="Price",
                                      widget=forms.widgets.CheckboxSelectMultiple())

    brand = forms.ChoiceField(choices=(),
                              widget=forms.widgets.RadioSelect(),
                              label="Brand",
                              required=False)

    availability = forms.ChoiceField(choices=((1, "Available"), (0, "Not Available")),
                                     widget=forms.widgets.RadioSelect(),
                                     label="Availability",
                                     required=False)

    discounted = forms.ChoiceField(choices=((1, "Discounted"), (0, "Not discounted")),
                                   widget=forms.widgets.RadioSelect(),
                                   label="Discounted",
                                   required=False)

    reviews = forms.MultipleChoiceField(
        choices=((1, "1 star"), (2, "2 stars"), (3, "3 stars"), (4, "4 stars"), (5, "5 stars")),
        widget=forms.widgets.CheckboxSelectMultiple(),
        label="Reviews",
        required=False)


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['brand'].choices = [(i['brand'], i['brand']) for i in Item.objects.all().values('brand').distinct()]


class SignUpForm(UserCreationForm):
    birthdate = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    first_name = forms.CharField(max_length=100, help_text='Last Name')
    last_name = forms.CharField(max_length=100, help_text='Last Name')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email',
                  'birthdate', 'password1', 'password2',)


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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].choices = [(c.name, [(sc.id, sc.name) for sc in Category.objects.all()
                                                     if sc.parent is not None and sc.parent.name == c.name])
                                           for c in Category.objects.all() if c.parent is None]


class CategoryForm(forms.Form):
    category = forms.CharField()


class SubcategoryForm(forms.Form):
    parent = forms.ChoiceField(choices=(),
                               widget=forms.widgets.Select(),
                               label="Category",
                               required=False)
    subcategory = forms.CharField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['parent'].choices = [(c.id, c.name) for c in Category.objects.all() if c.parent is None]


class CommentForm(forms.Form):
    item = forms.ChoiceField(choices=[(i.name, i.name) for i in Item.objects.all()], required=False)
    stars = forms.IntegerField(label="Rating",
                               validators=[validators.MinValueValidator(0), validators.MaxValueValidator(5)])
    comment = forms.CharField(label="Comment", max_length=1000)


class DeleteAccount(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(),
                               label="Confirm your password:")

    class Meta:
        model = User


class AddQuantityForm(forms.Form):
    quantity = forms.IntegerField(label="Quantity", validators=[validators.MinValueValidator(0)])
