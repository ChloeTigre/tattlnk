import tattlnk.da.models as access

test_code = access.Code()
test_code2 = access.Code()
test_code.data = dict(name="chloetigrerouge", gpgid="0xF5B6614B")
test_code.save()
pk = test_code.pk
test_code2.pk = pk
print("test_code.pk", test_code.pk)
test_code.data = dict(name="chloetigrerouge", gpgid="0xE5B6614B")
test_code.save()
test_code.load()
test_code2.load()

assert test_code2.pk == test_code.pk
assert test_code2.data == test_code.data

print("test_code2", test_code2)
print("test_code", test_code)
test_code.delete()

try:
    test_code.load()
    print("Loaded ???", test_code)
except Exception as e:
    print("OK could not load, got exception", e)

try:
    test_code2.load()
    print("Loaded ???", test_code2)
except Exception as e:
    print("OK could not load test_code2, got exception", e)

test_code = access.Code()
try:
    test_code.delete()
    print("Hum, deletion ?")

except Exception as e:
    print("Not deleted")
    print("OK, got exception", e)
