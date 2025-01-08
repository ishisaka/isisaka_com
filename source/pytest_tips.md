---
date: 2025-01-08 17:50
---

# Pytest Tips

## 公式ドキュメント

* [pytest documentation](https://docs.pytest.org/en/stable/)

## Fixture

### 非同期のfixture

`pytest_asyncio`をインポートして、`@pytest.mark.asyncio`を使うことで非同期のfixtureを定義できる。

```python
import pytest
import pytest_asyncio
from collections.abc import AsyncGenerator

@pytest_asyncio.fixture()
async def fixture() -> AsyncGenerator[str, None]:
    yield "a"

@pytest.mark.asyncio
async def test(fixture: str):
    assert fixture == "a"
```
