import sys, time

#sys.stdout.reconfigure(encoding='utf-8')

print("ex_pyprint 시작~~")
for i in range(3):
    print(f"응답 {i+1}")
    time.sleep(0.5)
print("ex_pyprint 완료")
