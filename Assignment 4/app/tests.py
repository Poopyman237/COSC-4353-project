from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory
from django.urls import reverse, resolve
from django.utils import timezone

from .forms import ProfileForm, FuelQuoteForm
from .models import Profile, FuelQuote, State
from .views import home, register, login_view, profile, profile_edit, fuel_history, fuel_quote


# Test for the home page
class HomeTests(TestCase):
    # this test the status code
    def test_home_view_status_code(self):
        url = reverse('app:home')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    # this test the view function called by the home url
    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)


# this logout test
class LogoutTest(TestCase):
    def setUp(self):
        self.url = reverse('app:logout')
        self.home_url = reverse('app:home')
        self.login_url = reverse('app:login')

    def test_logged_out(self):
        data = {
            'username': 'john',
            'password': 'abcdef123456',
        }
        # user is first created with the above data
        User.objects.create_user(**data)
        # user is logged in
        self.client.login(**data)
        response = self.client.get(self.url)
        # we assert that there is a redirect after logout just as the view is designed
        self.assertRedirects(response, self.home_url)


class LoginTest(TestCase):
    def setUp(self):
        url = reverse('app:login')
        self.response = self.client.get(url)
        self.home_url = reverse('app:home')

    # this test the status code of the get request to the login view
    def test_login_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    # this test the view function called by the login url
    def test_login_url_resolves_login_view(self):
        view = resolve('/login/')
        self.assertEquals(view.func, login_view)

    # this test that there is an instance of AuthenticationForm form in the view context
    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, AuthenticationForm)


class SuccessfulLoginTest(TestCase):
    def setUp(self):
        url = reverse('app:login')
        self.factory = RequestFactory()

        self.data = {
            'username': 'john',
            'password': 'abcdef123456',
        }
        self.user = User.objects.create_user(**self.data)
        self.response = self.client.post(url, self.data)
        self.home_url = reverse('app:home')

    def test_redirection(self):
        # A valid form submission should redirect the user to the home page
        self.assertRedirects(self.response, reverse('app:edit_profile'))

    # test the status code of the redirect
    def test_post_success(self):
        self.assertEquals(self.response.status_code, 302)

    def test_user_authentication(self):
        result = authenticate(**self.data)
        self.assertTrue(result is not None)


class RegisterTests(TestCase):
    def setUp(self):
        url = reverse('app:register')
        self.response = self.client.get(url)

    def test_register_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_register_url_resolves_register_view(self):
        view = resolve('/register/')
        self.assertEquals(view.func, register)

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)


class SuccessfulRegistrationTest(TestCase):
    def setUp(self):
        url = reverse('app:register')
        data = {
            'username': 'james',
            'password1': '12121212@',
            'password2': '12121212@',
        }
        self.response = self.client.post(url, data)
        self.home_url = reverse('app:home')
        self.login_url = reverse('app:login')

    def test_redirection(self):
        # A valid form submission should redirect the user to the login page
        self.assertRedirects(self.response, self.login_url)


class InvalidRegistrationTests(TestCase):
    def setUp(self):
        url = reverse('app:register')
        self.response = self.client.post(url, {})

    def test_register_status_code(self):
        # testing an invalid form submission, which should return to the same page
        self.assertEquals(self.response.status_code, 200)

    # testing that error details is return in the form when error occurs
    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    # test user is not created when there is an error
    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())


class ProfileTest(TestCase):
    def setUp(self):
        self.username = 'james'
        self.password = '12121212@'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.state = State.objects.create(name='Texas', abbr='TX')

    # testing that user object is mapped to one profile object
    def test_unique_user_profile(self):
        profile_qs = Profile.objects.filter(user=self.user)
        self.assertTrue(profile_qs.count() == 1)

    # testing the object return string
    def test_profile_return_string(self):
        self.assertEquals(self.user.profile.__str__(), self.username)
        self.assertEquals(self.state.__str__(), self.state.name)


class UpdateProfileTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('app:edit_profile')
        self.username = 'james'
        self.password = '12121212@'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_date = timezone.now().date()
        self.state = State.objects.create(name='Texas', abbr='TX')

        self.data = {
            'user': self.user,
            'address_1': 'Test address',
            'city': 'New York',
            'state': self.state.id,
            'zipcode': 2673648,
            'full_Name': 'John Doe'
        }

    def test_edit_profile_status_code(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = profile_edit(request)

        self.assertEquals(response.status_code, 200)

    def test_redirect(self):
        request = self.factory.post(self.url, self.data)
        request.user = self.user
        response = profile_edit(request)

        self.assertEquals(response.status_code, 302)

    def test_valid_profile_data(self):
        # url = reverse('new_topic', kwargs={'pk': 1})

        form = ProfileForm(data=self.data)
        self.assertTrue(form.is_valid())


class FuelQuoteTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.url = reverse('app:fuel_quote')
        self.username = 'james'
        self.password = '12121212@'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.test_date = timezone.now().date()

        self.data = {
            'user': self.user.id,
            'gallons_requested': 10,
            'delivery_date': self.test_date,
            'delivery_address': 'Test address',
            'rate': 2
        }

    def create_quote(self):
        return FuelQuote.objects.create(
            user=self.user,
            gallons_requested=10,
            delivery_date=self.test_date,
            delivery_address='Test address',
            rate=2
        )

    def test_quote_obj_return_string(self):
        q = self.create_quote()
        self.assertEquals(q.__str__(), self.user.username)

    def test_quote_total(self):
        q = self.create_quote()
        self.assertEquals(q.get_total(), 20)

    def test_fuel_quote_status_code(self):
        request = self.factory.get(self.url)
        request.user = self.user
        response = fuel_quote(request)

        self.assertEquals(response.status_code, 200)

    def test_valid_profile_data(self):
        # url = reverse('new_topic', kwargs={'pk': 1})

        form = FuelQuoteForm(data=self.data)
        self.assertTrue(form.is_valid())

    def test_redirect(self):
        response = self.client.post(self.url, self.data)

        self.assertEquals(response.status_code, 302)


class FuelHistoryTest(TestCase):
    def setUp(self):
        url = reverse('app:fuel_history')
        self.response = self.client.post(url, {})

    def test_fuel_history_status_code(self):
        # testing a get request to fuel_history view
        self.assertEquals(self.response.status_code, 200)