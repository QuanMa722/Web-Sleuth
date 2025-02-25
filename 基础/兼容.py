# -*- coding: utf-8 -*-

# 可能会出现乱码问题
# html_content = response.text

# Solution 1
# html_content = response.content.decode()

# Solution 2
# response.encoding = "utf-8"
# html_content = response.text

# Solution 3
# response.encoding = response.apparent_encoding
# html_content = response.text



