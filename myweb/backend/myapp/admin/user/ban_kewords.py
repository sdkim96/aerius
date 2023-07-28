with open('./ban_keywords.txt', encoding='utf-8') as f:
    ban_keywords = f.readlines()

with open('./admin_keywords.txt', encoding='utf-8') as g:
    admin_keywords = g.readlines()

print(ban_keywords)
print(admin_keywords)
