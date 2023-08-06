pip install socianAuthPySDK


import socianAuthPyTest

socian_auth = socianAuthPyTest.authSDK()
test_data = socian_auth.test(5,2)

print(test_data)