from cryptography.hazmat.primitives import hashes
digest = hashes.Hash(hashes.SHA256())
digest.update(b"abc")
digest.update(b"123")
hashs=digest.finalize()
print("The firs one : ",hashs)

digest = hashes.Hash(hashes.SHA256())
digest.update(b"abc")
digest.update(b"124")
hashs=digest.finalize()
print("The second one : ", hashs)

