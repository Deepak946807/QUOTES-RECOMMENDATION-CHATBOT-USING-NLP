import requests

def main():
    r = requests.post('http://localhost:8080/api/message', json={'sender':'user123','message':'funny'})
    print(r.status_code, r.text)

if __name__ == '__main__':
    main()