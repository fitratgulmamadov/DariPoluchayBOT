from pyngrok import ngrok

ssh_tunnel = ngrok.connect(8003, "http").public_url

print(ssh_tunnel)