from .var import var, varBool, varString


class Controls:
    """Controls implemented by/on and Element"""

    authenticatesDestination = varBool(
        False,
        doc="""Verifies the identity of the destination,
for example by verifying the authenticity of a digital certificate.""",
    )
    authenticatesSource = varBool(False)
    authenticationScheme = varString("")
    authorizesSource = varBool(False)
    checksDestinationRevocation = varBool(
        False,
        doc="""Correctly checks the revocation status
of credentials used to authenticate the destination""",
    )
    checksInputBounds = varBool(False)
    definesConnectionTimeout = varBool(False)
    disablesDTD = varBool(False)
    disablesiFrames = varBool(False)
    encodesHeaders = varBool(False)
    encodesOutput = varBool(False)
    encryptsCookies = varBool(False)
    encryptsSessionData = varBool(False)
    handlesCrashes = varBool(False)
    handlesInterruptions = varBool(False)
    handlesResourceConsumption = varBool(False)
    hasAccessControl = varBool(False)
    implementsAuthenticationScheme = varBool(False)
    implementsCSRFToken = varBool(False)
    implementsNonce = varBool(
        False,
        doc="""Nonce is an arbitrary number
that can be used just once in a cryptographic communication.
It is often a random or pseudo-random number issued in an authentication protocol
to ensure that old communications cannot be reused in replay attacks.
They can also be useful as initialization vectors and in cryptographic
hash functions.""",
    )
    implementsPOLP = varBool(
        False,
        doc="""The principle of least privilege (PoLP),
also known as the principle of minimal privilege or the principle of least authority,
requires that in a particular abstraction layer of a computing environment,
every module (such as a process, a user, or a program, depending on the subject)
must be able to access only the information and resources
that are necessary for its legitimate purpose.""",
    )
    implementsServerSideValidation = varBool(False)
    implementsStrictHTTPValidation = varBool(False)
    invokesScriptFilters = varBool(False)
    isEncrypted = varBool(
        False, doc="Requires incoming data flow to be encrypted"
    )
    isEncryptedAtRest = varBool(False, doc="Stored data is encrypted at rest")
    isHardened = varBool(False)
    isResilient = varBool(False)
    providesConfidentiality = varBool(False)
    providesIntegrity = varBool(False)
    sanitizesInput = varBool(False)
    tracksExecutionFlow = varBool(False)
    usesCodeSigning = varBool(False)
    usesEncryptionAlgorithm = varString("")
    usesMFA = varBool(
        False,
        doc="""Multi-factor authentication is an authentication method
in which a computer user is granted access only after successfully presenting two
or more pieces of evidence (or factors) to an authentication mechanism: knowledge
(something the user and only the user knows), possession (something the user
and only the user has), and inherence (something the user and only the user is).""",
    )
    usesParameterizedInput = varBool(False)
    usesSecureFunctions = varBool(False)
    usesStrongSessionIdentifiers = varBool(False)
    usesVPN = varBool(False)
    validatesContentType = varBool(False)
    validatesHeaders = varBool(False)
    validatesInput = varBool(False)
    verifySessionIdentifiers = varBool(False)

    def _attr_values(self):
        klass = self.__class__
        result = {}
        for i in dir(klass):
            if i.startswith("_") or callable(getattr(klass, i)):
                continue
            attr = getattr(klass, i, {})
            if isinstance(attr, var):
                value = attr.data.get(self, attr.default)
            else:
                value = getattr(self, i)
            result[i] = value
        return result

    def _safeset(self, attr, value):
        try:
            setattr(self, attr, value)
        except ValueError:
            pass
