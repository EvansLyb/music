# API

## 专辑列表

**请求URL：**
- `http://123.207.48.148:6999/api/v1/album`

**请求方式：**
- GET

**参数：**

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|offset |否  |int |页数   |
|limit     |否  |int |返回数量    |
|classification_id     |否  |int | 所属分类的 id    |

**返回示例**

```
{
    "error_code": 0,
    "data": [
        {
            "id": 1,
            "name": "album00",
            "artist": "artist00",
            "is_hot": false,
            "classification": [
                {
                    "id": 1,
                    "name": "cl00"
                },
                ...
            ]
        },
        ...
    ]
}
```


## 专辑详情

**请求URL：**
- `http://123.207.48.148:6999/api/v1/album/:id`

**请求方式：**
- GET

**参数：**
- 无

**返回示例**

```
{
    "error_code": 0,
    "data": {
        "id": 1,
        "name": "album00",
        "artist": "artist00",
        "is_hot": false,
        "classification": [
            {
                "id": 1,
                "name": "cl00"
            },
            ...
        ]
    }
}
```

## 添加专辑

**请求URL：**
- `http://123.207.48.148:6999/api/v1/album`

**请求方式：**
- POST

**参数：**


|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|name     |否  |string | 专辑名称   |
|artist     |否  |string | 歌手名称   |
|is_hot     |否  |boolean | 是否热门专辑    |
|classification     |否  |list | 分类 id 列表    |

**返回示例**

```
{
    "error_code": 0,
    "data": {
        "id": 1,
        "name": "album00",
        "artist": "artist00",
        "is_hot": false,
        "classification": [
            {
                "id": 1,
                "name": "cl00"
            },
            ...
        ]
    }
}
```

## 添加分类

**请求URL：**
- `http://123.207.48.148:6999/api/v1/classification`

**请求方式：**
- POST

**参数：**


|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|name     |是  |int | 分类名称    |
|parent     |否  |int | 父分类 id    |

**返回示例**

```
{
    "error_code": 0,
    "data": {
        "id": 2,
        "name": "cl00",
        "parent": 1
    }
}
```

## 获取分类信息

**请求URL：**
- `http://123.207.48.148:6999/api/v1/classification`

**请求方式：**
- GET

**参数：**
- 无

**返回示例**

```
{
    "error_code": 0,
    "data": [
        {
            "id": 1,
            "name": "Happy",
            "parent": 0
        },
        {
            "id": 2,
            "name": "Cats",
            "parent": 1
        },
        ...
    ]
}
```

## 专辑添加分类

**请求URL：**
- `http://123.207.48.148:6999/api/v1/album/:id`

**请求方式：**
- PUT

**参数：**

|参数名|必选|类型|说明|
|:----    |:---|:----- |-----   |
|classification     |是  |list | 分类 id 列表    |

**返回示例**

```
{
    "error_code": 0,
    "data": {
        "id": 1,
        "name": "album00",
        "artist": "artist00",
        "is_hot": false,
        "classification": [
            {
                "id": 1,
                "name": "cl00"
            },
            ...
        ]
    }
}
```

# Start up

<pre>
virtualenv -p python3 venv
source vent/bin/activate
pip install -r requirements/common.txt
python run.py

curl http://localhost:6999/api/v1/test
</pre>
