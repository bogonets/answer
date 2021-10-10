# -*- coding: utf-8 -*-

import os
from jwt import encode as jwt_encode
from jwt import decode as jwt_decode
from typing import Optional, Tuple
from datetime import datetime, timedelta
from recc.chrono.datetime import today

VERIFY_AUDIENCE_OPTION_KEY = "verify_aud"
VERIFY_ISSUED_AT_OPTION_KEY = "verify_iat"
VERIFY_EXPIRATION_OPTION_KEY = "verify_exp"
VERIFY_ISSUER_OPTION_KEY = "verify_iss"
VERIFY_SIGNATURE_OPTION_KEY = "verify_signature"
DEFAULT_JWT_ALGORITHM = "HS256"

DEFAULT_DECODE_OPTIONS = {
    VERIFY_AUDIENCE_OPTION_KEY: False,
    VERIFY_ISSUED_AT_OPTION_KEY: False,
    VERIFY_EXPIRATION_OPTION_KEY: True,
    VERIFY_ISSUER_OPTION_KEY: True,
    VERIFY_SIGNATURE_OPTION_KEY: True,
}

DEFAULT_ISSUER_RECC_ACCESS = "recc.a"
DEFAULT_ISSUER_RECC_REFRESH = "recc.r"
DEFAULT_ISSUER_RECC = "recc"

SECONDS_OF_MINUTE = 60.0
SECONDS_OF_HOUR = SECONDS_OF_MINUTE * 60.0
SECONDS_OF_DAY = SECONDS_OF_HOUR * 24.0

DEFAULT_MAX_AGE_SECONDS = SECONDS_OF_DAY
DEFAULT_ACCESS_MAX_AGE_SECONDS = SECONDS_OF_DAY
DEFAULT_REFRESH_MAX_AGE_SECONDS = SECONDS_OF_DAY
DEFAULT_LEEWAY_SECONDS = 1.0
DEFAULT_SIGNATURE_BYTE = 32

# JSON Web Token (JWT)
# https://datatracker.ietf.org/doc/html/rfc7519

ISS_KEY = "iss"  # Issuer, a.k.a. Server Name
AUD_KEY = "aud"  # Audience, a.k.a. User Name
EXP_KEY = "exp"  # Expiration Time (UTC, Seconds, Number), a.k.a. Expiration Time
IAT_KEY = "iat"  # Issued At (UTC, Seconds, Number), a.k.a. Created Time
SUB_KEY = "sub"  # Subject
NBF_KEY = "nbf"  # Not Before
JTI_KEY = "jti"  # JWT ID


def _create_signature(size=DEFAULT_SIGNATURE_BYTE) -> str:
    return os.urandom(size).hex()


class Session:
    def __init__(
        self,
        issuer: str,
        audience: str,
        expiration_time: datetime,
        issued_at: datetime,
    ):
        self.issuer = issuer
        self.audience = audience
        self.expiration_time = expiration_time
        self.issued_at = issued_at

    @property
    def username(self) -> str:
        return self.audience

    def to_claim_dict(self) -> dict:
        return {
            # Registered Claim
            ISS_KEY: self.issuer,
            AUD_KEY: self.audience,
            EXP_KEY: self.expiration_time,
            IAT_KEY: self.issued_at,
            # Public Claim
            # Private Claim
        }

    @classmethod
    def create_from_dict(cls, data: dict):
        return cls(
            issuer=data[ISS_KEY],
            audience=data[AUD_KEY],
            expiration_time=data[EXP_KEY],
            issued_at=data[IAT_KEY],
        )


class SessionFactory:
    def __init__(
        self,
        issuer=DEFAULT_ISSUER_RECC,
        max_age_seconds=DEFAULT_MAX_AGE_SECONDS,
        secret=_create_signature(),
        algorithm=DEFAULT_JWT_ALGORITHM,
        leeway_seconds=DEFAULT_LEEWAY_SECONDS,
    ):
        self.issuer = issuer
        self.max_age_seconds = max_age_seconds
        self.secret = secret
        self.algorithm = algorithm
        self.leeway_seconds = leeway_seconds

    def create_session(
        self,
        username: str,
        issued_at: Optional[datetime] = None,
        max_age: Optional[timedelta] = None,
    ) -> Session:
        issued = issued_at if issued_at else today()
        delta = max_age if max_age else timedelta(seconds=self.max_age_seconds)
        return Session(
            issuer=self.issuer,
            audience=username,
            expiration_time=issued + delta,
            issued_at=issued,
        )

    def encode(self, session: Session) -> str:
        return jwt_encode(
            payload=session.to_claim_dict(),
            key=self.secret,
            algorithm=self.algorithm,
        )

    def decode(self, token: str) -> Session:
        return Session.create_from_dict(
            jwt_decode(
                jwt=token,
                key=self.secret,
                algorithms=[self.algorithm],
                options=DEFAULT_DECODE_OPTIONS,
                issuer=self.issuer,
                leeway=timedelta(seconds=self.leeway_seconds),
            ),
        )


class SessionPairFactory:
    def __init__(
        self,
        access_issuer=DEFAULT_ISSUER_RECC_ACCESS,
        refresh_issuer=DEFAULT_ISSUER_RECC_REFRESH,
        access_max_age_seconds=DEFAULT_ACCESS_MAX_AGE_SECONDS,
        refresh_max_age_seconds=DEFAULT_REFRESH_MAX_AGE_SECONDS,
        access_secret: Optional[str] = None,
        refresh_secret: Optional[str] = None,
        access_algorithm=DEFAULT_JWT_ALGORITHM,
        refresh_algorithm=DEFAULT_JWT_ALGORITHM,
        access_leeway_seconds=DEFAULT_LEEWAY_SECONDS,
        refresh_leeway_seconds=DEFAULT_LEEWAY_SECONDS,
    ):
        self.access = SessionFactory(
            issuer=access_issuer,
            max_age_seconds=access_max_age_seconds,
            secret=access_secret if access_secret else _create_signature(),
            algorithm=access_algorithm,
            leeway_seconds=access_leeway_seconds,
        )
        self.refresh = SessionFactory(
            issuer=refresh_issuer,
            max_age_seconds=refresh_max_age_seconds,
            secret=refresh_secret if refresh_secret else _create_signature(),
            algorithm=refresh_algorithm,
            leeway_seconds=refresh_leeway_seconds,
        )

    def create_sessions(
        self,
        username: str,
        issued_at: Optional[datetime] = None,
        access_max_age: Optional[timedelta] = None,
        refresh_max_age: Optional[timedelta] = None,
    ) -> Tuple[Session, Session]:
        issued = issued_at if issued_at else today()
        return (
            self.access.create_session(username, issued, access_max_age),
            self.refresh.create_session(username, issued, refresh_max_age),
        )

    def encode_access(self, session: Session) -> str:
        return self.access.encode(session)

    def encode_refresh(self, session: Session) -> str:
        return self.refresh.encode(session)

    def create_tokens(
        self,
        username: str,
        issued_at: Optional[datetime] = None,
        access_max_age: Optional[timedelta] = None,
        refresh_max_age: Optional[timedelta] = None,
    ) -> Tuple[str, str]:
        issued = issued_at if issued_at else today()
        access_session, refresh_session = self.create_sessions(
            username, issued, access_max_age, refresh_max_age
        )
        return self.encode_access(access_session), self.encode_refresh(refresh_session)

    def decode_access(self, token: str) -> Session:
        return self.access.decode(token)

    def decode_refresh(self, token: str) -> Session:
        return self.refresh.decode(token)

    def renew_access_token(
        self,
        refresh_token: str,
        issued_at: Optional[datetime] = None,
        max_age: Optional[timedelta] = None,
    ) -> str:
        refresh_session = self.decode_refresh(refresh_token)
        username = refresh_session.audience
        access_session = self.access.create_session(username, issued_at, max_age)
        return self.encode_access(access_session)
