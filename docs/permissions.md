### Permission API:

- Global permission list > {{BASE}}api/v1/dashboard/permissions/list/ (All marketplace)-
- User permission list > {{BASE}}api/v1/accounts/user/permissions/ (for requested current user)
- POST, GET, PUT: {{BASE}}api/v1/accounts/role/{id}/  (for CRUD action)

#### Get all permission list

> {{BASE}}api/v1/dashboard/permissions/list/

```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": [
        {
            "id": 4,
            "name": "Foydalanuvchi o'chirish"
        },
        {
            "id": 3,
            "name": "Foydalanuvchini ko'rish"
        },
        {
            "id": 2,
            "name": "Foydalanuvchi tahrirlash"
        },
        {
            "id": 1,
            "name": "Foydalanuvchi qo'shish"
        }
    ],
    "total_count": 4,
    "page": 1,
    "page_count": 1,
    "per_page": 10
}
```

#### Current auth user permission

> {{BASE}}api/v1/accounts/user/permissions/

```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": [
        {
            "id": 7,
            "name": "Owner",
            "permissions": [
                {
                    "id": 1,
                    "name": "Foydalanuvchi qo'shish"
                },
                {
                    "id": 2,
                    "name": "Foydalanuvchi tahrirlash"
                },
                {
                    "id": 4,
                    "name": "Foydalanuvchi o'chirish"
                },
                {
                    "id": 3,
                    "name": "Foydalanuvchini ko'rish"
                }
            ]
        }
    ]
}
```

#### ROLE CRUD API

> POST: {{BASE}}api/v1/accounts/role/

>> PUT: {{BASE}}api/v1/accounts/role/{id}/

```json
{
    "name": "Admin",
    "permissions": [
        1,
        2,
        3,
        4
    ]
}
```

> GET: {{BASE}}api/v1/accounts/role/{id}/

```json
{
    "success": true,
    "code": 0,
    "message": "OK",
    "results": {
        "id": 9,
        "name": "Manager",
        "permissions": [
            {
                "id": 1,
                "name": "Foydalanuvchi qo'shish"
            },
            {
                "id": 2,
                "name": "Foydalanuvchi tahrirlash"
            }
        ]
    }
}
```