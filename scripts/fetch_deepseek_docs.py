import os
import time
import textwrap
from typing import List, Dict

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_ROOT = os.path.join(BASE_DIR, "data", "processed")

# 这里是“页面清单配置”，你可以按需要增删
PAGES: List[Dict] = [
    # ===== FAQ 域 =====
    {
        "domain": "faq",
        "section": "first_api_call",
        "url": "https://api-docs.deepseek.com/zh-cn/",
        "outfile": "faq/01_first_api_call.md",
    },
    {
        "domain": "faq",
        "section": "thinking_mode",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/thinking_mode",
        "outfile": "faq/02_thinking_mode.md",
    },
    {
        "domain": "faq",
        "section": "multi_round_chat",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/multi_round_chat",
        "outfile": "faq/03_multi_round_chat.md",
    },
    {
        "domain": "faq",
        "section": "json_mode",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/json_mode",
        "outfile": "faq/04_json_output.md",
    },
    {
        "domain": "faq",
        "section": "tool_calls",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/tool_calls",
        "outfile": "faq/05_tool_calls.md",
    },
    {
        "domain": "faq",
        "section": "kv_cache",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/kv_cache",
        "outfile": "faq/06_kv_cache.md",
    },
    {
        "domain": "faq",
        "section": "chat_prefix_completion",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/chat_prefix_completion",
        "outfile": "faq/07_chat_prefix_completion.md",
    },
    {
        "domain": "faq",
        "section": "fim_completion",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/fim_completion",
        "outfile": "faq/08_fim_completion.md",
    },
    {
        "domain": "faq",
        "section": "anthropic_api",
        "url": "https://api-docs.deepseek.com/zh-cn/guides/anthropic_api",
        "outfile": "faq/09_anthropic_api.md",
    },

    # ===== Tech 域 =====
    {
        "domain": "tech",
        "section": "error_codes",
        "url": "https://api-docs.deepseek.com/zh-cn/quick_start/error_codes",
        "outfile": "tech/01_error_codes.md",
    },
    {
        "domain": "tech",
        "section": "rate_limit",
        "url": "https://api-docs.deepseek.com/zh-cn/quick_start/rate_limit",
        "outfile": "tech/02_rate_limit.md",
    },
    {
        "domain": "tech",
        "section": "deepseek_api",
        "url": "https://api-docs.deepseek.com/zh-cn/api/deepseek-api",
        "outfile": "tech/03_deepseek_api_overview.md",
    },
    {
        "domain": "tech",
        "section": "list_models",
        "url": "https://api-docs.deepseek.com/zh-cn/api/list-models",
        "outfile": "tech/04_list_models.md",
    },
    {
        "domain": "tech",
        "section": "create_chat_completion",
        "url": "https://api-docs.deepseek.com/zh-cn/api/create-chat-completion",
        "outfile": "tech/05_create_chat_completion.md",
    },
    {
        "domain": "tech",
        "section": "create_completion",
        "url": "https://api-docs.deepseek.com/zh-cn/api/create-completion",
        "outfile": "tech/06_create_completion.md",
    },

    # ===== Account 域 =====
    {
        "domain": "account",
        "section": "pricing",
        "url": "https://api-docs.deepseek.com/zh-cn/quick_start/pricing",
        "outfile": "account/01_pricing.md",
    },
    {
        "domain": "account",
        "section": "token_usage",
        "url": "https://api-docs.deepseek.com/zh-cn/quick_start/token_usage",
        "outfile": "account/02_token_usage.md",
    },
    {
        "domain": "account",
        "section": "faq_account",
        "url": "https://api-docs.deepseek.com/zh-cn/faq",
        "outfile": "account/03_faq_account_billing.md",
    },
    # 如果需要，可以再加 get-user-balance 等 API 文档
    # {
    #     "domain": "account",
    #     "section": "get_user_balance",
    #     "url": "https://api-docs.deepseek.com/zh-cn/api/get-user-balance",
    #     "outfile": "account/04_get_user_balance.md",
    # },
]


HEADERS = {
    "User-Agent": "Mozilla/5.0 (TechSupport-Agent Data Prep Script)"
}

NOISE_PATTERNS = [
    "跳到主要内容",
    "微信公众号",
    "社区",
    "更多",
    "Copyright ©",
]


def fetch_html(url: str) -> str:
    resp = requests.get(url, headers=HEADERS, timeout=20)
    resp.raise_for_status()
    # 强制指定为 utf-8 编码，避免 requests 猜错
    resp.encoding = "utf-8"
    return resp.text
    # 或者更保险一点：
    # return resp.content.decode("utf-8", errors="ignore")



def extract_main_html(html: str) -> str:
    """
    尽量只拿文档主体，避免侧边栏 / 顶部导航。
    Docusaurus 文档内容一般在 article 或 div.theme-doc-markdown 里。
    """
    soup = BeautifulSoup(html, "html.parser")

    # 优先 article
    main = soup.find("article")
    if not main:
        # 其次尝试 Docusaurus 的典型 class
        main = soup.find("div", class_="theme-doc-markdown")
    if not main:
        # 再退而求其次找 main 标签
        main = soup.find("main")
    if not main:
        # 实在不行就用 body
        main = soup.body or soup

    return str(main)


def html_to_markdown(html: str) -> str:
    """
    用 markdownify 转成 Markdown，并做一点点简单清理。
    """
    md_text = md(
        html,
        heading_style="ATX",   # 用 # 号标题
        strip=["nav", "header", "footer"],  # 尝试去掉导航/footer
    )

    lines = md_text.splitlines()
    cleaned_lines = []
    for line in lines:
        if any(p in line for p in NOISE_PATTERNS):
            continue
        cleaned_lines.append(line.rstrip())

    # 去掉前后多余空行
    cleaned = "\n".join(cleaned_lines).strip() + "\n"
    return cleaned


def build_frontmatter(page_cfg: Dict) -> str:
    """
    构造 YAML Frontmatter。
    """
    domain = page_cfg["domain"]
    section = page_cfg["section"]
    url = page_cfg["url"]

    frontmatter = f"""\
    ---
    domain: {domain}
    product: deepseek-api
    section: {section}
    source_url: {url}
    language: zh
    ---
    """
    return textwrap.dedent(frontmatter).strip() + "\n\n"


def save_markdown(page_cfg: Dict, markdown_body: str) -> None:
    out_path = os.path.join(OUT_ROOT, page_cfg["outfile"])
    os.makedirs(os.path.dirname(out_path), exist_ok=True)

    fm = build_frontmatter(page_cfg)
    content = fm + markdown_body

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"[OK] {page_cfg['domain']}/{page_cfg['section']} -> {out_path}")


def run():
    for page in PAGES:
        url = page["url"]
        print(f"\n=== Fetching: {url} ===")
        try:
            html = fetch_html(url)
            main_html = extract_main_html(html)
            markdown_body = html_to_markdown(main_html)
            save_markdown(page, markdown_body)
            time.sleep(1.0)  # 友好一点，别连环打
        except Exception as e:
            print(f"[ERROR] {url}: {e}")


if __name__ == "__main__":
    run()
