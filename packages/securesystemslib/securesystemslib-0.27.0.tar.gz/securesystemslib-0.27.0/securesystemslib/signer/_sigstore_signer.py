"""Signer implementation for project sigstore.

Example:
```python
from sigstore.oidc import Issuer

from securesystemslib.signer import SigstoreKey, SigstoreSigner

# Create public key
identity = "luk.puehringer@gmail.com"  # change, unless you know my password
issuer = "https://github.com/login/oauth"
public_key = SigstoreKey.from_dict(
    "abcdefg",
    {
        "keytype": "sigstore-oidc",
        "scheme": "Fulcio",
        "keyval": {
            "issuer": issuer,
            "identity": identity,
        },
    },
)

# Create signer
issuer = Issuer.production()
token = issuer.identity_token()  # requires sign in with GitHub in a browser
signer = SigstoreSigner(token, public_key)

# Sign
signature = signer.sign(b"data")

# Verify
public_key.verify_signature(signature, b"data")

```

"""

import io
import logging
from typing import Any, Dict, Optional

from securesystemslib.exceptions import (
    UnsupportedLibraryError,
    UnverifiedSignatureError,
    VerificationError,
)
from securesystemslib.signer._signer import (
    Key,
    SecretsHandler,
    Signature,
    Signer,
)

IMPORT_ERROR = "sigstore library required to use 'sigstore-oidc' keys"

logger = logging.getLogger(__name__)


class SigstoreKey(Key):
    """Sigstore verifier.

    NOTE: unstable API - routines and metadata formats may change!
    """

    @classmethod
    def from_dict(cls, keyid: str, key_dict: Dict[str, Any]) -> "SigstoreKey":
        keytype = key_dict.pop("keytype")
        scheme = key_dict.pop("scheme")
        keyval = key_dict.pop("keyval")

        for content in ["identity", "issuer"]:
            if content not in keyval or not isinstance(keyval[content], str):
                raise ValueError(
                    f"{content} string required for scheme {scheme}"
                )

        return cls(keyid, keytype, scheme, keyval, key_dict)

    def to_dict(self) -> Dict:
        return {
            "keytype": self.keytype,
            "scheme": self.scheme,
            "keyval": self.keyval,
            **self.unrecognized_fields,
        }

    def verify_signature(self, signature: Signature, data: bytes) -> None:
        # pylint: disable=import-outside-toplevel,import-error
        result = None
        try:
            from sigstore.verify import VerificationMaterials, Verifier
            from sigstore.verify.policy import Identity
            from sigstore_protobuf_specs.dev.sigstore.bundle.v1 import Bundle

            verifier = Verifier.production()
            identity = Identity(
                identity=self.keyval["identity"], issuer=self.keyval["issuer"]
            )
            bundle = Bundle().from_dict(signature.unrecognized_fields["bundle"])
            materials = VerificationMaterials.from_bundle(
                input_=io.BytesIO(data), bundle=bundle, offline=True
            )
            result = verifier.verify(materials, identity)

        except Exception as e:
            logger.info("Key %s failed to verify sig: %s", self.keyid, str(e))
            raise VerificationError(
                f"Unknown failure to verify signature by {self.keyid}"
            ) from e

        if not result:
            logger.info(
                "Key %s failed to verify sig: %s",
                self.keyid,
                getattr(result, "reason", ""),
            )
            raise UnverifiedSignatureError(
                f"Failed to verify signature by {self.keyid}"
            )


class SigstoreSigner(Signer):
    """Sigstore signer.

    NOTE: unstable API - routines and metadata formats may change!
    """

    def __init__(self, token: str, public_key: Key):
        # TODO: Vet public key
        # - signer eligible for keytype/scheme?
        # - token matches identity/issuer?
        self.public_key = public_key
        self._token = token

    @classmethod
    def from_priv_key_uri(
        cls,
        priv_key_uri: str,
        public_key: Key,
        secrets_handler: Optional[SecretsHandler] = None,
    ) -> "SigstoreSigner":
        raise NotImplementedError()

    def sign(self, payload: bytes) -> Signature:
        """Signs payload using the OIDC token on the signer instance.

        Arguments:
            payload: bytes to be signed.

        Raises:
            Various errors from sigstore-python.

        Returns:
            Signature.

            NOTE: The relevant data is in `unrecognized_fields["bundle"]`.

        """
        # pylint: disable=import-outside-toplevel
        try:
            from sigstore.sign import Signer as _Signer
        except ImportError as e:
            raise UnsupportedLibraryError(IMPORT_ERROR) from e

        signer = _Signer.production()
        result = signer.sign(io.BytesIO(payload), self._token)
        # TODO: Ask upstream if they can make this public
        bundle = result._to_bundle()  # pylint: disable=protected-access

        return Signature(
            self.public_key.keyid,
            bundle.message_signature.signature.hex(),
            {"bundle": bundle.to_dict()},
        )
