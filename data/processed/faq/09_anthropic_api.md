---
domain: faq
product: deepseek-api
section: anthropic_api
source_url: https://api-docs.deepseek.com/zh-cn/guides/anthropic_api
language: zh
---


# Anthropic API

为了满足大家对 Anthropic API 生态的使用需求，我们的 API 新增了对 Anthropic API 格式的支持。通过简单的配置，即可将 DeepSeek 的能力，接入到 Anthropic API 生态中。

---

## 将 DeepSeek 模型接入 Claude Code[​](#将-deepseek-模型接入-claude-code "将 DeepSeek 模型接入 Claude Code的直接链接")

1. 安装 Claude Code

```
npm install -g @anthropic-ai/claude-code
```

2. 配置环境变量

```
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_AUTH_TOKEN=${DEEPSEEK_API_KEY}
export API_TIMEOUT_MS=600000
export ANTHROPIC_MODEL=deepseek-chat
export ANTHROPIC_SMALL_FAST_MODEL=deepseek-chat
export CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1
```

注：设置`API_TIMEOUT_MS`是为了防止输出过长，触发 Claude Code 客户端超时，这里设置的超时时间为 10 分钟。

3. 进入项目目录，执行 `claude` 命令，即可开始使用了。

```
cd my-project
claude
```

![](https://cdn.deepseek.com/api-docs/cc_example.png)

---

## 通过 Anthropic API 调用 DeepSeek 模型[​](#通过-anthropic-api-调用-deepseek-模型 "通过 Anthropic API 调用 DeepSeek 模型的直接链接")

1. 安装 Anthropic SDK

```
pip install anthropic
```

2. 配置环境变量

```
export ANTHROPIC_BASE_URL=https://api.deepseek.com/anthropic
export ANTHROPIC_API_KEY=${YOUR_API_KEY}
```

3. 调用 API

```
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="deepseek-chat",
    max_tokens=1000,
    system="You are a helpful assistant.",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "Hi, how are you?"
                }
            ]
        }
    ]
)
print(message.content)
```

**注意**：当您给 DeepSeek 的 Anthropic API 传入不支持的模型名时，API 后端会自动将其映射到 `deepseek-chat` 模型。

---

## Anthropic API 兼容性细节[​](#anthropic-api-兼容性细节 "Anthropic API 兼容性细节的直接链接")

### HTTP Header[​](#http-header "HTTP Header的直接链接")

| Field | Support Status |
| --- | --- |
| anthropic-beta | Ignored |
| anthropic-version | Ignored |
| x-api-key | Fully Supported |

### Simple Fields[​](#simple-fields "Simple Fields的直接链接")

| Field | Support Status |
| --- | --- |
| model | Use DeepSeek Model Instead |
| max\_tokens | Fully Supported |
| container | Ignored |
| mcp\_servers | Ignored |
| metadata | Ignored |
| service\_tier | Ignored |
| stop\_sequences | Fully Supported |
| stream | Fully Supported |
| system | Fully Supported |
| temperature | Fully Supported (range [0.0 ~ 2.0]) |
| thinking | Supported (`budget_tokens` is ignored) |
| top\_k | Ignored |
| top\_p | Fully Supported |

### Tool Fields[​](#tool-fields "Tool Fields的直接链接")

#### tools[​](#tools "tools的直接链接")

| Field | Support Status |
| --- | --- |
| name | Fully Supported |
| input\_schema | Fully Supported |
| description | Fully Supported |
| cache\_control | Ignored |

#### tool\_choice[​](#tool_choice "tool_choice的直接链接")

| Value | Support Status |
| --- | --- |
| none | Fully Supported |
| auto | Supported (`disable_parallel_tool_use` is ignored) |
| any | Supported (`disable_parallel_tool_use` is ignored) |
| tool | Supported (`disable_parallel_tool_use` is ignored) |

### Message Fields[​](#message-fields "Message Fields的直接链接")

| Field | Variant | Sub-Field | Support Status |
| --- | --- | --- | --- |
| content | string |  | Fully Supported |
| array, type="text" | text | Fully Supported |
| cache\_control | Ignored |
| citations | Ignored |
| array, type="image" |  | Not Supported |
| array, type = "document" |  | Not Supported |
| array, type = "search\_result" |  | Not Supported |
| array, type = "thinking" |  | Supported |
| array, type="redacted\_thinking" |  | Not Supported |
| array, type = "tool\_use" | id | Fully Supported |
| input | Fully Supported |
| name | Fully Supported |
| cache\_control | Ignored |
| array, type = "tool\_result" | tool\_use\_id | Fully Supported |
| content | Fully Supported |
| cache\_control | Ignored |
| is\_error | Ignored |
| array, type = "server\_tool\_use" |  | Not Supported |
| array, type = "web\_search\_tool\_result" |  | Not Supported |
| array, type = "code\_execution\_tool\_result" |  | Not Supported |
| array, type = "mcp\_tool\_use" |  | Not Supported |
| array, type = "mcp\_tool\_result" |  | Not Supported |
| array, type = "container\_upload" |  | Not Supported |
