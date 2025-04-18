from pydantic import BaseModel, Field
from typing   import Any


class JwksDTO(BaseModel):
    keys: list[dict[str, Any]] = Field(
        examples=[{
          "kty": "RSA",
          "alg": "RS256",
          "use": "sig",
          "kid": "d20a3d8a005a65c0",
          "n"  : "rzCd4EDSQgDpMJlj-VUzc7iGfLMYftxIw...",
          "e"  : "AQAB"
        }]
    )
