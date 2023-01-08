# Attributes API

### Add new attribute name (model: AttributeValue)

> POST: {{BASE}}api/v1/products/attribute/add/

* parent > Attribute
* name > AttributeValue // for a parent

#### Request body (raw json)
```json
{
    "parent": 2,
    "name": "Blue"
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
        "attribute": "Color",
        "name": "Blue"
    }
}
```
---------------------------------------

### Add new parent attribute (model: Attribute)

> POST: {{BASE}}api/v1/products/attribute/

* parent > Attribute
* name > AttributeValue // for a parent

#### Request body (raw json)
```json
{
    "parent":  "Color",
    "name": "white"
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
        "name": "White"
    }
}
```
---------------------------------------

### Update parent and child

> PUT: {{BASE}}api/v1/products/attribute/{parent_id}/

* parent > Attribute // optional
* id > AttributeValue ID
* name > AttributeValue

#### Request body (raw json)
```json
{
    "parent":  "new parent name",
    "id": 1,
    "name": "new value"
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
        "name": "new value"
    }
}
```
---------------------------------------

### Get all attribute values of a single parent

> GET: {{BASE}}api/v1/products/attribute/{parent_id}/

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 1,
        "name": "Color",
        "attributes": [
            {
                "id": 22,
                "attribute": "Color",
                "name": "Brown"
            },
            {
                "id": 21,
                "attribute": "Color",
                "name": "White"
            },
            {
                "id": 11,
                "attribute": "Color",
                "name": "Red"
            },
            {
                "id": 10,
                "attribute": "Color",
                "name": "Yellow"
            },
            {
                "id": 9,
                "attribute": "Color",
                "name": "Green"
            }
        ]
    }
}
```
---------------------------------------

### Get all attribute values of all parents with pagination

> GET: {{BASE}}api/v1/products/attribute/list/

| Query params| Description  |
| ----------- | -----------  |
| ?page=2     |Number of page|
| &per_page=1 |Count per page|

#### Response
```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": [
        {
            "id": 4,
            "name": "Display",
            "attributes": [
                {
                    "id": 19,
                    "attribute": "Display",
                    "name": "Amoled"
                },
                {
                    "id": 18,
                    "attribute": "Display",
                    "name": "AMOLED "
                },
                {
                    "id": 17,
                    "attribute": "Display",
                    "name": "OLED "
                },
                {
                    "id": 16,
                    "attribute": "Display",
                    "name": "IPS"
                },
                {
                    "id": 15,
                    "attribute": "Display",
                    "name": "LCD"
                }
            ]
        },
        {
            "id": 3,
            "name": "Network",
            "attributes": [
                {
                    "id": 14,
                    "attribute": "Network",
                    "name": "T-Mobile"
                },
                {
                    "id": 13,
                    "attribute": "Network",
                    "name": "Verizon"
                },
                {
                    "id": 12,
                    "attribute": "Network",
                    "name": "Unlocked"
                }
            ]
        },
        {
            "id": 2,
            "name": "Color",
            "attributes": [
                {
                    "id": 24,
                    "attribute": "Color",
                    "name": "Blue"
                },
                {
                    "id": 22,
                    "attribute": "Color",
                    "name": "Brown"
                },
                {
                    "id": 21,
                    "attribute": "Color",
                    "name": "White"
                },
                {
                    "id": 11,
                    "attribute": "Color",
                    "name": "Red"
                },
                {
                    "id": 10,
                    "attribute": "Color",
                    "name": "Yellow"
                },
                {
                    "id": 9,
                    "attribute": "Color",
                    "name": "Green"
                }
            ]
        },
        {
            "id": 1,
            "name": "Storage",
            "attributes": [
                {
                    "id": 8,
                    "attribute": "Storage",
                    "name": "512 GB"
                },
                {
                    "id": 7,
                    "attribute": "Storage",
                    "name": "256 GB"
                },
                {
                    "id": 6,
                    "attribute": "Storage",
                    "name": "128 GB"
                },
                {
                    "id": 5,
                    "attribute": "Storage",
                    "name": "64 GB"
                },
                {
                    "id": 4,
                    "attribute": "Storage",
                    "name": "32 GB"
                },
                {
                    "id": 3,
                    "attribute": "Storage",
                    "name": "16 GB"
                },
                {
                    "id": 2,
                    "attribute": "Storage",
                    "name": "8 GB"
                },
                {
                    "id": 1,
                    "attribute": "Storage",
                    "name": "4 GB"
                }
            ]
        }
    ],
    "count": 4,
    "page": 1,
    "last_page": 1,
    "per_page": 10
}
```
---------------------------------------