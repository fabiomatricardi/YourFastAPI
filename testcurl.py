import  subprocess
import urllib.parse
import shlex
query = input("Question: ")
#Safe Encode url string
encodedquery =  urllib.parse.quote(query)
#Join the curl command textx
command = f"curl -X 'GET' 'http://127.0.0.1:8000/lamini?question={encodedquery}' -H 'accept: application/json'"

args = shlex.split(command)
process = subprocess.Popen(args, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
stdout, stderr = process.communicate()
print(stdout)
