import re
import os.path
from pathlib import Path

domain = input("Please input domain: ")
port = input("Please input port: ")

dir_path = Path(r'/etc/nginx/sites-available/')
file_name = domain + '.txt'
file_path = dir_path.joinpath(file_name)
text = "server {\n\tlisten 80;\n\tserver_name {domain};\n\tlocation / {\n\t\tproxy_pass http://localhost:{port};" \
       "\n\t\tproxy_http_version 1.1;\n\t\tproxy_set_header Upgrade $http_upgrade;" \
       "\n\t\tproxy_set_header Connection 'upgrade';\n\t\tproxy_set_header Host $host;" \
       "\n\t\tproxy_cache_bypass $http_upgrade;\n\t}\n}"
replaces = {"{domain}": domain, "{port}": port}
regex = re.sub("|".join(replaces.keys()), lambda match: replaces[match.string[match.start():match.end()]], text)

filepath = os.path.join(dir_path, domain)
if not os.path.exists(dir_path):
    os.makedirs(dir_path)
f = open(file_path, "w")
f.write(regex)
f.close()

os.system("sudo ln -s /etc/nginx/sites-available/" + domain + " /etc/nginx/sites-enabled/")
os.system("sudo systemctl restart nginx")
os.system("sudo certbot --nginx -d " + domain)
os.system("2")

print(f"The domain: {domain} has been added for port: {port}")