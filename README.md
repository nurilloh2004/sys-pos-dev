# Django POSOX server

### Run project in docker container

```
/cd src
docker compose up
```

### Authentication and Authorization

> POST: http://127.0.0.1:8585/api/auth/v1/login/

#### Request body (raw json)
```json
{
    "username": "admin",
    "phone": "+998901234500",
    "password": "123"
}
```
#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "access": "eyJ0eXAiOiJKV1QiLCJhbGciOyNI15_mqZvIaKvbsK_Od3ds3S-ej1bgYWb3HTyYV2E",
        "refresh": "eyJ0eXAiOiJKV1QiL9.Q2slr4SeZgUry9fULoBoITsxES7hT1GRpDrCfnCHFEU"
    }
}
```
---------------------------------------
> POST, PUT : http://127.0.0.1:8585/api/outlets/v1/outlet/

#### Request body (raw json)
```json
{
    "parent": null,
    "name": "Texnomart",
    "legal_name": "Texnomart",
    "phone": "+998901234567",
    "category": 1,
    "currency": 1,
    "latitude": 41.123456,
    "longitude": 71.123456,
    "region": 1,
    "district": 1,
    "images": [1]
}
// create a child store
//{
//    "parent": {parent outlet id},
//}
```
#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 10,
        "coworkers": [
            {
                "id": 1,
                "groups": [],
                "created_at": "2022-06-18T22:53:10.725464+05:00",
                "username": null,
                "first_name": null,
                "last_name": null,
                "fullname": null,
                "legal_name": null,
                "email": null,
                "phone": "+998901234500",
                "activated_date": null,
                "language": "UZ",
                "is_staff": true
            }
        ],
        "created_at": "2022-06-26T15:34:51.484549+05:00",
        "updated_at": "2022-06-26T15:34:51.484571+05:00",
        "name": "Texnomart filial",
        "legal_name": "OOO Texnomart",
        "phone": "+998901234567",
        "email": "dts@gmail.com",
        "currency": 1,
        "latitude": "41.123456",
        "longitude": "71.123456",
        "status": 1,
        "parent": null,
        "category": 1,
        "region": 1,
        "district": 1
    }
}
```

---------------------------------------
> GET: http://127.0.0.1:8585/api/outlets/v1/my-outlet/

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 10,
        "coworkers": [
            {
                "id": 1,
                "groups": [],
                "created_at": "2022-06-18T22:53:10.725464+05:00",
                "username": null,
                "first_name": null,
                "last_name": null,
                "fullname": null,
                "legal_name": null,
                "email": null,
                "phone": "+998901234500",
                "activated_date": null,
                "language": "UZ",
                "is_staff": true
            }
        ],
        "created_at": "2022-06-26T15:34:51.484549+05:00",
        "updated_at": "2022-06-26T15:34:51.484571+05:00",
        "name": "Texnomart filial",
        "legal_name": "OOO Texnomart",
        "phone": "+998901234567",
        "email": "dts@gmail.com",
        "currency": 1,
        "latitude": "41.123456",
        "longitude": "71.123456",
        "status": 1,
        "parent": null,
        "category": 1,
        "region": 1,
        "district": 1
    }
}
```

---------------------------------------
> POST: http://127.0.0.1:8585/api/outlets/v1/upload/

#### Request body (form data)
```json
{
    "file": <file>
}
```

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 4,
        "url": "http://127.0.0.1:8585/media/upload/orel_muRKzhh.jpg"
    }
}
```

---------------------------------------
> POST: http://127.0.0.1:8585/api/products/v1/unit/ <br>
> GET, PUT: http://127.0.0.1:8585/api/products/v1/unit/{id}/

#### Request body (raw json)
```json
{
    "name": "Kilogram"
}
```

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 1,
        "name": "Kilogram",
        "status": 2
    }
}
```
---------------------------------------
> POST: http://127.0.0.1:8585/api/products/v1/brand/  <br>
> GET, PUT: http://127.0.0.1:8585/api/products/v1/brand/{id}/

#### Request body (raw json)
```json
{
    "name": "Artel"
}
```

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 1,
        "name": "Artel",
        "status": 2
    }
}
```

---------------------------------------
> POST: http://127.0.0.1:8585/api/outlets/v1/category/  <br>
> GET, PUT: http://127.0.0.1:8585/api/outlets/v1/category/{id}/

#### Request body (raw json)
```json
{
    "parent": null,
    "name": "Antiquities"
}
// create a child category
//{
//    "parent": {parent category id},
//}
```

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 1,
        "name": "Antiquities",
        "path": "Antiquities",
        "slug": "antiquities",
        "children": []
    }
}
```

### Exception

```json
{
    "success": false,
    "code": 3,
    "message": "invalid data",
    "debug": [
        {
            "name": [
                "Category already exists!"
            ]
        }
    ]
}
```

---------------------------------------
> POST: http://127.0.0.1:8585/api/products/v1/product/  <br>
> GET, PUT: http://127.0.0.1:8585/api/products/v1/product/{id}/

#### Request body (raw json)
```json
{
    "parent": null,
    "title": "Samsung A3",
    "brand": 1,
    "category": 1,
    "unit": 1,
    "description": "Lorem ipsum",
    "currency": 1,
    "value_added_tax": 2,
    "images": [1, 2],
    "variations": [
        {
            "name": "Color",
            "value": "grey",
            "original_price": 150,
            "selling_price": 152,
            "minimal_price": 151,
            "quantity": 1
        }
    ]
}
```

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 19,
        "title": "Samsung A3",
        "outlet": 10,
        "brand": 1,
        "category": 23,
        "unit": 1,
        "description": "",
        "currency": 1,
        "value_added_tax": 2.0,
        "variations": [
            {
                "id": 47,
                "id_number": "A-59252",
                "barcode": "4780024700016",
                "attribute": "grey",
                "original_price": 150.0,
                "selling_price": 152.0,
                "minimal_price": 151.0,
                "quantity": 1
            }
        ]
    }
}
```

### Exception

```json
{
    "success": false,
    "code": 4,
    "message": "[1, 2, 45] not found!"
}
```


---------------------------------------
> POST: http://127.0.0.1:8585/api/products/v1/product/income/

#### Request body (raw json)
```json
{
    "parent": 1,
    "images": [1, 2],
    "variations": [
        {
            "name": "Network",
            "value": "Unlocked",
            "original_price": 695,
            "selling_price": 615,
            "minimal_price": 605,
            "quantity": 8
        }
    ]
}
```

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 19,
        "title": "Samsung A3",
        "outlet": 10,
        "brand": 1,
        "category": 23,
        "unit": 1,
        "description": "",
        "currency": 1,
        "value_added_tax": 2.0,
        "variations": [
            {
                "id": 1,
                "id_number": "A-59252",
                "barcode": "4780024700016",
                "attribute": "grey",
                "original_price": 150.0,
                "selling_price": 152.0,
                "minimal_price": 151.0,
                "quantity": 1
            },
            {
                "id": 2,
                "id_number": "A-59244",
                "barcode": "4780024700016",
                "attribute": "Unlocked",
                "original_price": 695.0,
                "selling_price": 615.0,
                "minimal_price": 605.0,
                "quantity": 8
            }
        ]
    }
}
```

### Exception

```json
{
    "success": false,
    "code": 3,
    "message": "invalid data",
    "debug": [
        "BaseProduct matching query does not exist."
    ]
}
```

---------------------------------------
> GET: http://127.0.0.1:8585/api/outlets/v1/category/list/

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": [
        {
            "id": 23,
            "name": "Telefon",
            "path": "Electronik > Telefon",
            "slug": "telefon1",
            "children": []
        },
        {
            "id": 21,
            "name": "Computer",
            "path": "Electronik > Computer",
            "slug": "telefon",
            "children": []
        },
        {
            "id": 20,
            "name": "Electronik",
            "path": "Electronik",
            "slug": "electronik",
            "children": [
                {
                    "id": 23,
                    "parent": 20,
                    "name": "Telefon",
                    "path": "Electronik > Telefon",
                    "slug": "telefon1"
                },
                {
                    "id": 21,
                    "parent": 20,
                    "name": "Computer",
                    "path": "Electronik > Computer",
                    "slug": "telefon"
                }
            ]
        },
        {
            "id": 3,
            "name": "Quruq meva",
            "path": "Meva > Quruq meva",
            "slug": "quruq-meva",
            "children": []
        },
        {
            "id": 2,
            "name": "Ho'l meva",
            "path": "Meva > Ho'l meva",
            "slug": "hol-meva",
            "children": []
        },
        {
            "id": 1,
            "name": "Meva",
            "path": "Meva",
            "slug": "meva",
            "children": [
                {
                    "id": 3,
                    "parent": 1,
                    "name": "Quruq meva",
                    "path": "Meva > Quruq meva",
                    "slug": "quruq-meva"
                },
                {
                    "id": 2,
                    "parent": 1,
                    "name": "Ho'l meva",
                    "path": "Meva > Ho'l meva",
                    "slug": "hol-meva"
                }
            ]
        }
    ],
    "count": 7,
    "page": 1,
    "last_page": 1,
    "per_page": 10
}
```


---------------------------------------
> GET: http://127.0.0.1:8585/api/products/v1/product/list/

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": [
        {
            "id": 19,
            "title": "Samsung A3",
            "outlet": 10,
            "brand": 1,
            "category": 23,
            "unit": 1,
            "description": "",
            "currency": 1,
            "value_added_tax": 2.0,
            "variations": [
                {
                    "id": 47,
                    "id_number": "A-59252",
                    "barcode": "4780024700016",
                    "attribute": "grey",
                    "original_price": 150.0,
                    "selling_price": 152.0,
                    "minimal_price": 151.0,
                    "quantity": 1
                },
                {
                    "id": 48,
                    "id_number": "A-59244",
                    "barcode": "4780024700016",
                    "attribute": "Unlocked",
                    "original_price": 695.0,
                    "selling_price": 615.0,
                    "minimal_price": 605.0,
                    "quantity": 8
                }
            ]
        }
    ],
    "count": 1,
    "page": 1,
    "last_page": 1,
    "per_page": 10
}
```