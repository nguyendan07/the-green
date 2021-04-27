# The Green
The Green is Online Fruit and Vegetables Shop Project. The main objective of the Online Fruit and Vegetable shop is to create an online e-commerce platform for customers to buy fruit and vegs.  

## Get it up and running
**Install pipenv and create virtual environments**
```
pip install -U pip pipenv
pipenv install
```


**Running project**
```
./manage.py migrate
./manage.py loaddata dev_data.json
./manage.py runserver
```
*Open in your browser, visit http://127.0.0.1:8000 and login to /admin with admin/123456a@*

**Database dump**

```
python manage.py dumpdata --natural-primary --natural-foreign > dev_data.json
```
