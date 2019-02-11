import requests
from pymongo import MongoClient
import pytest
import run


def test_status_code():
    app = run.create_app()
    clint = app.test_client()
    res = clint.get('api/properties')
    assert res.status_code == 200


def test_page_items():
    app = run.create_app()
    clint = app.test_client()
    res = clint.get('api/properties?page=1')
    data = res.get_json()
    assert len(data['result']) == 48


def test_page_items_with_ratio():
    app = run.create_app()
    clint = app.test_client()
    res = clint.get('api/properties?page=1&feed_ratio=[{%22feed%22:%2011,%22ratio%22:%2024},{%22feed%22:%2012,%22ratio%22:%2012},{%22feed%22:%2016,%22ratio%22:%2012}]')
    data = res.get_json()
    len_11 = 0
    len_12 = 0
    len_16 = 0
    for i in data['result']:
        for key, value in i.items():
            if key == 'Feed':
                if value == '11':
                    len_11 += 1
        
                elif value == '12':
                    len_12 += 1
        
                else:
                    len_16 += 1

    assert len(data['result']) == 48 and len_11 == 24 and len_12 == 12 and len_16 == 12


def test_empty_page():
    app = run.create_app()
    clint = app.test_client()
    res = clint.get('api/properties?page=6')
    data = res.get_json()
    assert len(data['result']) == 0


def test_collection_items():
    conn = MongoClient()
    db = conn.mypropertydb
    data_table = db.properties
    items = 0
    for item in  data_table.find():
        items+=1

    app = run.create_app()
    clint = app.test_client()
    res = clint.get('api/properties')
    data = res.get_json()

    assert items == len(data['result'])





