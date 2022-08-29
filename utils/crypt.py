import bcrypt


async def check_pass(password: str, hash_pass: str):
    """
    Check valid password
    :param password: str
    :param hash_pass: bytes
    :return: bool
    """
    password = password.encode('utf-8')
    return bcrypt.checkpw(password, hash_pass.encode('utf-8'))
