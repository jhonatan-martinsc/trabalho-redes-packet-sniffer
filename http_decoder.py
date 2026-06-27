def unpack_http(data):
    try:
        decoded_data = data.decode('utf-8', errors='ignore')
        lines = decoded_data.split('\n')
        
        http_info = {'method': None, 'host': None, 'user_agent': None}
        
        for line in lines:
            line = line.strip()
            if line.startswith(('GET', 'POST', 'PUT', 'DELETE')):
                http_info['method'] = line
            elif line.startswith('Host:'):
                http_info['host'] = line.replace('Host: ', '')
            elif line.startswith('User-Agent:'):
                http_info['user_agent'] = line.replace('User-Agent: ', '')
                
        return http_info
    except Exception:
        return None