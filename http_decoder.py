def unpack_http(data):
    try:
        decoded_data = data.decode('utf-8', errors='ignore')
        lines = decoded_data.split('\n')
        
        http_info = {'method': None, 'host': None, 'user_agent': None}
        
        for line in lines:
            line = line.strip()
            if line.startswith(('GET ', 'POST ', 'PUT ', 'DELETE ', 'HEAD ', 'PATCH ')):
                http_info['method'] = line
            elif line.lower().startswith('host:'):
                http_info['host'] = line.split(':', 1)[1].strip()
            elif line.lower().startswith('user-agent:'):
                http_info['user_agent'] = line.split(':', 1)[1].strip()
                
        return http_info
    except Exception:
        return None