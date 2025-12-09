---
domain: tech
product: deepseek-api
section: list_models
source_url: https://api-docs.deepseek.com/zh-cn/api/list-models
language: zh
---


# 列出模型

```
GET

## /models
```

列出可用的模型列表，并提供相关模型的基本信息。请前往[模型 & 价格](/zh-cn/quick_start/pricing)查看当前支持的模型列表

## Responses[​](#responses "Responses的直接链接")

* 200

OK, 返回模型列表

* application/json

* Schema
* Example (from schema)
* Example

**Schema**

**object** stringrequired

**Possible values:** [`list`]

**data**

Model[]

required

* Array [

**id** stringrequired

模型的标识符

**object** stringrequired

**Possible values:** [`model`]

对象的类型，其值为 `model`。

**owned\_by** stringrequired

拥有该模型的组织。

* ]

```
{
  "object": "list",
  "data": [
    {
      "id": "string",
      "object": "model",
      "owned_by": "string"
    }
  ]
}
```

```
{
  "object": "list",
  "data": [
    {
      "id": "deepseek-chat",
      "object": "model",
      "owned_by": "deepseek"
    },
    {
      "id": "deepseek-reasoner",
      "object": "model",
      "owned_by": "deepseek"
    }
  ]
}
```

Loading...
